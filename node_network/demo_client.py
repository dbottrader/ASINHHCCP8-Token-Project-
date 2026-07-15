#!/usr/bin/env python3
"""Dispatch one deterministic task to a worker and verify its receipt."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any


def request_json(method: str, url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, sort_keys=True).encode("utf-8")
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header("Accept", "application/json")
    if body is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed with {exc.code}: {detail}") from exc


def wait_for_health(url: str, attempts: int = 30) -> None:
    for _ in range(attempts):
        try:
            result = request_json("GET", url + "/v1/health")
            if result.get("status") == "ok":
                return
        except Exception:
            time.sleep(1)
    raise RuntimeError(f"node did not become healthy: {url}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", default="http://127.0.0.1:8001")
    parser.add_argument("--validator", default="http://127.0.0.1:8002")
    args = parser.parse_args()

    wait_for_health(args.worker)
    wait_for_health(args.validator)

    task = {
        "task_id": "linkedin-frankenstein-rig-demo-001",
        "kind": "merkle_root",
        "input": [
            {"artifact": "gpu-rig-photo", "sha256": "replace-with-real-photo-hash"},
            {"artifact": "node-build-spec", "version": "0.1.0"},
            {"artifact": "execution-law", "rules": [
                "Capability != Authority",
                "No Receipt = No Promotion",
                "Replay Supersedes Narration",
                "Reality Retains Veto",
            ]},
        ],
    }
    receipt = request_json("POST", args.worker + "/v1/execute", task)
    verification = request_json(
        "POST",
        args.validator + "/v1/verify",
        {"receipt": receipt, "replay": True},
    )
    print(json.dumps({"task": task, "receipt": receipt, "verification": verification}, indent=2, sort_keys=True))
    return 0 if verification.get("valid") is True else 1


if __name__ == "__main__":
    sys.exit(main())
