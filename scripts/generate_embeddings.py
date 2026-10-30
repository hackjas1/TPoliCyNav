"""
=============================================================================
TPoliCynav — Embedding Generation Demo
Checkpoint 1, Deliverable 4: Embedding Generation
=============================================================================
Converts preprocessed text chunks into dense vector embeddings using
BAAI/bge-small-en-v1.5 and demonstrates semantic similarity search.

Model Choice: BAAI/bge-small-en-v1.5
  - Dimensions: 384
  - Size: ~130MB (small footprint, fast inference)
  - Performance: Top-tier on MTEB retrieval benchmarks for its size
  - License: MIT (free for commercial use)
  - Why this model: Optimized specifically for retrieval tasks, making it
    ideal for RAG pipelines. Its small size allows local inference on
    consumer hardware while maintaining strong semantic understanding.

Usage:
    python scripts/generate_embeddings.py
=============================================================================
"""

import os
import sys
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
METADATA_PATH = os.path.join(PROCESSED_DIR, "chunks_with_embeddings.json")

MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIM = 384


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def main():
    print("=" * 60)
    print("TPoliCynav — Embedding Generation Demo")
    print("Checkpoint 1, Deliverable 4")
    print("=" * 60)

    # --- Load Chunks ---
    if not os.path.exists(CHUNKS_PATH):
        print(f"❌ Chunks file not found: {CHUNKS_PATH}")
        print("   Run preprocess.py first!")
        return

    with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    print(f"\n📂 Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    # --- Load Model ---
    print(f"\n🤖 Loading embedding model: {MODEL_NAME}")
    print(f"   This downloads ~130MB on first run...")
    model = SentenceTransformer(MODEL_NAME)
    print(f"   ✅ Model loaded successfully!")
    print(f"   📐 Embedding dimensions: {EMBEDDING_DIM}")
    print(f"   📏 Max sequence length: {model.max_seq_length}")

    # --- Generate Embeddings ---
    print(f"\n⚡ Generating embeddings for {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]

    # BGE models recommend prepending "Represent this sentence: " for retrieval
    # but bge-small-en-v1.5 works well without it too
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,  # L2 normalize for cosine similarity
        batch_size=32
    )

    embeddings_np = np.array(embeddings)
    print(f"\n   ✅ Embeddings generated!")
    print(f"   📐 Shape: {embeddings_np.shape}")
    print(f"   📊 Dtype: {embeddings_np.dtype}")
    print(f"   📏 Sample vector (first 10 dims of chunk 0):")
    print(f"      {embeddings_np[0][:10]}")

    # --- Save Embeddings ---
    np.save(EMBEDDINGS_PATH, embeddings_np)
    print(f"\n💾 Saved embeddings to: {EMBEDDINGS_PATH}")

    # Save enriched chunks with embedding info
    for i, chunk in enumerate(chunks):
        chunk["embedding_index"] = i
        chunk["embedding_dim"] = EMBEDDING_DIM
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved enriched metadata to: {METADATA_PATH}")

    # =========================================================================
    # SEMANTIC SIMILARITY DEMO
    # =========================================================================
    print(f"\n{'=' * 60}")
    print("🔍 SEMANTIC SIMILARITY DEMO")
    print(f"{'=' * 60}")
    print("Testing if embeddings capture semantic meaning by querying")
    print("with natural language and finding the most relevant chunks.\n")

    test_queries = [
        "What happens if I wear torn pants to school?",
        "What are the curfew hours for boarding houses?",
        "How do I apply for a scholarship?",
        "What are the requirements for graduation?",
        "Can I drink alcohol near the campus?",
    ]

    for query in test_queries:
        print(f"\n{'─' * 60}")
        print(f"❓ Query: \"{query}\"")
        print(f"{'─' * 60}")

        # Encode the query
        query_embedding = model.encode(
            query, normalize_embeddings=True
        )

        # Compute cosine similarities with all chunks
        similarities = np.dot(embeddings_np, query_embedding)

        # Get top 3 results
        top_indices = np.argsort(similarities)[::-1][:3]

        for rank, idx in enumerate(top_indices, 1):
            chunk = chunks[idx]
            sim = similarities[idx]
            print(f"\n   🏆 Rank {rank} (similarity: {sim:.4f})")
            print(f"   📄 Source: {chunk['source']}")
            print(f"   📝 Text: {chunk['text'][:200]}...")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print(f"\n{'=' * 60}")
    print("EMBEDDING GENERATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  🤖 Model: {MODEL_NAME}")
    print(f"  📐 Dimensions: {EMBEDDING_DIM}")
    print(f"  🧩 Chunks embedded: {len(chunks)}")
    print(f"  📊 Embedding matrix shape: {embeddings_np.shape}")
    print(f"  💾 Files saved:")
    print(f"     - {EMBEDDINGS_PATH}")
    print(f"     - {METADATA_PATH}")
    print(f"{'=' * 60}")
    print(f"\n✅ Ready for Checkpoint 2: Upload to Pinecone!")


if __name__ == "__main__":
    main()
