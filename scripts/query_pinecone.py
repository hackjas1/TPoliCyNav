"""
=============================================================================
TPoliCynav — Pinecone Semantic Query Demo
Checkpoint 2: Retrieval Testing & Similarity Search
=============================================================================
Encodes natural language student queries and queries the Pinecone vector index
to retrieve top-k semantically relevant policy chunks.

Usage:
    python scripts/query_pinecone.py
=============================================================================
"""

import os
import sys
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Force UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tpolicynav")
MODEL_NAME = "BAAI/bge-small-en-v1.5"


def main():
    print("=" * 60)
    print("TPoliCynav — Pinecone Semantic Search Demo")
    print("Checkpoint 2: Vector Retrieval Evaluation")
    print("=" * 60)

    if not PINECONE_API_KEY:
        print("❌ Error: PINECONE_API_KEY not configured in .env.")
        return

    # 1. Connect to Pinecone and Load Model
    print("🤖 Loading query encoder (BAAI/bge-small-en-v1.5)...")
    model = SentenceTransformer(MODEL_NAME)
    
    print("🌲 Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)

    # 2. Benchmark Queries
    benchmark_queries = [
        "Are ripped jeans allowed during exams or class?",
        "What are the curfew hours and rules for boarding houses near TPC?",
        "What is the required GWA to qualify for the GSIS STEM scholarship?",
        "What is the penalty for alcohol sale near the campus?",
        "How do I apply for graduation clearance at TPC?"
    ]

    for q in benchmark_queries:
        print("\n" + "─" * 60)
        print(f"❓ Student Query: \"{q}\"")
        print("─" * 60)

        # Encode query
        query_vec = model.encode(q, normalize_embeddings=True).tolist()

        # Query Pinecone
        res = index.query(
            vector=query_vec,
            top_k=3,
            include_metadata=True
        )

        for rank, match in enumerate(res.get("matches", []), 1):
            score = match.get("score", 0.0)
            meta = match.get("metadata", {})
            source = meta.get("source", "Unknown")
            text = meta.get("text", "").strip().replace("\n", " ")
            print(f"\n   🏆 Rank {rank} | Similarity Score: {score:.4f}")
            print(f"   📄 Source: {source}")
            print(f"   📝 Match: {text[:220]}...")

    print("\n" + "=" * 60)
    print("✅ Pinecone Retrieval Benchmark Complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
