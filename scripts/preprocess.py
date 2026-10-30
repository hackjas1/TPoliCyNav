"""
=============================================================================
TPoliCynav — Text Preprocessing Pipeline
Checkpoint 1, Deliverable 3: Text Preprocessing Notebook/Script
=============================================================================
Cleans, normalizes, tokenizes, and chunks raw text documents into
embedding-ready segments. Demonstrates before/after examples at each stage.

Usage:
    python scripts/preprocess.py
=============================================================================
"""

import os
import sys
import re
import json
import unicodedata

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Chunking parameters
CHUNK_SIZE = 400        # Target tokens per chunk (approx words)
CHUNK_OVERLAP = 80      # Overlap tokens between chunks


# =============================================================================
# STEP 1: NOISE REMOVAL
# =============================================================================
def remove_noise(text: str) -> str:
    """
    Remove formatting artifacts, page markers, headers/footers,
    and other noise from raw extracted PDF text.
    """
    # Remove page markers (--- Page N ---)
    text = re.sub(r'---\s*Page\s*\d+\s*---', '', text)

    # Remove excessive whitespace and blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove page numbers standing alone on a line
    text = re.sub(r'^\s*\d{1,3}\s*$', '', text, flags=re.MULTILINE)

    # Remove common PDF artifacts
    text = re.sub(r'\x0c', '', text)         # Form feed characters
    text = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', text)  # Control chars

    # Remove repeated dashes/underscores used as separators
    text = re.sub(r'[-_]{5,}', '', text)
    text = re.sub(r'[=]{5,}', '', text)

    # Fix broken words from PDF line wrapping (word- \n continuation)
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)

    return text.strip()


# =============================================================================
# STEP 2: TEXT NORMALIZATION
# =============================================================================
def normalize_text(text: str) -> str:
    """
    Normalize Unicode characters, fix whitespace, and standardize formatting.
    Preserves case since policy documents contain proper nouns and section titles.
    """
    # Unicode normalization (NFKC — compatible decomposition + composition)
    text = unicodedata.normalize('NFKC', text)

    # Replace smart quotes with standard quotes
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')

    # Replace en-dash and em-dash with standard dash
    text = text.replace('\u2013', '-').replace('\u2014', '-')

    # Normalize bullet points
    text = re.sub(r'[•●○▪▸►◦]', '-', text)

    # Collapse multiple spaces into one (but preserve newlines)
    text = re.sub(r'[^\S\n]+', ' ', text)

    # Remove leading/trailing whitespace per line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)

    # Collapse multiple blank lines into maximum two
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# =============================================================================
# STEP 3: SENTENCE TOKENIZATION
# =============================================================================
def tokenize_sentences(text: str) -> list:
    """
    Split text into sentences using regex-based approach.
    Handles abbreviations common in institutional documents and splits on
    major headings, numbered items, and paragraph breaks.
    """
    # Common abbreviations that should NOT trigger sentence splits
    abbreviations = [
        r'Mr\.', r'Mrs\.', r'Ms\.', r'Dr\.', r'Prof\.',
        r'Jr\.', r'Sr\.', r'St\.', r'Ave\.', r'Blvd\.',
        r'No\.', r'Art\.', r'Sec\.', r'Vol\.', r'Inc\.',
        r'Corp\.', r'Ltd\.', r'etc\.', r'vs\.', r'e\.g\.',
        r'i\.e\.', r'a\.m\.', r'p\.m\.', r'Ph\.D\.',
        r'B\.S\.', r'M\.A\.', r'GWA\.', r'AY\.',
    ]

    # Protect abbreviations by replacing dots temporarily
    for i, abbr in enumerate(abbreviations):
        text = re.sub(abbr, f'ABBR{i}PLACEHOLDER', text, flags=re.IGNORECASE)

    # First split on paragraph boundaries / double newlines
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    raw_sentences = []
    for para in paragraphs:
        # Split on sentence-ending punctuation followed by space + uppercase
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', para)
        for s in sents:
            # If a block has no punctuation but contains numbered lists (1. , 2. ) or section headers
            sub_splits = re.split(r'(?=\b(?:ARTICLE|Chapter|PART|SECTION|\d+\.)\s+[A-Z0-9])', s)
            for sub in sub_splits:
                if sub.strip():
                    raw_sentences.append(sub.strip())

    # Restore abbreviations
    restored = []
    for sent in raw_sentences:
        for i, abbr in enumerate(abbreviations):
            clean_abbr = abbr.replace('\\', '')
            sent = sent.replace(f'ABBR{i}PLACEHOLDER', clean_abbr)
        sent = sent.strip()
        if sent:
            restored.append(sent)

    return restored


# =============================================================================
# STEP 4: CHUNKING WITH OVERLAP
# =============================================================================
def chunk_text(sentences: list, source_name: str,
               chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> list:
    """
    Group sentences into overlapping chunks suitable for embedding.
    If an individual sentence or table block exceeds chunk_size, it is
    subdivided cleanly.
    """
    # Subdivide any individual oversized sentence blocks
    flattened_sentences = []
    for s in sentences:
        words = s.split()
        if len(words) > chunk_size:
            # Subdivide words into chunk_size pieces
            for i in range(0, len(words), chunk_size - overlap):
                sub_words = words[i:i + chunk_size]
                flattened_sentences.append(' '.join(sub_words))
        else:
            flattened_sentences.append(s)

    chunks = []
    current_chunk_words = []
    current_word_count = 0
    chunk_id = 0

    for sentence in flattened_sentences:
        words = sentence.split()
        word_count = len(words)

        # If adding this sentence exceeds chunk_size, save current chunk
        if current_word_count + word_count > chunk_size and current_chunk_words:
            c_text = ' '.join(current_chunk_words)
            chunks.append({
                "chunk_id": f"{source_name}_chunk_{chunk_id:04d}",
                "source": source_name,
                "text": c_text,
                "word_count": current_word_count
            })
            chunk_id += 1

            # Keep overlap words for next chunk
            overlap_words = current_chunk_words[-overlap:] if overlap > 0 else []
            current_chunk_words = overlap_words
            current_word_count = len(overlap_words)

        current_chunk_words.extend(words)
        current_word_count += word_count

    # Don't forget the last chunk
    if current_chunk_words:
        c_text = ' '.join(current_chunk_words)
        chunks.append({
            "chunk_id": f"{source_name}_chunk_{chunk_id:04d}",
            "source": source_name,
            "text": c_text,
            "word_count": current_word_count
        })

    return chunks


# =============================================================================
# BEFORE/AFTER DISPLAY
# =============================================================================
def show_before_after(stage: str, before: str, after: str, max_chars: int = 500):
    """Print a side-by-side comparison of text before and after a processing step."""
    print(f"\n{'─' * 60}")
    print(f"📋 {stage}")
    print(f"{'─' * 60}")
    print(f"\n🔴 BEFORE ({len(before):,} chars):")
    print(f"   {before[:max_chars]}{'...' if len(before) > max_chars else ''}")
    print(f"\n🟢 AFTER ({len(after):,} chars):")
    print(f"   {after[:max_chars]}{'...' if len(after) > max_chars else ''}")
    print(f"\n   ➡️  Reduced by {len(before) - len(after):,} characters "
          f"({(1 - len(after)/max(len(before),1))*100:.1f}% reduction)")


# =============================================================================
# MAIN PIPELINE
# =============================================================================
def process_document(filepath: str, source_name: str) -> list:
    """
    Run the full preprocessing pipeline on a single document.
    Returns a list of processed chunks.
    """
    print(f"\n{'=' * 60}")
    print(f"📖 Processing: {source_name}")
    print(f"{'=' * 60}")

    # Load raw text
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    print(f"\n📊 Raw text: {len(raw_text):,} characters, ~{len(raw_text.split()):,} words")

    # Step 1: Noise Removal
    cleaned = remove_noise(raw_text)
    show_before_after("Step 1: Noise Removal", raw_text, cleaned)

    # Step 2: Normalization
    normalized = normalize_text(cleaned)
    show_before_after("Step 2: Text Normalization", cleaned, normalized)

    # Step 3: Sentence Tokenization
    sentences = tokenize_sentences(normalized)
    print(f"\n{'─' * 60}")
    print(f"📋 Step 3: Sentence Tokenization")
    print(f"{'─' * 60}")
    print(f"   Split into {len(sentences)} sentences")
    print(f"   First 3 sentences:")
    for i, sent in enumerate(sentences[:3]):
        print(f"   [{i+1}] {sent[:120]}{'...' if len(sent) > 120 else ''}")

    # Step 4: Chunking
    chunks = chunk_text(sentences, source_name)
    print(f"\n{'─' * 60}")
    print(f"📋 Step 4: Chunking (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"{'─' * 60}")
    print(f"   Created {len(chunks)} chunks")
    if chunks:
        avg_words = sum(c['word_count'] for c in chunks) / len(chunks)
        print(f"   Average chunk size: {avg_words:.0f} words")
        print(f"\n   Sample chunk [{chunks[0]['chunk_id']}]:")
        print(f"   {chunks[0]['text'][:200]}...")

    return chunks


def main():
    print("=" * 60)
    print("TPoliCynav — Text Preprocessing Pipeline")
    print("Checkpoint 1, Deliverable 3")
    print("=" * 60)

    all_chunks = []

    # Process all raw text files
    if not os.path.exists(RAW_DATA_DIR):
        print(f"❌ Raw data directory not found: {RAW_DATA_DIR}")
        print("   Run extract_pdf.py first!")
        return

    raw_files = sorted([f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.txt')])
    if not raw_files:
        print(f"❌ No .txt files found in {RAW_DATA_DIR}")
        print("   Run extract_pdf.py first!")
        return

    print(f"\n📂 Found {len(raw_files)} raw documents to process:")
    for f in raw_files:
        print(f"   - {f}")

    for filename in raw_files:
        filepath = os.path.join(RAW_DATA_DIR, filename)
        source_name = os.path.splitext(filename)[0]
        chunks = process_document(filepath, source_name)
        all_chunks.extend(chunks)

    # Save all chunks to JSON
    output_path = os.path.join(PROCESSED_DIR, "chunks.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    # Final Summary
    print(f"\n{'=' * 60}")
    print("PREPROCESSING SUMMARY")
    print(f"{'=' * 60}")
    print(f"  📂 Documents processed: {len(raw_files)}")
    print(f"  🧩 Total chunks created: {len(all_chunks)}")
    print(f"  📊 Average words/chunk: {sum(c['word_count'] for c in all_chunks) / max(len(all_chunks),1):.0f}")
    print(f"  💾 Saved to: {output_path}")

    # Source breakdown
    print(f"\n  Chunks per source:")
    sources = {}
    for c in all_chunks:
        sources[c['source']] = sources.get(c['source'], 0) + 1
    for source, count in sources.items():
        print(f"    - {source}: {count} chunks")

    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
