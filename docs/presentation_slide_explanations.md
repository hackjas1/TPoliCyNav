# TPoliCynav: Presentation Slide Explanations & Speaker Guide

**Project:** TPoliCynav (The TPC Policy Navigator)  
**Topic:** System Architecture & Checkpoint 1 Data Pipeline  
**Target Audience:** Panel Defense / Class Presentation  

---

## Slide 1: System Architecture (End-to-End Pipeline)

### 🎯 Key Message
> *"This slide illustrates the high-level architecture of TPoliCynav, showing the step-by-step transformation of raw institutional policy documents into an interactive, retrieval-augmented conversational agent."*

### 📊 Component Breakdown (Left to Right)

```
[7 Documents] ──► [4-Stage Preprocessing] ──► [BGE-small Embeddings] ──► [Pinecone Vector DB] ──► [RAG Chatbot]
  (30+ pages)        (Clean & Chunk)           (384-dim Vectors)           (119 Vectors)         (3 Prompt Tiers)
```

1. **7 Documents (30+ Pages):**
   * Raw institutional policy documents gathered from Talibon Polytechnic College (Student Handbook, Dress Code, Admissions) and local authorities (Municipal Ordinance 127, PNP Security Guidelines).
2. **Preprocessing (4-Stage Pipeline):**
   * Cleans formatting artifacts, standardizes typography, identifies sentence boundaries, and divides long text into overlapping chunks.
3. **Embeddings (`BAAI/bge-small-en-v1.5`):**
   * Encodes text segments into 384-dimensional dense vectors that capture the semantic meaning of policies rather than just keyword matches.
4. **Pinecone Vector Database (119 Vectors):**
   * Cloud-hosted serverless vector store that indexes all 119 policy vectors for sub-millisecond similarity search using Cosine Similarity.
5. **RAG Chatbot (3 Prompt Tiers):**
   * Student inquiries are embedded in real time, relevant policy chunks are retrieved, and a grounded answer with citations is generated using structured system prompts.

### 🛠️ Technology Stack Justification
* **Embedding Model (`BAAI/bge-small-en-v1.5`):** Lightweight (~130 MB, 384 dimensions), open-source (MIT license), and ranks at the top of the MTEB Retrieval benchmark for its size class.
* **Vector Database (Pinecone Serverless):** Cloud vector store on AWS `us-east-1`, eliminating local vector database overhead and providing fast, scalable cosine similarity queries.
* **Application Framework (Python 3.11 CLI):** Interactive terminal application featuring real-time semantic retrieval, citation tracking, and out-of-scope question filtering.

### 🎙️ Slide 1 Presenter Speaking Script
> *"Good day, everyone. On this slide, we present the System Architecture of TPoliCynav. Our system follows a 5-step Retrieval-Augmented Generation workflow:*  
> *First, we ingest 7 official policy documents covering over 30 pages of campus and local regulations. Second, we clean and structure the text through a 4-stage preprocessing pipeline. Third, we convert each segment into 384-dimensional vector embeddings using the BGE-small model. Fourth, these 119 vectors are stored in Pinecone Serverless vector database. Finally, when a student asks a question, our RAG chatbot retrieves the exact matching policy context and synthesizes a direct, cited response."*

---

## Slide 2: Checkpoint 1 — Data Pipeline

### 🎯 Key Message
> *"This slide details our data foundation for Checkpoint 1—explaining the 7 official policy sources collected and the 4-stage preprocessing pipeline that converts raw text into 119 high-quality semantic chunks."*

### 📚 The 7 Policy Data Sources (Left Column)

| Source Document | Scope & Content |
| :--- | :--- |
| **TPC Student Handbook v.04** | Academic rules, grading policies, student rights, clearance, and code of conduct (199 pages). |
| **Municipal Ordinance No. 127** | Talibon boarding house regulations, safety standards, and student curfew hours. |
| **Uniform & Dress Code Guide** | Guidelines on required campus uniforms, grooming, and examination dress codes. |
| **PNP–TPC Security Protocols** | Security coordination and the 500-meter alcohol and illegal substance prohibition zone. |
| **CHED Free Education (RA 10931)** | Free Higher Education Act guidelines and undergraduate tuition subsidy coverage. |
| **GSIS STEM Subsidy (GSSP)** | Qualification criteria, course eligibility, and General Weighted Average (GWA) requirements. |
| **Admissions & TPCAT Guidelines** | Official list of 7 undergraduate degree programs, entrance exam rules, and documentary requirements. |

### ⚙️ 4-Stage Preprocessing Pipeline (Right Column)

1. **Noise Removal (Regex Cleaning):**
   * Removes page markers (e.g., `--- Page N ---`), headers, footers, standalone page numbers, and rejoins words broken across line breaks.
2. **Unicode Normalization (NFKC):**
   * Standardizes characters to clean ASCII, replacing smart quotes (`“ ”`), directional apostrophes (`’`), and irregular hyphens/dashes.
3. **Sentence Tokenization (NLTK Punkt):**
   * Detects true sentence boundaries using linguistic rules so sentences are never clipped halfway during chunking.
4. **Sliding-Window Chunking (400 Words, 80-Word Overlap):**
   * Packages sentences into chunks of approximately 400 words with an 80-word overlap to ensure continuous context across chunk boundaries.

### 📈 Output Result
* **119 Semantic Chunks** generated $\rightarrow$ encoded into **384-dimensional dense vectors**.

### 🎙️ Slide 2 Presenter Speaking Script
> *"Moving to Checkpoint 1: Data Pipeline. On the left are our 7 official data sources. We covered everything from the TPC Student Handbook and municipal boarding house curfew ordinances to CHED Free Education and GSIS STEM scholarship guidelines.*  
> *On the right, we show our 4-stage preprocessing workflow:*  
> *1. We strip noise like page numbers and headers using regular expressions.*  
> *2. We normalize Unicode characters and typography to standard ASCII.*  
> *3. We tokenize sentences using NLTK Punkt to maintain grammatical integrity.*  
> *4. We segment the text using a 400-word sliding window with 80 words of overlap.*  
> *This produced 119 contextual chunks, fully prepared for vector embedding and retrieval."*

---

## ⚡ Quick 30-Second Presenter Cheat-Sheet

```text
[SLIDE 1 - 30 SECONDS]
"Our system architecture connects 7 institutional policy documents to our RAG Chatbot. 
We preprocess the text, encode it using BGE-small into 384-dimensional embeddings, 
and index 119 vectors in Pinecone Serverless for instant semantic search and grounded answers."

[SLIDE 2 - 30 SECONDS]
"For Checkpoint 1, we ingested 7 official institutional and municipal sources. 
We processed them through 4 stages: noise removal, Unicode normalization, sentence 
tokenization, and sliding-window chunking (400 words with 80-word overlap), 
resulting in 119 clean semantic chunks ready for embedding."
```

---

## 🛡️ Anticipated Defense Q&A (Bonus Prep)

* **Q: Why did you choose BAAI/bge-small-en-v1.5 over OpenAI or other embedding models?**  
  * *Answer:* BGE-small is lightweight (~130 MB), runs locally without API costs, has an MIT open-source license, and achieves top retrieval performance on the Massive Text Embedding Benchmark (MTEB).
* **Q: Why did you use 400-word chunks with an 80-word overlap?**  
  * *Answer:* 400 words provides enough context for complete policy sections (like course lists or penalties), while the 80-word overlap prevents policy rules from being cut off between two chunks.
* **Q: Why Pinecone Serverless?**  
  * *Answer:* Pinecone Serverless provides managed cloud indexing with zero local infrastructure overhead and fast cosine similarity queries over vector embeddings.
