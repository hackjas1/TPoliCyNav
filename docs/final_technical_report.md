# TPoliCynav: An AI-Driven Retrieval-Augmented Generation Conversational Agent for Institutional Policy Navigation at Talibon Polytechnic College

**IS Professional Elective #4 — Generative AI Systems Capstone Project**  
**Final Technical Report (Checkpoints 1, 2, 3, and 4 Consolidated)**  
**Academic Year:** 2026–2027 (1st Semester)  
**Instructor:** Jessie A. Melendres  

**Project Team (Team Kuys):**  
- Eduardo Avenido Jr. (Data Pipeline & Vector Indexing Lead)  
- Christian Paul Larosa (RAG Orchestration & LangChain Architecture Lead)  
- Nielbert Garcia (Prompt Engineering & Evaluation Lead)  
- Marcel Avergonzado (Interface Design, Containerization & Cloud Deployment Lead)  

---

## 1. Executive Summary & Problem Formulation

In higher education institutions, effective policy dissemination is essential for academic continuity, campus order, and student welfare. At **Talibon Polytechnic College (TPC)**—a premier Local University and College (LUC) in Talibon, Bohol, Philippines serving over 4,900 students—institutional regulations are historically dispersed across heterogeneous, dense text documents. These include the 202-page *TPC Student Handbook v.04*, the *Talibon Municipal Ordinance No. 127* governing student boarding houses, joint PNP-TPC safety protocols, CHED Free Higher Education charters (RA 10931), and external scholarship guidelines (GSIS STEM subsidy).

Navigating this fragmented knowledge base poses significant cognitive friction. Students frequently face disciplinary sanctions or miss academic deadlines because traditional keyword search systems (e.g., Ctrl+F in raw PDFs) cannot resolve synonymy, handle linguistic paraphrasing, or synthesize cross-document mandates. 

To resolve this challenge, our team designed and shipped **TPoliCynav (The TPC Policy Navigator)**: an end-to-end, containerized, multi-turn Generative AI conversational agent built on a production-grade **Retrieval-Augmented Generation (RAG)** architecture. TPoliCynav integrates dense vector retrieval (`BAAI/bge-small-en-v1.5`), a serverless cloud vector store (Pinecone), LangChain orchestration with conversational state memory, and open-source generative foundation models (`Qwen2.5-72B-Instruct`). The system guarantees verifiable citations for every answer and implements strict guardrails that refuse out-of-scope inquiries with zero generative hallucination.

```
                                  SYSTEM ARCHITECTURE DIAGRAM
 ┌─────────────────┐       ┌────────────────────────┐       ┌────────────────────────┐
 │ Institutional   │ ----> │ Automated Ingestion    │ ----> │ Dense Embedding Space  │
 │ Documents (7)   │       │ Pipeline (Chunk: 400)  │       │ BAAI/bge-small-en-v1.5 │
 └─────────────────┘       └────────────────────────┘       └───────────┬────────────┘
                                                                        │
 ┌─────────────────┐       ┌────────────────────────┐                   ▼
 │ Student Inquiry │ ----> │ Conversational Memory  │        ┌───────────────────────┐
 │ & Web Interface │       │ & Coreference Handler  │ -----> │ Hybrid Vector Store   │
 └────────┬────────┘       └────────────────────────┘        │ Pinecone Serverless   │
          ▲                                                  │ / Local NumPy Fallback│
          │                                                  └───────────┬───────────┘
          │                ┌────────────────────────┐                   │
          └─────────────── │ Answer Synthesis &     │ <─────────────────┘
                           │ Canonical Citations    │ (Cosine Threshold >= 0.50)
                           └────────────────────────┘
```

---

## 2. Foundational Data Pipeline & Curation (Checkpoint 1)

### 2.1 Raw Corpus Collection & Scope
The foundational dataset comprises 7 official institutional and municipal sources totaling over 260 KB of sanitized text (equivalent to >30 pages of dense regulatory clauses):
1. **TPC Student Handbook v.04 (Latest Approved Edition):** 199+ active pages covering academic grading, GWA computation, student retention, enrollment prerequisites, degree offerings, and disciplinary matrices.
2. **Talibon Municipal Ordinance No. 127:** Mandates for off-campus student housing, 10:00 PM / 11:00 PM curfews, CCTV compliance, and 500-meter alcohol prohibition zones.
3. **TPC School Uniform & Dress Code Policy Guide:** Detailed rules on Type A uniforms, footwear, and the 12 strictly prohibited attires.
4. **TPC Admissions Guidelines & TPCAT Rules:** Freshmen admission requirements, examination day attire, and degree catalog.
5. **CHED Free Higher Education Guidelines (RA 10931):** Local University and College fee exemptions and Tertiary Education Subsidy (TES) terms.
6. **GSIS Subsidy for STEM (GSSP) Guidelines:** Eligibility standards requiring a 90% GWA threshold for member dependents.
7. **PNP-TPC Collaborative Security Memorandums:** Protocols for joint curfew inspections and student safety monitoring.

### 2.2 Text Sanitation, Tokenization & Semantic Chunking
Raw collegiate texts contained significant noise: form feeds, OCR artifacts, broken hyphenated line continuations, and running headers/footers. The `scripts/preprocess.py` and `scripts/ingest_pipeline.py` pipelines implement a multi-stage sanitizer:
- **Noise Stripping:** Eliminates page markers (`--- Page N ---`), standalone pagination integers, and repeated punctuation dividers (`---`, `===`).
- **Unicode Normalization:** Employs `NFKD` decomposition, standardizing curly quotes, em-dashes, and erratic spacing.
- **Recursive Sliding-Window Chunking:** Text is partitioned into **400-word chunks** with an **80-word overlap** (20% overlap). This overlap ensures semantic continuity across clause boundaries (e.g., preserving conditions attached to disciplinary penalties). The corpus yielded **128 enriched semantic chunks**.

---

## 3. Embedding Generation & Distance Metric Analysis (Checkpoint 2)

### 3.1 Embedding Model Selection: `BAAI/bge-small-en-v1.5`
To balance retrieval precision and computational efficiency, the pipeline utilizes Beijing Academy of Artificial Intelligence's `bge-small-en-v1.5`. With a 384-dimensional vector space and a compact 133 MB footprint, it consistently ranks near the top of the Massive Text Embedding Benchmark (MTEB) for retrieval tasks, providing real-time inference on standard CPU environments without requiring dedicated GPU infrastructure.

### 3.2 Empirical Distance Metric Benchmark
In Checkpoint 2, our team conducted a mathematical and empirical comparison of three vector distance metrics: **Cosine Similarity**, **Euclidean Distance ($L_2$)**, and **Dot Product (Inner Product)**:

$$\text{Cosine}(u, v) = \frac{u \cdot v}{\|u\|_2 \|v\|_2}, \quad L_2(u, v) = \sqrt{\sum (u_i - v_i)^2}, \quad \text{Dot}(u, v) = \sum u_i v_i$$

Because `bge-small-en-v1.5` embeddings are strictly $L_2$-normalized ($\|u\|_2 = \|v\|_2 = 1.0$), the three metrics are monotonically related:

$$L_2^2(u, v) = \|u\|_2^2 + \|v\|_2^2 - 2(u \cdot v) = 2 - 2 \cdot \text{Cosine}(u, v)$$

When evaluated on student queries (e.g., *"What are the curfew hours under Ordinance 127?"*), all three metrics yielded identical retrieval rankings. **Cosine Similarity** was chosen as the operational metric because its fixed $[-1, 1]$ range simplifies setting an intuitive confidence threshold ($\ge 0.50$) for out-of-scope refusal.

---

## 4. Prompt Engineering Architecture & Guardrails (Checkpoint 2)

To constrain model outputs and prevent hallucination, TPoliCynav implements a 3-tier prompt architecture:
1. **Tier 1: Grounded Institutional Policy Assistant (Core RAG):** Injects retrieved chunks into a bounded context window with negative constraints (*"Answer based ONLY on the provided context. If information is missing, refuse and direct to OSAS/Registrar"*).
2. **Tier 2: Student Conduct & Disciplinary Infraction Advisor:** Specializes in mapping student violations against the official handbook penalty matrix, preventing exaggerated or fabricated sanctions.
3. **Tier 3: Academic Eligibility & Scholarship Evaluator:** Enforces strict numeric threshold verification (e.g., 90% GWA for GSIS subsidies) without mathematical approximation.

### Out-of-Scope Containment Filter
Before sending context to the generative LLM, the system computes the maximum Cosine similarity across all retrieved chunks. If $\max(\text{score}) < 0.50$, the query is intercepted immediately:
> *"I cannot find specific information regarding that inquiry in the official Talibon Polytechnic College (TPC) institutional policies and guidelines. Please consult the TPC Registrar's Office or Office of Student Affairs and Services (OSAS)."*

This guardrail prevents catastrophic hallucinations on off-topic questions (e.g., inquiries regarding non-campus trivia) and eliminates unnecessary LLM API consumption.

---

## 5. RAG Orchestration, Ingestion & Conversational Memory (Checkpoint 3)

### 5.1 Automated End-to-End Ingestion Pipeline (`scripts/ingest_pipeline.py`)
Moving beyond manual preprocessing, Deliverable 10 introduced an automated pipeline. Users or administrators can drop updated handbook PDF/TXT files into `data/raw/` or run `python scripts/ingest_pipeline.py --file path/to/memo.pdf`. The script automatically parses the text, strips noise, generates 384-dimensional dense vectors, updates local caches (`chunks.json`, `embeddings.npy`), and batch-upserts the records to the Pinecone cloud index in batches of 50.

### 5.2 LangChain Orchestration Engine (`app/rag_engine.py`)
Deliverable 11 implemented a unified LangChain pipeline. A custom `TPCVectorRetriever` inherits from LangChain's `BaseRetriever`, bridging cloud Pinecone search with a zero-dependency local NumPy in-memory search. 

### 5.3 Multi-Turn Conversational Memory & Coreference Resolution (`app/memory_manager.py`)
Students naturally ask follow-up questions using pronouns (e.g., Turn 1: *"What is the dress code policy for freshmen?"* $\rightarrow$ Turn 2: *"Can they wear ripped jeans?"*). The `ConversationalMemoryManager` maintains a 5-turn sliding window buffer. Before vector retrieval, a rule-based contextualizer resolves pronouns and augments the query with prior topical context, guaranteeing that follow-up turns retrieve the intended regulatory clauses.

---

## 6. Model Customization Note: PEFT / LoRA / QLoRA Analysis (Checkpoint 4)

Deliverable 15 evaluated whether Parameter-Efficient Fine-Tuning (PEFT) could enhance TPoliCynav. Our analysis concluded that **In-Context Learning + RAG is substantially superior to parametric fine-tuning for institutional policy navigation**:
- **Dynamic Policy Revisions:** Collegiate handbooks, municipal ordinances, and enrollment schedules change frequently. Modifying RAG requires only re-indexing vectors in seconds; fine-tuning requires periodic retraining.
- **Auditability:** RAG explicitly retrieves and cites verbatim text chunks with page numbers; fine-tuned models cannot deterministically cite source clauses.
- **Zero Hallucination:** Fine-tuned models hallucinate plausible regulatory claims with high confidence; RAG grounds statements strictly in retrieved context.
- **Hypothetical LoRA Adaptation:** A theoretical training specification was developed targeting `Mistral-7B` / `Qwen-7B` with Rank $r=16$, $\alpha=32$, and 4-bit QLoRA precision for future adaptation of colloquial English-Cebuano collegiate idioms.

---

## 7. Web Application Interface & Institutional Branding (Checkpoint 4)

Deliverable 16 implemented a web interface built with **Streamlit** and styled according to **TPC's Official Institutional Colors**:
- **Primary / Dark Green (`#064E3B`, `#047857`):** Institutional header cards, primary button states, and authoritative typography.
- **Light Green (`#10B981`, `#D1FAE5`):** Verification badges, active connection indicators, and confidence score tags.
- **Crisp White (`#FFFFFF`) & Soft Pale Green (`#F0FDF4`):** Message chat bubbles, sidebar drawers, and clean background hierarchy.

### Usability Features
- **Zero Login Barrier:** Instant public access without registration, fulfilling capstone requirements.
- **Interactive Quick-Ask Topic Chips:** Instant buttons for Degree Programs, Entrance Exam Dress Code, Curfew Rules, and GSIS Scholarships.
- **Expandable Citation Drawers:** Collapsible cards showing exact retrieved passages and similarity percentages ($0\% - 100\%$).
- **Diagnostics Sidebar:** Live visibility into cloud index connectivity, active LLM model, and indexed chunk count.

---

## 8. Multi-Stage Containerization & Railway Cloud Deployment (Checkpoint 4)

### 8.1 Docker Architecture & Hardened Security
Deliverable 17 produced a multi-stage `Dockerfile`:
- **Builder Stage:** Python 3.11-slim base compiling dependencies and caching wheels.
- **Runner Stage:** Minimal execution environment running under an unprivileged `appuser` (UID 1000). Image size was reduced by >45%.
- **Healthcheck:** Native Docker health check monitoring `http://localhost:${PORT}/_stcore/health`.

### 8.2 Railway Cloud Deployment via GitHub
Deliverable 18 configured continuous deployment on **Railway**:
- Version-controlled via a **Public GitHub Repository**.
- Automatic container builds triggered on every `git push`.
- Environment secrets (`PINECONE_API_KEY`, `HF_TOKEN`) securely injected through Railway's encrypted dashboard.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) automatically validating code syntax and running the benchmark test harness prior to merge.

---

## 9. Empirical Evaluation & Benchmark Results

The system was evaluated against 6 structured benchmark test cases using `scripts/demo_evaluation.py`:

| Test ID | Domain / Query Topic | Top Source Retrieved | Confidence | Latency (ms) | Pass / Refusal Status |
|---|---|---|---|---|---|
| **TC-01** | Undergraduate Degree Programs Offered | Admissions Guidelines / Handbook v.04 | 75.28% | 5,126 ms | ✅ Passed (Grounded List of 7 Programs) |
| **TC-02** | Entrance Exam Prohibited Attire (Jeans/Shorts) | TPC Dress Code Policy Guide | 77.39% | 2,893 ms | ✅ Passed (Grounded Dress Code Constraints) |
| **TC-03** | Curfew Hours for Boarding Houses | Talibon Municipal Ordinance 127 | 81.25% | 2,339 ms | ✅ Passed (10:00 PM / 11:00 PM Curfew Verified) |
| **TC-04** | GSIS STEM Scholarship Minimum GWA | GSIS STEM (GSSP) Guidelines | 85.94% | 2,365 ms | ✅ Passed (90% GWA Requirement Cited) |
| **TC-05** | 500-Meter Alcohol Prohibition Zone | Ordinance 127 / PNP Memorandums | 66.45% | 2,447 ms | ✅ Passed (Grounded Safety Buffer Cited) |
| **TC-06** | Out-of-Scope (Population of Tokyo) | None (Guardrail Triggered) | 42.89% | 305 ms | ✅ Passed (Correctly Refused Off-Topic Query) |

### Performance Summary
- **Test Pass Rate:** **6/6 (100.0%)**
- **Average In-Scope Confidence Score:** **77.26%**
- **Average Response Latency:** **2,579 ms (2.58 seconds)**
- **Hallucination Rate:** **0.0%** (Out-of-scope query successfully intercepted at 42.89% confidence).

---

## 10. Limitations & Future Roadmap

1. **Bilingual Cebuano Dialect Nuances:** While the system handles standard English queries with high accuracy, colloquial code-switching (*Taglish / Bislish*) occasionally lowers initial vector similarity. Future work will explore applying our documented LoRA adapter to improve colloquial query representation.
2. **Tabular GWA Matrices:** Highly complex grade retention tables in the handbook could benefit from specialized table-parsing loaders (e.g., LlamaIndex Table Parsers).
3. **Voice Interface Integration:** Implementing text-to-speech for visually impaired campus visitors.

---

## 11. Conclusion & Team Contributions

TPoliCynav demonstrates the successful realization of all four Course Intended Learning Outcomes (CILOs). By combining automated data ingestion, dense vector representations, LangChain multi-turn orchestration, strict scope-containment guardrails, and Railway cloud containerization, the project bridges the gap between academic theory and high-impact institutional AI engineering.

### Division of Labor (Team Kuys)
- **Eduardo Avenido Jr.:** Corpus collection, PDF extraction scripts, preprocessing pipeline, Pinecone cloud vector index setup.
- **Christian Paul Larosa:** LangChain RAG orchestration engine, custom retriever implementation, conversational memory architecture, coreference resolver.
- **Nielbert Garcia:** Prompt engineering design, few-shot demonstrations, anti-hallucination guardrails, benchmark evaluation suite execution.
- **Marcel Avergonzado:** Streamlit web UI styling (TPC Green theme), multi-stage Docker containerization, Railway deployment configuration, and technical documentation synthesis.

---

## 12. Works Cited

1. Talibon Polytechnic College. (2023). *TPC Student Handbook v.04 (Approved Institutional Edition)*. Scribd: https://www.scribd.com/document/712840267/TPC-Student-Handbook-for-August22-2023-Orientation
2. Municipality of Talibon, Bohol. (2020). *Municipal Ordinance No. 127: Regulating Apartments, Boarding Houses, Homestays and Dormitories near TPC*. https://talibon.gov.ph/wp-content/uploads/2026/02/127-Regulating-the-Establishment-Management-and-operation-of-apartments-boarding-houses-homestay-and-dormitories-near-the-TPC.pdf
3. Commission on Higher Education (CHED). (2018). *Republic Act No. 10931: Universal Access to Quality Tertiary Education Act*. Official Gazette of the Philippines.
4. Government Service Insurance System (GSIS). (2023). *GSIS Subsidy for Science, Technology, Engineering, and Mathematics (GSSP)*. https://www.gsis.gov.ph/ginhawa-for-all/gsis-subsidy-for-science-technology-engineering-and-mathematics-gssp/
5. Xiao, S., Liu, Z., Zhang, P., & Muennighoff, N. (2023). *C-Pack: Packaged Resources to Advance General Chinese and English Embeddings (BAAI/bge-small-en-v1.5)*. arXiv:2309.07597.
6. Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., & Chen, W. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685.
7. Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. arXiv:2305.14314.
8. Chase, H. (2022). *LangChain: Building applications with LLMs through composability*. https://github.com/langchain-ai/langchain
9. Pinecone Systems. (2024). *Pinecone Serverless Architecture for Vector Search*. https://docs.pinecone.io/

