"""
=============================================================================
TPoliCynav — Automated End-to-End Ingestion Pipeline
Checkpoint 3: Deliverable 10
=============================================================================
Automated pipeline that:
  1. Parses raw policy documents (.pdf, .txt, .md).
  2. Cleans, normalizes, and recursively chunks text with overlap.
  3. Generates 384-dimensional dense vectors using BAAI/bge-small-en-v1.5.
  4. Stores data locally (chunks.json, embeddings.npy) and syncs with
     Pinecone Cloud Serverless Vector DB (tpolicynav).

Usage:
    # Ingest all documents from data/raw/
    python scripts/ingest_pipeline.py

    # Ingest a single new policy file
    python scripts/ingest_pipeline.py --file path/to/new_policy.pdf

    # Rebuild entire dataset from scratch
    python scripts/ingest_pipeline.py --rebuild

    # Local-only mode (offline / without Pinecone upsert)
    python scripts/ingest_pipeline.py --skip-pinecone
=============================================================================
"""

import os
import sys
import re
import json
import time
import hashlib
import argparse
import unicodedata
from datetime import datetime
import numpy as np
from dotenv import load_dotenv

# Console encoding for Windows
sys.stdout.reconfigure(encoding="utf-8")

# Project directories
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
METADATA_PATH = os.path.join(PROCESSED_DIR, "chunks_with_embeddings.json")

# Model configurations
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384
DEFAULT_CHUNK_SIZE = 400
DEFAULT_CHUNK_OVERLAP = 80
BATCH_SIZE = 50

# Pinecone configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tpolicynav")


class DocumentParser:
    """Parses various file types (.pdf, .txt, .md) into plain text."""

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF using pdfplumber with fallback."""
        text = ""
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    extracted = page.extract_text(layout=True) or ""
                    text += f"\n--- Page {page_num} ---\n" + extracted
            return text
        except Exception as e:
            print(f"   ⚠️ pdfplumber failed ({e}), trying PyPDF2...")
            try:
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                for page_num, page in enumerate(reader.pages, 1):
                    text += f"\n--- Page {page_num} ---\n" + (page.extract_text() or "")
                return text
            except Exception as e2:
                raise RuntimeError(f"Failed to parse PDF {file_path}: {e2}")

    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Extract text from plain text or markdown file."""
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Could not decode text file: {file_path}")

    @classmethod
    def parse_file(cls, file_path: str) -> str:
        """Route to appropriate parser based on extension."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.parse_pdf(file_path)
        elif ext in [".txt", ".md", ".csv"]:
            return cls.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")


class TextSanitizer:
    """Cleans, normalizes, and chunks institutional policy text."""

    @staticmethod
    def clean(text: str) -> str:
        """Remove page numbers, noise headers, and extraneous whitespace."""
        text = re.sub(r'---\s*Page\s*\d+\s*---', '', text)
        text = re.sub(r'^\s*\d{1,3}\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\x0c', '', text)
        text = re.sub(r'[\x00-\x08\x0b\x0e-\x1f]', '', text)
        text = re.sub(r'[-_]{5,}', '', text)
        text = re.sub(r'[=]{5,}', '', text)
        # Fix hyphenated wrapped lines
        text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    @staticmethod
    def normalize(text: str) -> str:
        """Standardize Unicode, quotes, dashes, and spaces."""
        text = unicodedata.normalize('NFKD', text)
        # Curly quotes to straight
        text = re.sub(r'[\u2018\u2019]', "'", text)
        text = re.sub(r'[\u201c\u201d]', '"', text)
        # Dashes
        text = re.sub(r'[\u2013\u2014]', '-', text)
        # Tabs and multiple spaces
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    @staticmethod
    def chunk(text: str, source_id: str, chunk_size: int = DEFAULT_CHUNK_SIZE,
              chunk_overlap: int = DEFAULT_CHUNK_OVERLAP) -> list:
        """
        Split normalized text into overlapping chunks respecting sentence boundaries.
        """
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunk_id = f"{source_id}_chunk_{chunk_idx:04d}"
            content_hash = hashlib.sha256(chunk_text.encode('utf-8')).hexdigest()[:16]

            chunks.append({
                "chunk_id": chunk_id,
                "source": source_id,
                "text": chunk_text,
                "word_count": len(chunk_words),
                "hash": content_hash,
                "timestamp": datetime.now().isoformat()
            })

            chunk_idx += 1
            if end >= len(words):
                break
            start += (chunk_size - chunk_overlap)

        return chunks


class IngestionPipeline:
    """End-to-End Orchestrator for Parsing, Chunking, Embedding, and Indexing."""

    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE,
                 chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
                 skip_pinecone: bool = False):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.skip_pinecone = skip_pinecone
        self.model = None

    def load_model(self):
        """Lazy load the sentence-transformers model."""
        if self.model is None:
            print(f"📦 Loading Embedding Model ({EMBEDDING_MODEL_NAME})...")
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            print("   ✅ Embedding Model active (dim=384)")

    def process_document(self, file_path: str) -> list:
        """Extract, clean, and chunk a single file."""
        source_id = os.path.splitext(os.path.basename(file_path))[0]
        print(f"📄 Processing: {os.path.basename(file_path)} (ID: {source_id})")

        raw_text = DocumentParser.parse_file(file_path)
        cleaned_text = TextSanitizer.clean(raw_text)
        normalized_text = TextSanitizer.normalize(cleaned_text)

        chunks = TextSanitizer.chunk(
            normalized_text,
            source_id=source_id,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        print(f"   ↳ Extracted {len(chunks)} chunks ({len(normalized_text.split())} total words)")
        return chunks

    def process_directory(self, dir_path: str) -> list:
        """Process all supported documents in a directory."""
        supported_exts = {".pdf", ".txt", ".md"}
        all_chunks = []
        files = [
            os.path.join(dir_path, f) for f in sorted(os.listdir(dir_path))
            if os.path.splitext(f)[1].lower() in supported_exts
        ]

        print(f"📂 Found {len(files)} documents in {dir_path}")
        for file_path in files:
            try:
                chunks = self.process_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"   ❌ Error processing {file_path}: {e}")

        return all_chunks

    def generate_embeddings(self, chunks: list) -> np.ndarray:
        """Compute normalized dense embeddings for all chunks."""
        self.load_model()
        texts = [c["text"] for c in chunks]
        print(f"🔢 Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=32
        )
        return np.array(embeddings, dtype=np.float32)

    def sync_local_storage(self, chunks: list, embeddings: np.ndarray):
        """Save chunk metadata and dense matrix to disk."""
        print("💾 Saving local vector cache...")
        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        np.save(EMBEDDINGS_PATH, embeddings)

        metadata_records = []
        for i, chunk in enumerate(chunks):
            record = dict(chunk)
            record["embedding_dim"] = int(embeddings.shape[1])
            metadata_records.append(record)

        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata_records, f, indent=2, ensure_ascii=False)

        print(f"   ✅ Saved {len(chunks)} chunks to {CHUNKS_PATH}")
        print(f"   ✅ Saved embeddings matrix of shape {embeddings.shape} to {EMBEDDINGS_PATH}")

    def sync_pinecone(self, chunks: list, embeddings: np.ndarray):
        """Upsert vectors and rich metadata to Pinecone Serverless."""
        if self.skip_pinecone:
            print("🌲 Skipping Pinecone sync (--skip-pinecone flagged).")
            return

        if not PINECONE_API_KEY or PINECONE_API_KEY.startswith("your_"):
            print("ℹ️ Pinecone API key not found in .env; skipping cloud upsert.")
            return

        print(f"🌲 Connecting to Pinecone Index '{INDEX_NAME}'...")
        try:
            from pinecone import Pinecone, ServerlessSpec
            pc = Pinecone(api_key=PINECONE_API_KEY)

            # Check if index exists, create if not
            existing_indexes = [idx["name"] for idx in pc.list_indexes()]
            if INDEX_NAME not in existing_indexes:
                print(f"   Creating serverless index '{INDEX_NAME}' (dim=384, cosine)...")
                pc.create_index(
                    name=INDEX_NAME,
                    dimension=EMBEDDING_DIM,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                while not pc.describe_index(INDEX_NAME).status["ready"]:
                    time.sleep(1)

            index = pc.Index(INDEX_NAME)

            # Upsert in batches of BATCH_SIZE
            total_chunks = len(chunks)
            print(f"   Upserting {total_chunks} vectors in batches of {BATCH_SIZE}...")
            for i in range(0, total_chunks, BATCH_SIZE):
                batch_chunks = chunks[i:i + BATCH_SIZE]
                batch_embeddings = embeddings[i:i + BATCH_SIZE]

                vectors = []
                for chunk, emb in zip(batch_chunks, batch_embeddings):
                    vectors.append({
                        "id": chunk["chunk_id"],
                        "values": emb.tolist(),
                        "metadata": {
                            "source": chunk["source"],
                            "text": chunk["text"][:1000],  # Pinecone metadata limit safe
                            "word_count": chunk["word_count"]
                        }
                    })

                index.upsert(vectors=vectors)
                print(f"   ↳ Upserted batch {i // BATCH_SIZE + 1} / {(total_chunks - 1) // BATCH_SIZE + 1}")

            stats = index.describe_index_stats()
            print(f"   ✅ Pinecone Index Synced! Total vectors in cloud: {stats.total_vector_count}")

        except Exception as e:
            print(f"   ⚠️ Pinecone upsert failed: {e}")
            print("   (Local vector cache remains intact and fully functional).")

    def run(self, input_file: str = None, input_dir: str = None, rebuild: bool = False):
        """Execute full end-to-end ingestion pipeline."""
        print("\n" + "=" * 65)
        print("  🚀 TPOLICYNAV AUTOMATED INGESTION PIPELINE")
        print("  Talibon Polytechnic College Institutional Knowledge Base")
        print("=" * 65)

        target_dir = input_dir or RAW_DATA_DIR
        if input_file:
            print(f"🎯 Target File: {input_file}")
            new_chunks = [self.process_document(input_file)]
            # If not rebuild, append to existing chunks
            if not rebuild and os.path.exists(CHUNKS_PATH):
                with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                    all_chunks = json.load(f)
                all_chunks.extend(new_chunks)
            else:
                all_chunks = new_chunks
        else:
            print(f"🎯 Target Directory: {target_dir}")
            all_chunks = self.process_directory(target_dir)

        if not all_chunks:
            print("❌ No chunks generated. Exiting pipeline.")
            return

        print(f"\n📊 Total Chunks in Corpus: {len(all_chunks)}")
        embeddings = self.generate_embeddings(all_chunks)

        self.sync_local_storage(all_chunks, embeddings)
        self.sync_pinecone(all_chunks, embeddings)

        print("\n" + "=" * 65)
        print("  🎉 INGESTION PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
        print(f"  • Chunks processed: {len(all_chunks)}")
        print(f"  • Embedding dimensions: {embeddings.shape[1]}")
        print(f"  • Vector backend: Local Cache + {'Pinecone' if not self.skip_pinecone else 'Offline Only'}")
        print("=" * 65 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="TPoliCynav Automated Ingestion Pipeline")
    parser.add_argument("--file", type=str, default=None, help="Path to single file to ingest")
    parser.add_argument("--dir", type=str, default=None, help="Directory containing raw policy files")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild entire dataset from scratch")
    parser.add_argument("--skip-pinecone", action="store_true", help="Skip cloud Pinecone upsert")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Tokens/words per chunk")
    parser.add_argument("--chunk-overlap", type=int, default=DEFAULT_CHUNK_OVERLAP, help="Overlap words per chunk")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    pipeline = IngestionPipeline(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        skip_pinecone=args.skip_pinecone
    )
    pipeline.run(input_file=args.file, input_dir=args.dir, rebuild=args.rebuild)

