# ── Build stage ──
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest
COPY pyproject.toml ./

# Install Python dependencies (base only, no ML frameworks)
RUN pip install --no-cache-dir -e "."

# Copy application code
COPY . .

# ── Runtime stage ──
FROM base AS runtime

# Non-root user for security
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
