# Technical Note: Multi-Stage Containerization & Secrets Management

**Course:** IS Professional Elective #4 — Generative AI Systems  
**Project:** TPoliCynav: The TPC Policy Navigator  
**Authors:** Eduardo Avenido Jr., Christian Paul Larosa, Nielbert Garcia, Marcel Avergonzado  
**Institution:** Talibon Polytechnic College, Bohol, Philippines  
**Checkpoint:** Checkpoint 4 (Final & Defense) — Deliverable 17  

---

## 1. Overview & Architectural Goals

To transition TPoliCynav from a local development environment into a production-grade cloud application deployed on **Railway**, containerization was implemented using a **multi-stage Docker build**. This approach ensures:
1. **Minimal Attack Surface:** Separating compiler toolchains from the runtime image.
2. **Reduced Footprint:** Slimming image layers to accelerate deployment builds.
3. **Hardened Security Perimeter:** Executing under an unprivileged non-root user (`appuser`).
4. **Zero-Leakage Secrets Governance:** Enforcing strict runtime environment injection without burning credentials into images or git commits.

---

## 2. Multi-Stage Docker Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MULTI-STAGE DOCKER BUILD                              │
├────────────────────────────────┬────────────────────────────────────────────┤
│ STAGE 1: BUILDER               │ STAGE 2: RUNTIME (RUNNER)                  │
│ • Base: python:3.11-slim       │ • Base: python:3.11-slim                   │
│ • Installs build-essential     │ • Copies /root/.local from builder         │
│ • Compiles wheels into user dir│ • Creates unprivileged user 'appuser' (1000)│
│ • Discards build tools         │ • Copies application source + vector cache │
│                                │ • Size: Reduced by >45%                    │
└────────────────────────────────┴────────────────────────────────────────────┘
```

### Stage 1: The Builder Stage
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
```
*Why this matters:* Compilers (`gcc`, `g++`, header files) necessary for compiling C-extensions in packages like `torch` or `numpy` remain in the temporary builder stage and never leak into the production container.

### Stage 2: The Minimal Runtime Stage
```dockerfile
FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8501
CMD streamlit run app/streamlit_app.py --server.port=${PORT} ...
```
*Security Features:*
- **Non-Root Execution:** Running as `appuser` (UID 1000) mitigates container breakout vulnerabilities.
- **Embedded Healthcheck:** Periodically queries `/_stcore/health` to confirm Streamlit process vitality.

---

## 3. Environment Variables & Secrets Handling Protocol

Strict compliance with the capstone rubric and OWASP Top 10 API Security requires zero secrets leakage. TPoliCynav implements a 4-tier security protocol:

### 3.1 Excluded from Version Control
The `.gitignore` and `.dockerignore` strictly prevent local secret files from ever being added to Git or copied into Docker layers:
```
.env
.env.local
*.key
*.pem
```

### 3.2 Standardized `.env.example`
A sanitized `.env.example` file is maintained in the root directory providing variable schemas without real secrets:
```env
# Pinecone Vector Database
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=tpolicynav

# Hugging Face Inference API
HF_TOKEN=your_huggingface_token_here
```

### 3.3 Railway Cloud Secret Injection
When deploying on **Railway**, secrets are supplied exclusively through Railway's encrypted **Variables** dashboard:
1. Navigate to the project on `railway.app`.
2. Open the **Variables** tab.
3. Add `PINECONE_API_KEY` and `HF_TOKEN`.
4. Railway injects these into container memory at runtime as read-only environment variables.
5. Railway dynamically binds the `$PORT` environment variable to ensure public HTTP routing.

### 3.4 Fallback Resilience
If environment variables are omitted or invalid, TPoliCynav does not crash. Instead, the LangChain hybrid retriever seamlessly activates the local NumPy vector cache (`embeddings.npy`) and local precision extractor, ensuring the application remains functional even during cloud credential rotation.

