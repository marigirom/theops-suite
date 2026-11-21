# ── Stage 1: builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN python -m venv /venv \
 && /venv/bin/pip install --no-cache-dir -r requirements.txt

# ── Stage 2: final ───────────────────────────────────────────────────────────
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /venv /venv
COPY app/ .
RUN adduser --disabled-password --no-create-home appuser \
 && chown -R appuser:appuser /app
USER appuser
ENV PATH="/venv/bin:$PATH"
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c \
  "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
