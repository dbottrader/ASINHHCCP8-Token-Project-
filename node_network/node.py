#!/usr/bin/env python3
"""ASIN-HHC <-> CP8 receipt-driven node MVP.

This module intentionally implements a narrow, auditable execution surface:
- deterministic task execution;
- Ed25519-signed receipts;
- independent signature verification;
- deterministic replay verification;
- a minimal HTTP API using only Python's standard library plus cryptography.

It is a prototype and is not a production consensus or financial network.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

PROTOCOL = "asin-hhc-cp8-receipt-v1"
MAX_BODY_BYTES = 1_048_576
SUPPORTED_TASKS = ("sha256", "canonical_json", "merkle_root")


def canonical_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically for hashing and signing."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _leaf_hash(value: Any) -> bytes:
    return hashlib.sha256(b"\x00" + canonical_bytes(value)).digest()


def merkle_root(values: list[Any]) -> str:
    """Return a domain-separated SHA-256 Merkle root for JSON values."""
    if not values:
        return sha256_hex(b"\x00")
    level = [_leaf_hash(value) for value in values]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hashlib.sha256(b"\x01" + level[i] + level[i + 1]).digest()
            for i in range(0, len(level), 2)
        ]
    return level[0].hex()


def execute_task(kind: str, task_input: Any) -> Any:
    """Execute the allow-listed deterministic task kinds."""
    if kind == "sha256":
        return {"sha256": sha256_hex(canonical_bytes(task_input))}
    if kind == "canonical_json":
        return {"canonical_json": canonical_bytes(task_input).decode("utf-8")}
    if kind == "merkle_root":
        if not isinstance(task_input, list):
            raise ValueError("merkle_root input must be a JSON array")
        return {"merkle_root": merkle_root(task_input), "leaf_count": len(task_input)}
    raise ValueError(f"unsupported task kind: {kind}")


def _private_key_bytes(key: Ed25519PrivateKey) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _public_key_bytes(key: Ed25519PublicKey) -> bytes:
    return key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def load_or_create_private_key(path: Path) -> Ed25519PrivateKey:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raw = base64.b64decode(path.read_text(encoding="utf-8").strip(), validate=True)
        if len(raw) != 32:
            raise ValueError(f"invalid Ed25519 private key length in {path}")
        return Ed25519PrivateKey.from_private_bytes(raw)

    key = Ed25519PrivateKey.generate()
    encoded = base64.b64encode(_private_key_bytes(key)).decode("ascii")
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(encoded + "\n", encoding="utf-8")
    os.chmod(temp, 0o600)
    os.replace(temp, path)
    return key


@dataclass(frozen=True)
class NodeIdentity:
    node_id: str
    role: str
    private_key: Ed25519PrivateKey

    @property
    def public_key_b64(self) -> str:
        return base64.b64encode(_public_key_bytes(self.private_key.public_key())).decode("ascii")


def build_receipt(identity: NodeIdentity, task: dict[str, Any]) -> dict[str, Any]:
    task_id = str(task.get("task_id") or uuid.uuid4())
    kind = task.get("kind")
    if kind not in SUPPORTED_TASKS:
        raise ValueError(f"kind must be one of: {', '.join(SUPPORTED_TASKS)}")
    if "input" not in task:
        raise ValueError("task must contain an input field")

    task_input = task["input"]
    output = execute_task(kind, task_input)
    claim = {
        "protocol": PROTOCOL,
        "node_id": identity.node_id,
        "role": identity.role,
        "task_id": task_id,
        "kind": kind,
        "input": task_input,
        "input_sha256": sha256_hex(canonical_bytes(task_input)),
        "output": output,
        "output_sha256": sha256_hex(canonical_bytes(output)),
    }
    claim_bytes = canonical_bytes(claim)
    signature = identity.private_key.sign(claim_bytes)
    return {
        "claim": claim,
        "receipt_hash": sha256_hex(claim_bytes),
        "public_key_ed25519": identity.public_key_b64,
        "signature_ed25519": base64.b64encode(signature).decode("ascii"),
        "observed_at_unix_ms": int(time.time() * 1000),
    }


def verify_receipt(receipt: dict[str, Any], replay: bool = True) -> dict[str, Any]:
    errors: list[str] = []
    claim = receipt.get("claim")
    if not isinstance(claim, dict):
        return {"valid": False, "signature_valid": False, "replay_valid": False, "errors": ["missing claim"]}

    claim_bytes = canonical_bytes(claim)
    calculated_hash = sha256_hex(claim_bytes)
    if receipt.get("receipt_hash") != calculated_hash:
        errors.append("receipt_hash mismatch")

    signature_valid = False
    try:
        public_key_raw = base64.b64decode(receipt["public_key_ed25519"], validate=True)
        signature = base64.b64decode(receipt["signature_ed25519"], validate=True)
        public_key = Ed25519PublicKey.from_public_bytes(public_key_raw)
        public_key.verify(signature, claim_bytes)
        signature_valid = True
    except (KeyError, ValueError, InvalidSignature) as exc:
        errors.append(f"invalid Ed25519 signature: {exc.__class__.__name__}")

    if claim.get("protocol") != PROTOCOL:
        errors.append("unsupported protocol")
    if claim.get("input_sha256") != sha256_hex(canonical_bytes(claim.get("input"))):
        errors.append("input_sha256 mismatch")
    if claim.get("output_sha256") != sha256_hex(canonical_bytes(claim.get("output"))):
        errors.append("output_sha256 mismatch")

    replay_valid = True
    if replay:
        try:
            replay_output = execute_task(str(claim.get("kind")), claim.get("input"))
            replay_valid = replay_output == claim.get("output")
            if not replay_valid:
                errors.append("deterministic replay mismatch")
        except (TypeError, ValueError) as exc:
            replay_valid = False
            errors.append(f"replay failed: {exc}")

    return {
        "valid": signature_valid and replay_valid and not errors,
        "signature_valid": signature_valid,
        "replay_valid": replay_valid,
        "receipt_hash": calculated_hash,
        "errors": errors,
    }


class ReceiptStore:
    """Append-only JSONL storage guarded for concurrent HTTP requests."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def append(self, record: dict[str, Any]) -> None:
        line = canonical_bytes(record) + b"\n"
        with self._lock:
            with self.path.open("ab") as handle:
                handle.write(line)
                handle.flush()
                os.fsync(handle.fileno())


class NodeHTTPServer(ThreadingHTTPServer):
    identity: NodeIdentity
    store: ReceiptStore


class NodeHandler(BaseHTTPRequestHandler):
    server_version = "ASINHHCCP8Node/0.1"

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = canonical_bytes(payload)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if length_header is None:
            raise ValueError("Content-Length is required")
        length = int(length_header)
        if length < 0 or length > MAX_BODY_BYTES:
            raise ValueError(f"request body must be 0..{MAX_BODY_BYTES} bytes")
        raw = self.rfile.read(length)
        value = json.loads(raw.decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError("request JSON must be an object")
        return value

    def do_GET(self) -> None:  # noqa: N802
        identity = self.server.identity
        if self.path == "/v1/health":
            self._send_json(HTTPStatus.OK, {
                "status": "ok",
                "protocol": PROTOCOL,
                "node_id": identity.node_id,
                "role": identity.role,
            })
            return
        if self.path == "/v1/capabilities":
            self._send_json(HTTPStatus.OK, {
                "node_id": identity.node_id,
                "role": identity.role,
                "tasks": list(SUPPORTED_TASKS),
                "receipt": "Ed25519 + canonical JSON + SHA-256",
                "public_key_ed25519": identity.public_key_b64,
            })
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._read_json()
            if self.path == "/v1/execute":
                if self.server.identity.role not in {"worker", "worker_validator"}:
                    self._send_json(HTTPStatus.FORBIDDEN, {"error": "node role cannot execute tasks"})
                    return
                receipt = build_receipt(self.server.identity, payload)
                self.server.store.append({"type": "execution_receipt", "receipt": receipt})
                self._send_json(HTTPStatus.OK, receipt)
                return

            if self.path == "/v1/verify":
                receipt = payload.get("receipt", payload)
                if not isinstance(receipt, dict):
                    raise ValueError("receipt must be a JSON object")
                result = verify_receipt(receipt, replay=bool(payload.get("replay", True)))
                self.server.store.append({"type": "verification_result", "result": result})
                self._send_json(HTTPStatus.OK if result["valid"] else HTTPStatus.UNPROCESSABLE_ENTITY, result)
                return

            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc:  # fail closed without returning a stack trace
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"internal error: {exc.__class__.__name__}"})

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))


def serve(args: argparse.Namespace) -> None:
    data_dir = Path(args.data_dir)
    key = load_or_create_private_key(data_dir / "identity.key")
    identity = NodeIdentity(node_id=args.node_id, role=args.role, private_key=key)
    server = NodeHTTPServer((args.host, args.port), NodeHandler)
    server.identity = identity
    server.store = ReceiptStore(data_dir / "receipts.jsonl")
    print(json.dumps({
        "event": "node_started",
        "node_id": identity.node_id,
        "role": identity.role,
        "listen": f"http://{args.host}:{args.port}",
        "protocol": PROTOCOL,
        "public_key_ed25519": identity.public_key_b64,
    }, sort_keys=True), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def self_test() -> int:
    key = Ed25519PrivateKey.generate()
    identity = NodeIdentity("self-test-node", "worker_validator", key)
    task = {"task_id": "self-test-001", "kind": "merkle_root", "input": [{"x": 1}, {"x": 2}]}
    receipt = build_receipt(identity, task)
    result = verify_receipt(receipt, replay=True)
    print(json.dumps({"receipt": receipt, "verification": result}, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASIN-HHC <-> CP8 receipt-driven node MVP")
    subparsers = parser.add_subparsers(dest="command", required=True)

    serve_parser = subparsers.add_parser("serve", help="run a worker or validator HTTP node")
    serve_parser.add_argument("--host", default=os.environ.get("NODE_HOST", "0.0.0.0"))
    serve_parser.add_argument("--port", type=int, default=int(os.environ.get("NODE_PORT", "8000")))
    serve_parser.add_argument("--node-id", default=os.environ.get("NODE_ID", "asin-hhc-cp8-node-001"))
    serve_parser.add_argument(
        "--role",
        choices=("worker", "validator", "worker_validator"),
        default=os.environ.get("NODE_ROLE", "worker_validator"),
    )
    serve_parser.add_argument("--data-dir", default=os.environ.get("NODE_DATA_DIR", "./data"))
    serve_parser.set_defaults(func=serve)

    test_parser = subparsers.add_parser("self-test", help="generate, sign, and replay-verify a local receipt")
    test_parser.set_defaults(func=lambda _args: sys.exit(self_test()))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
