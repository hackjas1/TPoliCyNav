# 🏛️ TPoliCynav: The TPC Policy Navigator

[![CI/CD Pipeline](https://github.com/hackjas1/TPoliCyNav/actions/workflows/ci.yml/badge.svg)](https://github.com/hackjas1/TPoliCyNav/actions)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![Railway](https://img.shields.io/badge/deployed-Railway-green.svg)](https://railway.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An official AI-driven **Retrieval-Augmented Generation (RAG)** conversational agent designed for institutional policy navigation at **Talibon Polytechnic College (TPC)** in Bohol, Philippines.

Developed for **IS Professional Elective #4: Generative AI Systems** (1st Semester, A.Y. 2026–2027)  
**Instructor:** Jessie A. Melendres  

---

## 👥 Project Team (Team Kuys)

| Member Name | Student Role & Ownership | Primary Deliverables |
|---|---|---|
| **Eduardo Avenido Jr.** | Data Pipeline & Vector Indexing Lead | Corpus Curation, Sanitation Pipeline, Ingestion Engine (`scripts/ingest_pipeline.py`) |
| **Christian Paul Larosa** | RAG Orchestration & LangChain Architect | LangChain Custom Retriever, Conversational Memory (`app/rag_engine.py`, `app/memory_manager.py`) |
| **Nielbert Garcia** | Prompt Engineering & Evaluation Lead | 3-Tier Prompt Architecture, Scope Containment, Benchmark Suite (`scripts/demo_evaluation.py`) |
| **Marcel Avergonzado** | Interface Design & Cloud Deployment Lead | Streamlit Web UI (TPC Green Theme), Dockerfile, Railway Cloud Deployment via GitHub |

---

## 🌐 Public Live Application Link

- **Live Web App:** `https://tpolicynav-production.up.railway.app` *(or your generated Railway URL)*
- **Access Protocol:** Opens publicly in any modern browser with **zero login**, **zero installation**, and **no access requests required**.
- **Usage Limits Note:** Powered by free-tier Pinecone Serverless and Hugging Face Inference API quotas. If cloud rate limits occur, the system automatically falls back to its built-in local vector cache and precision policy extractor.

---

## 🚀 Architecture & Tech Stack

```
                              [ Student Inquiry / Web UI ]
                                           │
                                           ▼
                   [ Conversational Memory & Coreference Resolver ]
                                           │
                                           ▼
                    [ Dense Vector Encoding: BAAI/bge-small-en-v1.5 ]
                                           │
                                           ▼
                  [ Pinecone Serverless Vector Store (AWS us-east-1) ]
                               (Local NumPy Fallback)
                                           │
                                           ▼
                  [ Cosine Similarity Score Evaluation (Gate >= 0.50) ]
                       │                                   │
             (Score < 0.50: Refusal)              (Score >= 0.50: Pass)
                       │                                   │
                       ▼                                   ▼
         [ Graceful OSAS Redirection ]       [ LangChain Grounded Synthesis ]
                                             [ Qwen2.5-72B-Instruct / LLM ]
                                                           │
                                                           ▼
                                           [ Answer with Canonical Citations ]
```

| Layer | Component | Description |
|---|---|---|
| **Orchestration** | `LangChain 1.4+` | Custom `BaseRetriever`, prompt chaining, sliding-window session memory |
| **Embeddings** | `BAAI/bge-small-en-v1.5` | 384-dimensional dense vectors, MTEB retrieval leaderboard leader |
| **Vector Database** | `Pinecone Serverless` | Cloud index (`tpolicynav`) on AWS `us-east-1` with Cosine similarity |
| **Generative LLM** | `Qwen2.5-72B-Instruct` | High-precision open foundation model via Hugging Face Inference API |
| **Fallback Engine** | `NumPy Matrix + Extractor` | 100% offline local retrieval and sentence extraction resilience |
| **Web Interface** | `Streamlit 1.35+` | Custom branded UI using TPC official Green, Dark Green, Light Green, and White |
| **Containerization** | `Docker (Multi-Stage)` | Hardened Python 3.11-slim runtime executing under non-root `appuser` |
| **Cloud Hosting** | `Railway via GitHub` | Continuous deployment from GitHub with automated build and HTTPS |

---

## 📚 Official Knowledge Base Sources

The RAG knowledge base comprises **7 official collegiate and municipal documents** (>260 KB sanitized text, 128 semantic chunks):
1. **TPC Student Handbook v.04 (Latest Approved 202-Page Edition):** Academic retention, grading, GWA calculation, 7 degree offerings, student discipline matrices.
2. **Talibon Municipal Ordinance No. 127:** Safety standards, CCTV requirements, and 10:00 PM / 11:00 PM curfews for boarding houses near TPC.
3. **TPC School Uniform & Dress Code Policy Guide:** Type A uniform wearing days, shoe guidelines, and 12 prohibited attires.
4. **TPC Admissions & TPCAT Guidelines:** Freshmen entrance requirements, examination day rules, and degree catalogs.
5. **CHED Free Higher Education Guidelines (RA 10931):** Tuition exemption parameters for Local Universities and Colleges (LUCs).
6. **GSIS Subsidy for STEM (GSSP) Guidelines:** Eligibility standards requiring maintenance of at least 90% GWA.
7. **PNP-TPC Collaborative Security Memorandums:** Protocols for joint boarding house inspections and student safety monitoring.

---

## ⚡ Quickstart & Local Execution Guide

### 1. Clone the Repository
```bash
git clone https://github.com/hackjas1/TPoliCyNav.git
cd TPoliCyNav
```

### 2. Configure Environment Secrets
Copy `.env.example` to `.env` and supply your API keys:
```bash
cp .env.example .env
```
Edit `.env`:
```env
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=tpolicynav
HF_TOKEN=your_huggingface_token_here
```
*(Note: If you do not have cloud API keys, the system automatically runs in 100% offline fallback mode using local vectors).*

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Web Application (TPC Green Theme)
```bash
streamlit run app/streamlit_app.py
```
Open your browser at `http://localhost:8501`.

### 5. Run the Interactive Terminal CLI
```bash
python rag_chatbot.py
# Or force offline mode:
python rag_chatbot.py --offline
```

### 6. Run the Automated Ingestion Pipeline
```bash
# Ingest all documents from data/raw/
python scripts/ingest_pipeline.py

# Ingest a specific new policy document
python scripts/ingest_pipeline.py --file path/to/new_memo.pdf
```

### 7. Run the Benchmark Evaluation Suite
```bash
python scripts/demo_evaluation.py
```

---

## 🐳 Running with Docker

### Local Docker Build & Run
```bash
# Build multi-stage image
docker build -t tpolicynav:latest .

# Run container
docker run -p 8501:8501 --env-file .env tpolicynav:latest
```

### Using Docker Compose
```bash
docker-compose up --build
```
Access the application at `http://localhost:8501`.

---

## 🚢 Deploying to Railway Cloud via GitHub

1. Push this repository to a **Public GitHub repository**:
   ```bash
   git init
   git add .
   git commit -m "feat: complete Checkpoints 3 and 4 RAG chatbot"
   git branch -M main
   git remote add origin https://github.com/hackjas1/TPoliCyNav.git
   git push -u origin main
   ```
2. Log in to [railway.app](https://railway.app) and click **"+ New Project"** $\rightarrow$ **"Deploy from GitHub repo"**.
3. Select your `tpolicynav` repository.
4. In the Railway dashboard under **Variables**, set:
   - `PINECONE_API_KEY`: *(your real Pinecone API key)*
   - `PINECONE_INDEX_NAME`: `tpolicynav`
   - `HF_TOKEN`: *(your real Hugging Face user token)*
5. Under **Settings** $\rightarrow$ **Networking**, click **"Generate Domain"** to obtain your public live URL.

---

## 🧪 Benchmark Evaluation Results

Evaluated via `scripts/demo_evaluation.py` across 6 institutional inquiry test cases:

```
===========================================================================
🏆 EVALUATION SUMMARY: 6/6 Tests Passed (100.0%)
⚡ Average Latency: 2,579.2 ms (2.58 seconds)
🎯 In-Scope Average Confidence: 77.26%
🛡️ Out-of-Scope Hallucination Rate: 0.0% (Correctly Refused)
===========================================================================
```

---

## 📂 Deliverables Directory Structure

```
d:\THESIS CHATBOT\Tpolicynav_1.0\
├── .github/workflows/ci.yml         # Checkpoint 4: Automated CI/CD test workflow
├── .streamlit/config.toml           # Checkpoint 4: Official TPC Green Theme
├── Dockerfile                       # Checkpoint 4: Multi-stage production container
├── docker-compose.yml               # Checkpoint 4: Container orchestration
├── Procfile / railway.json          # Checkpoint 4: Railway Cloud deployment configs
├── requirements.txt                 # Project dependencies
├── README.md                        # Master repository documentation
├── rag_chatbot.py                   # Root shortcut for terminal CLI
├── app.py                           # Root shortcut for Streamlit web app
│
├── app/
│   ├── streamlit_app.py             # Checkpoint 4: Web UI (Green/Light Green/White)
│   ├── rag_engine.py                # Checkpoint 3: LangChain RAG Orchestrator
│   ├── memory_manager.py            # Checkpoint 3: Multi-turn conversational memory
│   └── rag_chatbot.py               # Terminal interactive conversational agent
│
├── scripts/
│   ├── ingest_pipeline.py           # Checkpoint 3: End-to-end automated ingestion
│   ├── demo_evaluation.py           # Checkpoint 3: Benchmark evaluation test suite
│   ├── build_presentation.py        # Generates final defense presentation deck
│   ├── preprocess.py                # Checkpoint 1: Sanitation and chunking
│   ├── generate_embeddings.py       # Checkpoint 1: Dense vector embeddings
│   ├── upload_to_pinecone.py        # Checkpoint 2: Pinecone serverless indexing
│   └── query_pinecone.py            # Checkpoint 2: Similarity search benchmarks
│
├── docs/
│   ├── TPoliCynav_Final_Technical_Report.docx       # Checkpoint 4: 3-5 page report
│   ├── final_technical_report.md                    # Checkpoint 4: Markdown report
│   ├── TPoliCynav_Final_Presentation.pptx           # Checkpoint 4: 12-slide defense deck
│   ├── final_presentation_defense_guide.md          # Checkpoint 4: Defense & video guide
│   ├── TPoliCynav_Model_Customization_PEFT_LoRA.docx# Checkpoint 4: PEFT/LoRA note
│   ├── model_customization_note.md                  # Checkpoint 4: PEFT/LoRA markdown
│   ├── TPoliCynav_Framework_Comparison.docx         # Checkpoint 3: LangChain vs LlamaIndex
│   ├── framework_comparison.md                      # Checkpoint 3: Framework markdown
│   ├── evaluation_results.json                      # Checkpoint 3: Benchmark JSON output
│   ├── containerization_and_secrets.md              # Checkpoint 4: Docker & secrets note
│   ├── railway_deployment_guide.md                  # Checkpoint 4: Railway shipping guide
│   ├── distance_metric_comparison.md                # Checkpoint 2: Distance metric study
│   ├── prompt_engineering.md                        # Checkpoint 2: Prompt architecture
│   └── project_proposal.md                          # Checkpoint 1: Initial proposal
│
├── data/
│   ├── raw/                         # 7 curated institutional policy documents
│   └── processed/                   # chunks.json (128 chunks), embeddings.npy
│
└── prompts/
    ├── system_prompt.txt            # Master institutional system prompt
    └── prompt_templates.py          # Few-shot templates and RAG formatters
```

---

## 📜 License & Academic Integrity

This project is submitted in partial fulfillment of the requirements for **IS Professional Elective #4 (Generative AI Systems)** at **Talibon Polytechnic College**. All collegiate policy excerpts remain the intellectual property of Talibon Polytechnic College and the Local Government Unit of Talibon, Bohol. Source code is licensed under the MIT License.

