# TPoliCynav: The TPC Policy Navigator 🎓🤖

An AI-driven Retrieval-Augmented Generation (RAG) conversational agent for institutional policy navigation at **Talibon Polytechnic College (TPC)** in Bohol, Philippines.

Developed for **IS Professional Elective #4 (Generative AI) — Semester Performance Task Series**.

---

## 👥 Project Team (TEAM KUYS)
- **Eduardo Avenido Jr.**
- **Christian Paul Larosa**
- **Nielbert Garcia**
- **Marcel Avergonzado**

---

## 🚀 Architecture & Tech Stack

```
                                 [ Student Inquiries ]
                                           │
                                           ▼
                 [ Dense Vector Encoding: BAAI/bge-small-en-v1.5 ]
                                           │
                                           ▼
             [ Pinecone Serverless Vector Database (dim=384, Cosine) ]
                                           │
                                           ▼
                         [ Top-K Context Grounding & Prompt ]
                                           │
                                           ▼
             [ Generative LLM: Hugging Face Inference API / Mistral-7B ]
                                           │
                                           ▼
                 [ Grounded Answer with Official Document Citations ]
```

| Layer | Component | Description |
|-------|-----------|-------------|
| **Embeddings** | `BAAI/bge-small-en-v1.5` | 384-dimensional dense vectors, high MTEB retrieval performance |
| **Vector DB** | `Pinecone` (AWS us-east-1) | Managed serverless cloud vector store with cosine similarity index |
| **LLM** | `Hugging Face Inference API` | Qwen / Mistral-7B for policy question answering |
| **Data Corpus** | 7 Documents (30+ Pages) | TPC Student Handbook, Talibon Municipal Ordinance 127, Admissions, PNP, CHED, GSIS |

---

## 📂 Project Structure

```
d:\THESIS CHATBOT\
├── .env.example                        # Template for API keys
├── requirements.txt                   # Project dependencies
├── README.md                          # Main project guide
│
├── docs/
│   ├── project_proposal.md            # Checkpoint 1, Deliverable 1: Formal Proposal
│   └── reflection.md                  # Checkpoint 1, Deliverable 5: Data Cleaning Reflection
│
├── data/
│   ├── raw/                           # Checkpoint 1, Deliverable 2: Raw Document Corpus
│   │   ├── tpc_student_handbook.txt   # Extracted from 202-page handbook PDF
│   │   ├── municipal_ordinance_127.txt# Talibon boarding house & safety ordinance
│   │   ├── admissions_guidelines.txt  # Freshmen admissions & entrance exam rules
│   │   ├── enrollment_info.txt        # 2nd Semester AY 2025-2026 enrollment
│   │   ├── pnp_tpc_security.txt       # Joint PNP-TPC safety & curfew monitoring
│   │   ├── ched_free_education.txt    # RA 10931 Free Higher Education guidelines
│   │   └── gsis_stem_subsidy.txt      # GSIS STEM scholarship (90% GWA)
│   └── processed/
│       ├── chunks.json                # 119 cleaned & tokenized chunks with metadata
│       ├── embeddings.npy             # (119, 384) NumPy dense vector embedding matrix
│       └── chunks_with_embeddings.json# Metadata-rich chunk records
│
├── scripts/
│   ├── extract_pdf.py                 # PDF text extraction utility (pdfplumber)
│   ├── preprocess.py                  # Checkpoint 1, Deliverable 3: Preprocessing pipeline
│   ├── generate_embeddings.py         # Checkpoint 1, Deliverable 4: Embedding generator
│   ├── upload_to_pinecone.py          # Checkpoint 2: Pinecone index creator & batch upsert
│   ├── query_pinecone.py              # Checkpoint 2: Semantic retrieval benchmark
│   └── generate_notebook.py           # Generates Jupyter Notebook for Prelim submission
│
├── notebooks/
│   └── checkpoint1_pipeline.ipynb     # Checkpoint 1 interactive submission notebook
│
├── prompts/
│   ├── system_prompt.txt              # Checkpoint 2: System prompt & scope containment
│   └── prompt_templates.py            # Checkpoint 2: RAG prompt templates & few-shot examples
│
└── app/
    └── rag_chatbot.py                 # Checkpoint 2 & 3: Working RAG Chatbot CLI Application
```

---

## ⚡ Quickstart & Execution Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```env
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=tpolicynav
HF_TOKEN=your_huggingface_read_token
```

### 3. Checkpoint 1 (Prelim) Pipeline
Run the preprocessing and embedding generation demo:
```bash
# Extract raw text from handbook PDF
python scripts/extract_pdf.py

# Clean, normalize, tokenize, and chunk (119 chunks)
python scripts/preprocess.py

# Generate 384-dim dense embeddings with BAAI/bge-small-en-v1.5
python scripts/generate_embeddings.py
```

### 4. Checkpoint 2 (Midterm) Vector Indexing & RAG
```bash
# Create Pinecone index & upsert all 119 vectors with metadata
python scripts/upload_to_pinecone.py

# Test live vector search against Pinecone
python scripts/query_pinecone.py

# Launch the interactive TPoliCynav chatbot
python app/rag_chatbot.py
```

---

## 🏆 Checkpoint Evaluation & Deliverables Matrix

| Checkpoint | Deliverable | Location in Repo | Status |
|------------|-------------|------------------|--------|
| **Checkpoint 1 (Prelim)** | 1. Project Proposal | [`docs/project_proposal.md`](file:///d:/THESIS CHATBOT/docs/project_proposal.md) | ✅ Complete |
| | 2. Data Collection (30+ pages) | [`data/raw/`](file:///d:/THESIS CHATBOT/data/raw) (7 sources, ~260KB text) | ✅ Complete |
| | 3. Preprocessing Script & Notebook | [`scripts/preprocess.py`](file:///d:/THESIS CHATBOT/scripts/preprocess.py) & [`notebooks/checkpoint1_pipeline.ipynb`](file:///d:/THESIS CHATBOT/notebooks/checkpoint1_pipeline.ipynb) | ✅ Complete |
| | 4. Embedding Generation Demo | [`scripts/generate_embeddings.py`](file:///d:/THESIS CHATBOT/scripts/generate_embeddings.py) (`bge-small-en-v1.5`) | ✅ Complete |
| | 5. Data Reflection (½ page) | [`docs/reflection.md`](file:///d:/THESIS CHATBOT/docs/reflection.md) | ✅ Complete |
| | 📄 **Checkpoint 1 Submission DOCX** | [`docs/TPoliCynav_Checkpoint_1_Prelim.docx`](file:///d:/THESIS CHATBOT/docs/TPoliCynav_Checkpoint_1_Prelim.docx) | ✅ Complete |
| **Checkpoint 2 (Midterm)** | 6. Prompt Engineering Document | [`docs/prompt_engineering.md`](file:///d:/THESIS CHATBOT/docs/prompt_engineering.md) & [`prompts/`](file:///d:/THESIS CHATBOT/prompts) | ✅ Complete |
| | 7. API Integration / Chatbot Demo | [`app/rag_chatbot.py`](file:///d:/THESIS CHATBOT/app/rag_chatbot.py) (Working RAG Application) | ✅ Complete |
| | 8. Vector Database Setup | [`scripts/upload_to_pinecone.py`](file:///d:/THESIS CHATBOT/scripts/upload_to_pinecone.py) (`tpolicynav` index) | ✅ Complete |
| | 9. Distance Metric Comparison | [`scripts/compare_metrics.py`](file:///d:/THESIS CHATBOT/scripts/compare_metrics.py) & [`docs/distance_metric_comparison.md`](file:///d:/THESIS CHATBOT/docs/distance_metric_comparison.md) | ✅ Complete |
| | 📄 **Checkpoint 2 Submission DOCX** | [`docs/TPoliCynav_Checkpoint_2_Midterm.docx`](file:///d:/THESIS CHATBOT/docs/TPoliCynav_Checkpoint_2_Midterm.docx) | ✅ Complete |
| **Combined Submission** | 📄 **Master Checkpoints 1 & 2 DOCX** | [`docs/TPoliCynav_Combined_Checkpoints_1_and_2.docx`](file:///d:/THESIS CHATBOT/docs/TPoliCynav_Combined_Checkpoints_1_and_2.docx) | ✅ Complete |

