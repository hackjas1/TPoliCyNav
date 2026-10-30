# =============================================================================
# TPoliCynav — Multi-Stage Production Dockerfile
# Optimized for Railway Cloud & Local Docker Deployment
# =============================================================================

# --- Stage 1: Build & Dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY requirements.txt .

# Build wheels to speed up final runtime image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt


# --- Stage 2: Minimal Runtime Environment ---
FROM python:3.11-slim AS runner

WORKDIR /app

# Install lightweight runtime libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Create non-root user for security hardening
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy application source code and pre-indexed datasets
COPY --chown=appuser:appuser . .

# Switch to unprivileged user
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8501

# Expose default application port
EXPOSE 8501

# Healthcheck to verify web service responsiveness
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/_stcore/health || exit 1

# Launch Streamlit web interface
CMD streamlit run app/streamlit_app.py \
    --server.port=${PORT} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false

