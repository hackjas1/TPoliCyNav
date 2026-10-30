"""
=============================================================================
TPoliCynav — Pinecone Vector Indexing Script
Checkpoint 2: Vector Indexing & Cloud Deployment
=============================================================================
Connects to Pinecone, creates a serverless vector index with dimension=384,
and upserts preprocessed chunks along with their BGE dense vector embeddings.

Usage:
    python scripts/upload_to_pinecone.py
=============================================================================
"""

import os
import sys
import json
import time
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Force UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tpolicynav")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
METADATA_PATH = os.path.join(PROCESSED_DIR, "chunks_with_embeddings.json")

EMBEDDING_DIM = 384
METRIC = "cosine"
BATCH_SIZE = 50


def main():
    print("=" * 60)
    print("TPoliCynav — Pinecone Vector Indexing")
    print("Checkpoint 2: Cloud Vector Store Integration")
    print("=" * 60)

    if not PINECONE_API_KEY or "your_pinecone" in PINECONE_API_KEY:
        print("❌ Error: Valid PINECONE_API_KEY not found in .env file.")
        return

    # 1. Load Embeddings and Metadata
    if not os.path.exists(EMBEDDINGS_PATH) or not os.path.exists(METADATA_PATH):
        print("❌ Embeddings or metadata missing! Please run generate_embeddings.py first.")
        return

    embeddings = np.load(EMBEDDINGS_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"📊 Loaded {len(chunks)} chunks and embeddings of shape {embeddings.shape}")

    # 2. Initialize Pinecone Client
    print(f"\n🌲 Connecting to Pinecone...")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # 3. Create Index if it doesn't exist
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    print(f"🔍 Existing indexes: {existing_indexes}")

    if INDEX_NAME not in existing_indexes:
        print(f"📦 Creating new Serverless Index: '{INDEX_NAME}' (dim={EMBEDDING_DIM}, metric={METRIC})...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIM,
            metric=METRIC,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # Wait for index to be ready
        print("⏳ Waiting for index initialization...")
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(2)
        print(f"✅ Index '{INDEX_NAME}' is active and ready.")
    else:
        print(f"ℹ️ Index '{INDEX_NAME}' already exists.")

    index = pc.Index(INDEX_NAME)

    # 4. Prepare Vector Records for Upsert
    print(f"\n⚡ Formatting {len(chunks)} vectors with metadata payloads...")
    vectors_to_upsert = []
    for i, chunk in enumerate(chunks):
        vec_id = chunk["chunk_id"]
        values = embeddings[i].tolist()
        metadata = {
            "source": chunk["source"],
            "word_count": chunk.get("word_count", 0),
            "text": chunk["text"][:1000]  # Pinecone metadata size limit preservation
        }
        vectors_to_upsert.append({
            "id": vec_id,
            "values": values,
            "metadata": metadata
        })

    # 5. Batch Upsert to Pinecone
    print(f"🚀 Upserting vectors in batches of {BATCH_SIZE}...")
    for start in range(0, len(vectors_to_upsert), BATCH_SIZE):
        end = min(start + BATCH_SIZE, len(vectors_to_upsert))
        batch = vectors_to_upsert[start:end]
        index.upsert(vectors=batch)
        print(f"   ⬆️  Upserted batch {start+1} - {end} of {len(vectors_to_upsert)}")

    # 6. Verify Index Statistics
    time.sleep(3)
    stats = index.describe_index_stats()
    print("\n" + "=" * 60)
    print("PINECONE INDEXING SUMMARY")
    print("=" * 60)
    print(f"  🌲 Index Name: {INDEX_NAME}")
    print(f"  📐 Dimension: {EMBEDDING_DIM}")
    print(f"  📊 Total Vector Count: {stats.get('total_vector_count', 'N/A')}")
    print(f"  🌐 Namespaces: {stats.get('namespaces', {})}")
    print("=" * 60)
    print("✅ Pinecone index populated successfully!")


if __name__ == "__main__":
    main()
