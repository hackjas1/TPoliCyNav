# =============================================================================
# TPoliCynav — Production Dockerfile for Railway Cloud & Local Deployment
# =============================================================================

FROM python:3.11-slim

WORKDIR /app

# Install essential runtime tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set model cache directories
ENV HF_HOME=/app/.cache/huggingface \
    TORCH_HOME=/app/.cache/torch \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8501

# Install CPU-optimized PyTorch first (fast build, 150MB footprint instead of 2.5GB CUDA)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy and install application requirements system-wide
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download and cache embedding model during build for instant container startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# Copy application source, data, and configs
COPY . .

# Expose default port
EXPOSE 8501

# Healthcheck monitoring
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8501}/_stcore/health || exit 1

# Start Streamlit dynamically bound to Railway's assigned $PORT
CMD ["sh", "-c", "streamlit run app/streamlit_app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false"]
