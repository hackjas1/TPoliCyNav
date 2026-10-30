# TPoliCynav — Distance Metric Comparison Report
## Checkpoint 2, Deliverable 9: Mathematical Similarity Metric Evaluation

**Course:** IS Professional Elective #4 (Generative AI Systems)  
**Team:** TEAM KUYS (Avenido, Larosa, Garcia, Avergonzado)  
**Model:** `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors, L2-normalized)  
**Vector Store:** Pinecone Serverless Index (`tpolicynav`)  

---

### 1. Theoretical Comparison of Distance Metrics

| Metric | Mathematical Formula | Range | Characteristics & Complexity |
|---|---|---|---|
| **Cosine Similarity** | $$\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$ | $[-1, +1]$ | Measures angular orientation regardless of vector magnitude. Scale-invariant. Standard for semantic search. |
| **Euclidean Distance ($L_2$)** | $$d(\mathbf{A}, \mathbf{B}) = \sqrt{\sum_{i=1}^n (A_i - B_i)^2}$$ | $[0, +\infty)$ | Measures geometric straight-line distance. Highly sensitive to vector length/magnitude if unnormalized. |
| **Dot Product (Inner Product)** | $$\mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^n A_i B_i$$ | $(-\infty, +\infty)$ | Measures both angle and magnitude. Computationally fastest. Equivalent to Cosine Similarity when vectors are unit-normalized ($L_2=1$). |

---

### 2. Empirical Benchmark on TPC Policy Corpus (119 Chunks)

We evaluated the three metrics on test queries across distinct campus policy domains.

#### Query: "What are the curfew hours for boarding houses near TPC?" (Municipal Ordinance & Student Housing)

| Rank | Metric | Top Matched Chunk ID & Source | Metric Score / Distance | Preview |
|---|---|---|---|---|
| 1 | **Cosine Similarity** | `municipal_ordinance_127_chunk_0001` (municipal_ordinance_127) | **0.7691** | least thirty (30) days. 2. Fire Safety Measures: Accessible, fully charged fire extinguishers on every floor, clearly marked emergency exit routes, functioning smoke detectors, and... |
| 1 | **Euclidean ($L_2$)** | `municipal_ordinance_127_chunk_0001` (municipal_ordinance_127) | **0.6796** (min) | least thirty (30) days. 2. Fire Safety Measures: Accessible, fully charged fire extinguishers on every floor, clearly marked emergency exit routes, functioning smoke detectors, and... |
| 1 | **Dot Product** | `municipal_ordinance_127_chunk_0001` (municipal_ordinance_127) | **0.7691** | least thirty (30) days. 2. Fire Safety Measures: Accessible, fully charged fire extinguishers on every floor, clearly marked emergency exit routes, functioning smoke detectors, and... |

#### Query: "Are students allowed to wear ripped jeans or shorts on campus?" (Dress Code & Campus Regulations)

| Rank | Metric | Top Matched Chunk ID & Source | Metric Score / Distance | Preview |
|---|---|---|---|---|
| 1 | **Cosine Similarity** | `tpc_uniform_and_dress_code_guide_chunk_0001` (tpc_uniform_and_dress_code_guide) | **0.7540** | or decent jeans; tattered or ripped jeans are strictly not allowed). 3. Closed shoes with socks (rubber shoes, sneakers, or casual closed shoes; slippers and open sandals are prohi... |
| 1 | **Euclidean ($L_2$)** | `tpc_uniform_and_dress_code_guide_chunk_0001` (tpc_uniform_and_dress_code_guide) | **0.7015** (min) | or decent jeans; tattered or ripped jeans are strictly not allowed). 3. Closed shoes with socks (rubber shoes, sneakers, or casual closed shoes; slippers and open sandals are prohi... |
| 1 | **Dot Product** | `tpc_uniform_and_dress_code_guide_chunk_0001` (tpc_uniform_and_dress_code_guide) | **0.7540** | or decent jeans; tattered or ripped jeans are strictly not allowed). 3. Closed shoes with socks (rubber shoes, sneakers, or casual closed shoes; slippers and open sandals are prohi... |

#### Query: "What is the minimum GWA required to qualify for GSIS STEM scholarship?" (Scholarships & Financial Grants)

| Rank | Metric | Top Matched Chunk ID & Source | Metric Score / Distance | Preview |
|---|---|---|---|---|
| 1 | **Cosine Similarity** | `gsis_stem_subsidy_chunk_0000` (gsis_stem_subsidy) | **0.8151** | GSIS SUBSIDY FOR SCIENCE, TECHNOLOGY, ENGINEERING, AND MATHEMATICS (GSSP) The Government Service Insurance System (GSIS) provides financial assistance to qualified dependents of GS... |
| 1 | **Euclidean ($L_2$)** | `gsis_stem_subsidy_chunk_0000` (gsis_stem_subsidy) | **0.6081** (min) | GSIS SUBSIDY FOR SCIENCE, TECHNOLOGY, ENGINEERING, AND MATHEMATICS (GSSP) The Government Service Insurance System (GSIS) provides financial assistance to qualified dependents of GS... |
| 1 | **Dot Product** | `gsis_stem_subsidy_chunk_0000` (gsis_stem_subsidy) | **0.8151** | GSIS SUBSIDY FOR SCIENCE, TECHNOLOGY, ENGINEERING, AND MATHEMATICS (GSSP) The Government Service Insurance System (GSIS) provides financial assistance to qualified dependents of GS... |

---

### 3. Key Observations & Mathematical Proof of Equivalence

1. **Identical Ranking Behavior on Normalized Vectors:**  
   Because our embedding pipeline applies $L_2$ normalization (unit length, $\|\mathbf{A}\| = \|\mathbf{B}\| = 1$), the mathematical relationship between Euclidean distance and Cosine similarity is exactly:
   $$d_{L_2}^2 = \|\mathbf{A} - \mathbf{B}\|^2 = \|\mathbf{A}\|^2 + \|\mathbf{B}\|^2 - 2(\mathbf{A} \cdot \mathbf{B}) = 2 - 2\cos(\theta)$$
   $$d_{L_2} = \sqrt{2(1 - \cos(\theta))}$$
   Thus, minimizing Euclidean distance is mathematically monotonic and identical to maximizing Cosine similarity.

2. **Score Interpretability:**  
   Cosine similarity scores map neatly into a bounded interval $[0, 1]$ for text embeddings, making it intuitive to define confidence thresholds (e.g., score $> 0.70$ is high relevance; score $< 0.40$ is out-of-scope). Euclidean distance has unbounded positive values, making static thresholding harder across varying query lengths.

3. **Computational Efficiency:**  
   For pre-normalized embeddings, Dot Product requires only $D$ multiplications and additions per vector without square roots or divisions. This enables maximum throughput in cloud vector indexes.

---

### 4. Recommendation for TPoliCynav

**Recommendation:** **Cosine Similarity (or Normalized Dot Product)** in Pinecone.
- **Why:** BAAI BGE embeddings are optimized for Cosine metric. It provides intuitive thresholding for out-of-domain filtering and zero hallucination guardrails.
- **Pinecone Index Metric:** Configured as `metric="cosine"` on AWS serverless `us-east-1` cluster.