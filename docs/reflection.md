# Checkpoint 1 Reflection: What Was Messy About Our Data

**Team KUYS** — TPoliCynav: The TPC Policy Navigator

---

## The Challenges We Encountered

### 1. PDF Extraction Artifacts

The TPC Student Handbook, our primary data source at 199 pages, was stored as a scanned/digital PDF on Scribd. Extracting text with `pdfplumber` introduced several types of noise:

- **Page headers and footers** were embedded in the extracted text, creating repetitive noise that would pollute our embeddings.
- **Page numbers** appeared as standalone lines (e.g., "42") scattered throughout, providing zero semantic value.
- **Table formatting** was lost entirely — the disciplinary matrix tables, which map offenses to sanctions, were extracted as jumbled text strings rather than structured data.
- **Line breaks** occurred mid-word due to PDF column wrapping, producing fragments like "dis-\nciplinary" instead of "disciplinary."

**How we handled it:** We built regex-based cleaning functions that strip page markers, rejoin hyphenated words across line breaks, and remove isolated page numbers. For tables, we accepted that some structural meaning would be lost but ensured the raw text content was preserved.

### 2. Mixed Language Content

The handbook contains a mix of English and Filipino (Tagalog/Bisaya) text, particularly in:
- Student pledge sections
- Some disciplinary hearing procedures
- Informal notes and annotations

This posed a challenge because our embedding model (`BAAI/bge-small-en-v1.5`) is primarily trained on English text.

**How we handled it:** Since the vast majority (~95%) of policy content is in English, we kept the Filipino text as-is rather than translating it. The embedding model still captures contextual meaning from surrounding English text, and for Checkpoint 2, we plan to test if bilingual queries return accurate results.

### 3. Inconsistent Document Formatting

Our 7 data sources came in wildly different formats:
- **PDFs** (handbook, ordinance) — required `pdfplumber` extraction
- **Web pages** (admissions, CHED, PNP) — contained HTML boilerplate, CSS, navigation menus
- **Government documents** — used formal legal numbering (Section 1, Article II) vs. the handbook's informal bullet-point style

**How we handled it:** We standardized all documents into plain `.txt` files through our preprocessing pipeline, which normalizes Unicode characters, replaces smart quotes, standardizes bullet points, and collapses excessive whitespace. Every document goes through the same 4-step pipeline: noise removal → normalization → tokenization → chunking.

### 4. Chunking Strategy Decisions

Deciding how to split 199 pages into embedding-ready chunks was non-trivial. Too small (50 words) and we lose context; too large (1000 words) and the embedding becomes too diffuse to match specific queries.

**How we handled it:** We settled on ~400-word chunks with 80-word overlap after testing different sizes. The overlap ensures that sentences spanning chunk boundaries aren't lost. Each chunk carries metadata (source document, chunk ID) so we can trace answers back to their origins.

### 5. Blocked Web Sources

The GSIS website (`gsis.gov.ph`) actively blocked our automated scraping attempts, returning a "Request Rejected" error. This is common with Philippine government websites that employ WAF (Web Application Firewall) protection.

**How we handled it:** We manually copied the relevant content from the GSIS STEM subsidy page and formatted it as a clean text file, maintaining all factual information while removing web navigation elements.

---

## Key Takeaway

Real-world data is inherently messy. The gap between "we have 30 pages of policy documents" and "we have 30 pages of *embedding-ready* text" required significant engineering effort. Our preprocessing pipeline — from PDF extraction through chunking — exists specifically to bridge this gap, and every cleaning decision was made with the downstream embedding model's needs in mind.
