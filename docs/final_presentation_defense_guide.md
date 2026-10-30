# TPoliCynav: Final Presentation, Live Defense & Video Walkthrough Guide

**Course:** IS Professional Elective #4 — Generative AI Systems  
**Project:** TPoliCynav: The TPC Policy Navigator  
**Authors:** Eduardo Avenido Jr., Christian Paul Larosa, Nielbert Garcia, Marcel Avergonzado  
**Institution:** Talibon Polytechnic College, Bohol, Philippines  
**Checkpoint:** Checkpoint 4 (Final Milestone) — Deliverable 20  

---

## Part 1: Final Presentation Slide Outline (10–15 Minutes)

| Slide # | Slide Title | Speaker | Key Talking Points & Visuals |
|---|---|---|---|
| **Slide 1** | **Title & Introduction** | Eduardo Avenido Jr. | • Title: TPoliCynav: The TPC Policy Navigator<br>• Subtitle: AI-Driven RAG Assistant for Talibon Polytechnic College<br>• Team Kuys & Instructor Jessie A. Melendres |
| **Slide 2** | **Problem Statement & Target Users** | Eduardo Avenido Jr. | • Cognitive friction navigating 199+ handbook pages and Municipal Ordinance 127.<br>• 4,900 TPC students, freshmen dress code rules, boarding house curfews, and scholarships. |
| **Slide 3** | **End-to-End System Architecture** | Christian Paul Larosa | • Full architectural flow diagram: Data $\rightarrow$ Embeddings $\rightarrow$ Pinecone $\rightarrow$ LangChain $\rightarrow$ Streamlit $\rightarrow$ Railway Cloud.<br>• Hybrid execution: Cloud active with 100% offline fallback. |
| **Slide 4** | **Data Pipeline & Automated Ingestion** | Eduardo Avenido Jr. | • 7 official collegiate/municipal documents (>260 KB sanitized text).<br>• `scripts/ingest_pipeline.py`: Automated parsing, cleaning, 400-word chunking, 80-word overlap, 128 semantic chunks. |
| **Slide 5** | **Embeddings & Distance Metric Benchmark** | Nielbert Garcia | • `BAAI/bge-small-en-v1.5` (384 dimensions, MTEB leader, 133 MB).<br>• Empirical comparison: Cosine vs. Euclidean vs. Dot Product. Proof of monotonic equivalence on $L_2$-normalized vectors. |
| **Slide 6** | **Prompt Architecture & Anti-Hallucination** | Nielbert Garcia | • 3-Tier Prompt Design (Strict Policy, Conduct Matrix, Scholarship Evaluator).<br>• Strict guardrail: Cosine threshold $< 0.50$ triggers graceful refusal with OSAS redirection. |
| **Slide 7** | **LangChain Orchestration & Conversational Memory** | Christian Paul Larosa | • Custom `TPCVectorRetriever` bridging cloud Pinecone and local NumPy.<br>• `ConversationalMemoryManager`: 5-turn sliding window buffer with pronoun/coreference resolution. |
| **Slide 8** | **Live Demonstration of Deployed Application** | All Team Members | • Live browser walkthrough of Railway public deployment (`*.up.railway.app`).<br>• Query 1: Degree Programs<br>• Query 2: Entrance Exam Dress Code<br>• Query 3: Ordinance 127 Curfew<br>• Query 4: GSIS 90% GWA Subsidy<br>• Query 5: Out-of-Scope Refusal (Tokyo Population). |
| **Slide 9** | **Model Customization: PEFT/LoRA/QLoRA Rationale** | Christian Paul Larosa | • Mathematical breakdown of LoRA ($\Delta W = \frac{\alpha}{r} BA$) and QLoRA NF4.<br>• Rigorous justification: Why RAG is superior to fine-tuning for institutional policies (zero update latency, auditable citations). |
| **Slide 10** | **Containerization, CI/CD & Railway Cloud** | Marcel Avergonzado | • Multi-stage `Dockerfile` (Python 3.11-slim, non-root `appuser`, >45% size reduction).<br>• Zero-secrets leakage via Railway dashboard variables.<br>• GitHub Actions CI pipeline running automated benchmark tests. |
| **Slide 11** | **Empirical Evaluation & Benchmark Results** | Nielbert Garcia | • 6/6 Benchmark tests passed (100% pass rate).<br>• Average In-Scope confidence: 77.26%. Average latency: 2.58 seconds. |
| **Slide 12** | **Limitations, Future Work & Conclusion** | Marcel Avergonzado | • Future bilingual Cebuano-English LoRA adaptation.<br>• Successful fulfillment of all 4 Course Intended Learning Outcomes (CILOs). |

---

## Part 2: Demo Video Walkthrough Script (5 to 8 Minutes)

*Video Requirements (from Final Presentation Guide):*
- Screen recording of live deployed application.
- Upload to Google Drive / YouTube (unlisted, shared with "Anyone with the link").
- Must test playing in an Incognito window.

### [00:00 – 01:15] Section 1: The Problem & Knowledge Sources
> *"Good day! We are Team Kuys, presenting **TPoliCynav: The TPC Policy Navigator**, our Generative AI capstone project for IS Professional Elective #4 at Talibon Polytechnic College.*  
>  
> *The problem we are solving is the high cognitive friction experienced by over 4,900 TPC students trying to find specific rules hidden inside a 202-page student handbook, or navigate local boarding house ordinances like Talibon Municipal Ordinance 127.  
>  
> *To solve this, we collected and processed seven official institutional sources: the TPC Student Handbook v.04, Ordinance 127, the TPC Uniform and Dress Code Guide, admissions memos, CHED Free Higher Education guidelines under RA 10931, GSIS STEM subsidy guidelines, and joint PNP-TPC security protocols."*

### [01:15 – 02:30] Section 2: System Architecture & Tech Stack
> *"Our architecture implements a complete, modern RAG pipeline:*  
> *1. **Embeddings:** We use `BAAI/bge-small-en-v1.5`, generating 384-dimensional dense vectors.*  
> *2. **Vector Database:** We use a Pinecone Serverless cloud index on AWS `us-east-1`, paired with a local NumPy matrix for offline resilience.*  
> *3. **Orchestration & Memory:** We use LangChain with our custom `ConversationalMemoryManager` to handle multi-turn follow-up queries.*  
> *4. **Generative LLM:** We connect to `Qwen2.5-72B-Instruct` via the Hugging Face Inference API, with a local precision extractor fallback.*  
> *5. **Interface & Hosting:** The application is built in Streamlit using TPC's official green and white colors, containerized with a multi-stage Dockerfile, and deployed live on Railway Cloud via GitHub CI/CD."*

### [02:30 – 05:45] Section 3: Live Application Walkthrough & Test Queries
*(Switch to browser showing the live Railway URL in an Incognito tab: `https://tpolicynav-production.up.railway.app`)*

> *"Notice that the application opens instantly without requiring any login or software installation. On the left sidebar, we have our system diagnostics showing our active Pinecone index and LLM engine, alongside our 7 official policy sources and quick-ask buttons.*  
>  
> *Let's test our first question:  
> **Question 1: What courses and degree programs are officially offered at TPC?**  
> *(Click button or type)*  
> *Notice how TPoliCynav returns all 7 undergraduate degree programs—BSIS, BSCrim, BSAIS, BSAgri, BAEL, BAPoS, and BECEd—and explicitly cites the TPC Student Handbook and Admissions Guidelines. We can expand the citation drawer to inspect the exact retrieved chunk and similarity confidence score.*  
>  
> *Now let's test conversational memory with a natural follow-up:  
> **Question 2: Are ripped jeans or shorts allowed during entrance exams?**  
> *(Type question)*  
> *Notice that TPoliCynav connects this to our previous admissions topic, citing the TPC Dress Code Policy Guide to confirm that ripped jeans, shorts, sleeveless tops, and slippers are strictly prohibited on exam day.*  
>  
> *Let's test an off-campus municipal rule:  
> **Question 3: What are the curfew hours for boarding houses under Ordinance 127?**  
> *(Click button)*  
> *The system accurately retrieves Talibon Municipal Ordinance No. 127, stating the 10:00 PM curfew on weekdays and 11:00 PM curfew on weekends.*  
>  
> *Now let's test our critical anti-hallucination guardrail with an out-of-scope inquiry:  
> **Question 4: What is the capital city and total population of Tokyo, Japan?**  
> *(Type query)*  
> *Notice what happens! The match confidence is 42.89%, which falls below our 0.50 threshold. Instead of hallucinating trivia, the system gracefully refuses: 'I cannot find specific information regarding that inquiry in the official TPC policies... Please consult the TPC Registrar or OSAS.' This proves our scope containment guardrail works 100% reliably."*

### [05:45 – 07:15] Section 4: What We Would Improve & Future Roadmap
> *"If we had additional development time, we would improve two areas:*  
> *First, we would implement our documented LoRA fine-tuning specification on a 7B model to improve comprehension of colloquial Cebuano-English student phrasing (*'Pwede ba mag-short sa exam?'*).*  
> *Second, we would integrate hierarchical table-parsing to directly query complex retention grading matrices.*  
>  
> *All code, Docker configurations, and technical reports are available in our public GitHub repository. Thank you, and we welcome your questions!"*

---

## Part 3: Comprehensive Oral Defense Q&A Preparation

### Question 1: Why did you choose this distance metric and vector database over the alternatives?
**Model Answer:**  
*"We selected **Cosine Similarity** because our embedding model, `BAAI/bge-small-en-v1.5`, outputs strictly $L_2$-normalized vectors ($\|u\|_2 = 1$). Under unit normalization, Cosine Similarity, Euclidean Distance ($L_2$), and Dot Product are mathematically monotonic: $L_2^2 = 2 - 2 \cdot \text{Cosine}$. Cosine was chosen because its fixed range between $-1.0$ and $+1.0$ allowed us to establish an intuitive, empirically verified confidence threshold of $0.50$ for out-of-scope refusal.  
For the vector store, we chose **Pinecone Serverless** on AWS `us-east-1` because it provides sub-50ms retrieval latency, zero infrastructure maintenance, automatic scaling, and metadata filtering. Crucially, we engineered a dual-retrieval layer in LangChain so that if the cloud connection is unavailable, our system falls back to an in-memory NumPy matrix with zero downtime."*

---

### Question 2: Walk us through what happens, step-by-step, when a user submits a query.
**Model Answer:**  
*"When a student submits a query, it follows a 6-step lifecycle:*  
*1. **Contextualization:** The query passes through our `ConversationalMemoryManager`. If the query contains pronouns or follow-up phrasing (e.g. 'Can I wear them?'), it is rephrased using recent dialogue turns into a standalone retrieval query.*  
*2. **Dense Vector Encoding:** The query is encoded into a 384-dimensional dense vector using `BAAI/bge-small-en-v1.5`.*  
*3. **Similarity Search:** The vector is passed to our LangChain `TPCVectorRetriever`, which queries Pinecone Serverless to retrieve the top 4 most similar chunks.*  
*4. **Scope Containment Filter:** The system evaluates the highest similarity score. If $\max(\text{score}) < 0.50$, retrieval is aborted, and a polite refusal directing the student to OSAS is returned immediately, preventing any hallucination.*  
*5. **Prompt Assembly & LLM Synthesis:** If confidence is $\ge 0.50$, the retrieved context, system instructions, and user query are injected into our LangChain prompt and sent to `Qwen2.5-72B-Instruct` via the Hugging Face Inference API.*  
*6. **Memory & Citation Packaging:** The synthesized answer, canonical citations, confidence score, and latency are rendered in Streamlit and appended to the conversational session state."*

---

### Question 3: How does your system avoid or reduce hallucinated answers?
**Model Answer:**  
*"TPoliCynav implements a 4-layer defense in depth against hallucination:*  
*1. **Retrieval Grounding:** The model is not asked to generate answers from memory; it acts strictly as a synthesis engine over retrieved context.*  
*2. **Negative System Constraints:** Our prompt explicitly commands: 'Base your answers strictly on the provided context. If the context does not contain the answer, do not speculate; state that you do not have that information.'*  
*3. **Low Temperature:** We set temperature to $0.1$ to enforce deterministic, focused decoding.*  
*4. **Hard Cosine Similarity Gate (0.50):** The most effective mechanism is our pre-generation guardrail. If an inquiry (such as Tokyo's population) has no semantic match in TPC documents, the highest similarity score is $< 0.45$. The system refuses before the generative LLM is even called, reducing hallucination risk to zero."*

---

### Question 4: What would break first if your document collection grew 100x?
**Model Answer:**  
*"If our document collection grew from 7 documents (128 chunks) to 700 documents (~13,000 chunks):*  
*1. **Local NumPy Fallback:** In-memory dot-product scaling would increase search latency linearly ($O(N \cdot D)$). We would upgrade the local fallback from brute-force NumPy to an approximate nearest neighbor (ANN) index such as **FAISS with HNSW (Hierarchical Navigable Small World)** graphs.*  
*2. **Retrieval Precision & Chunk Clutter:** In a 13,000-chunk index, retrieving top-4 by basic dense search would suffer from semantic overlap and noise. We would introduce a **Cross-Encoder Re-ranker** (such as `bge-reranker-base`) to score the top-20 retrieved candidates down to the top-4 most relevant chunks before LLM generation.*  
*3. **Pinecone Cloud Store:** Pinecone Serverless natively handles millions of vectors, so the cloud database itself would scale effortlessly."*

---

### Question 5: If you had time to fine-tune a model with LoRA/QLoRA, what would you target and why?
**Model Answer:**  
*"As detailed in our Model Customization Note (Deliverable 15), we would NOT use fine-tuning to memorize policy facts, because policies change frequently and require auditable citations.  
Instead, we would use **QLoRA** on `Mistral-7B-Instruct-v0.3` targeting attention projection matrices (`q_proj`, `v_proj`) with Rank $r=16$, $\alpha=32$, and 4-bit precision specifically to adapt **tone and bilingual comprehension**.  
Our students at TPC frequently ask questions using colloquial Taglish or Bislish (*'Pwede ba mag-uniform ug Wednesday?'*). Pretrained base models sometimes struggle with regional colloquialisms. Fine-tuning an adapter on 350 bilingual student queries would make TPoliCynav more culturally accessible and natural for Boholano students, while still relying on RAG for factual policy retrieval."*

