FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY node.py demo_client.py ./

RUN useradd --create-home --uid 10001 nodeuser \
    && mkdir -p /data \
    && chown -R nodeuser:nodeuser /data /app
USER nodeuser

EXPOSE 8000
ENTRYPOINT ["python", "node.py"]
CMD ["serve", "--port", "8000", "--data-dir", "/data"]
