"""
=============================================================================
TPoliCynav: The TPC Policy Navigator
Interactive RAG Conversational Agent for Talibon Polytechnic College
=============================================================================
Orchestrates:
  1. User Question Intake
  2. Dense Vector Encoding (BAAI/bge-small-en-v1.5)
  3. Hybrid Vector Retrieval:
     - Cloud Mode: Pinecone Serverless (AWS us-east-1, Cosine Similarity)
     - Offline / Fallback Mode: Local NumPy Matrix (embeddings.npy)
  4. Hybrid Answer Synthesis:
     - Cloud Mode: Hugging Face Generative LLM (Qwen/Qwen2.5-72B-Instruct)
     - Offline / Fallback Mode: Local Precision Policy Extractor
  5. Clean, Direct Answer Synthesis with Official Citations & Guardrails
=============================================================================
"""

import os
import sys
import re
import json
import argparse
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from huggingface_hub import InferenceClient

from prompts.prompt_templates import format_rag_prompt

# Force UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# --- Project Paths & Config ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tpolicynav")
MODEL_NAME = "BAAI/bge-small-en-v1.5"

PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")

HF_TOKEN = os.getenv("HF_TOKEN")
LLM_MODEL = "Qwen/Qwen2.5-72B-Instruct"


class TPoliCynavBot:
    def __init__(self, mode: str = "auto"):
        """
        Initialize TPoliCynavBot in Hybrid Mode.

        Args:
            mode: "auto" (default: prefers cloud with local fallback),
                  "offline" (forces 100% local execution),
                  "online" (strictly requires cloud services).
        """
        self.mode = mode.lower()
        print("\n" + "=" * 65)
        print("  🏛️  INITIALIZING TPoliCynav (TPC POLICY NAVIGATOR)")
        print("=" * 65)

        # 1. Load Local Embedding Model (Runs locally via PyTorch)
        print("📦 [1/3] Loading Embedding Model (BAAI/bge-small-en-v1.5)...")
        self.encoder = SentenceTransformer(MODEL_NAME)
        print("   ✅ Embedding Model active (384-dimensional dense vectors)")

        # 2. Ingest Local Vector Matrix & Chunks (Always available for instant offline fallback)
        self.local_embeddings = None
        self.local_chunks = None
        if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(CHUNKS_PATH):
            try:
                self.local_embeddings = np.load(EMBEDDINGS_PATH)
                with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                    self.local_chunks = json.load(f)
                print(f"   📂 Local vector cache loaded ({len(self.local_chunks)} policy chunks)")
            except Exception as e:
                print(f"   ⚠️ Warning: Could not load local vector cache: {e}")

        # 3. Initialize Vector Database (Pinecone Cloud or Local Fallback)
        self.vector_backend = "local"
        self.pc = None
        self.index = None

        if self.mode == "offline":
            print("🌲 [2/3] Vector Storage: 📴 Offline Mode (Local NumPy Index, Cosine Metric)")
            self.vector_backend = "local"
        else:
            print("🌲 [2/3] Connecting to Pinecone Vector Database...")
            if PINECONE_API_KEY and not PINECONE_API_KEY.startswith("your_"):
                try:
                    self.pc = Pinecone(api_key=PINECONE_API_KEY)
                    self.index = self.pc.Index(INDEX_NAME)
                    # Quick connectivity check
                    _ = self.pc.describe_index(INDEX_NAME)
                    self.vector_backend = "pinecone"
                    print(f"   ✅ Connected to Pinecone Cloud Index '{INDEX_NAME}' (AWS us-east-1)")
                except Exception as e:
                    if self.mode == "online":
                        raise ConnectionError(f"Failed to connect to Pinecone in online mode: {e}")
                    print(f"   ⚠️ Pinecone Cloud unreachable ({e}).")
                    print("   🔄 Seamlessly activated Local Vector Storage (119 chunks, Cosine Similarity)")
                    self.vector_backend = "local"
            else:
                print("   ℹ️ No Pinecone API key configured in .env.")
                print("   🔄 Seamlessly activated Local Vector Storage (119 chunks, Cosine Similarity)")
                self.vector_backend = "local"

        # 4. Initialize Generative LLM Client (Cloud Hugging Face or Local Extractor)
        self.llm_client = None
        if self.mode == "offline":
            print("🤖 [3/3] Generator: 📴 Local Precision Policy Extractor (100% Offline)")
        else:
            print(f"🤖 [3/3] Initializing Generative LLM ({LLM_MODEL})...")
            if HF_TOKEN and not HF_TOKEN.startswith("your_"):
                try:
                    self.llm_client = InferenceClient(token=HF_TOKEN)
                    print("   ✅ Generative Cloud LLM is ready.")
                except Exception as e:
                    print(f"   ⚠️ Could not initialize Cloud LLM: {e}")
                    print("   🔄 Local Precision Policy Extractor will be used as fallback.")
            else:
                print("   ℹ️ No HF_TOKEN found. Using Local Precision Policy Extractor.")

        # Status Summary Banner
        print("=" * 65)
        if self.vector_backend == "pinecone" and self.llm_client:
            print("  🌐 STATUS: ONLINE MODE (Pinecone Cloud + Qwen-72B LLM)")
        elif self.vector_backend == "pinecone":
            print("  🌐 STATUS: HYBRID MODE (Pinecone Cloud + Local Policy Extractor)")
        else:
            print("  📴 STATUS: OFFLINE / LOCAL MODE (Local NumPy Vector Search + Local Extractor)")
        print("  ✅ TPoliCynav is ready for policy inquiries!")
        print("=" * 65 + "\n")

    def retrieve_context(self, query: str, top_k: int = 4) -> list:
        """
        Embed the query and retrieve top_k policy chunks using either
        Pinecone Cloud or Local NumPy In-Memory search.
        """
        query_vec = self.encoder.encode(query, normalize_embeddings=True)

        # Attempt Cloud Retrieval if configured
        if self.vector_backend == "pinecone" and self.index:
            try:
                res = self.index.query(
                    vector=query_vec.tolist(),
                    top_k=top_k,
                    include_metadata=True
                )
                retrieved = []
                for match in res.get("matches", []):
                    retrieved.append({
                        "id": match.get("id"),
                        "score": match.get("score", 0.0),
                        "source": match.get("metadata", {}).get("source", "Official TPC Policy"),
                        "text": match.get("metadata", {}).get("text", "")
                    })
                return retrieved
            except Exception as e:
                print(f"   ⚠️ Cloud query failed ({e}). Falling back to Local Vector Search...")

        # Local In-Memory Cosine Similarity Retrieval
        if self.local_embeddings is not None and self.local_chunks is not None:
            # Normalized dot product is identical to Cosine Similarity
            similarities = np.dot(self.local_embeddings, query_vec)
            top_indices = np.argsort(similarities)[::-1][:top_k]
            retrieved = []
            for idx in top_indices:
                chunk = self.local_chunks[idx]
                retrieved.append({
                    "id": chunk.get("chunk_id", f"chunk_{idx:04d}"),
                    "score": float(similarities[idx]),
                    "source": chunk.get("source", "Official TPC Policy"),
                    "text": chunk.get("text", "")
                })
            return retrieved

        return []

    def extract_relevant_content(self, query: str, chunks: list) -> tuple:
        """
        Offline semantic extraction of relevant policy statements from retrieved chunks.
        Returns: (formatted_answer_string, list_of_cited_sources)
        """
        source_labels = {
            "admissions_guidelines": "TPC Admissions Guidelines & Degree Offerings",
            "tpc_student_handbook": "TPC Student Handbook v.04",
            "tpc_uniform_and_dress_code_guide": "TPC School Uniform & Dress Code Policy",
            "municipal_ordinance_127": "Talibon Municipal Ordinance No. 127",
            "pnp_tpc_security": "PNP-TPC Joint Security Collaboration Guidelines",
            "ched_free_education": "CHED Free Higher Education Guidelines (RA 10931)",
            "gsis_stem_subsidy": "GSIS Subsidy for STEM (GSSP) Guidelines"
        }

        # 1. Check if user is asking about courses / degree programs
        is_course_query = bool(re.search(r'course|program|degree|offer|bachelor|curriculum|major', query, re.IGNORECASE))
        for chunk in chunks:
            raw_text = chunk["text"]
            if "DEGREE PROGRAMS" in raw_text.upper() or "COURSES AND PROGRAMS" in raw_text.upper() or (is_course_query and "BACHELOR OF" in raw_text.upper()):
                programs = re.findall(r'\d+\.\s+([A-Za-z\s\(\)\-]+?)(?=\s+\d+\.|\s+All degree|\s+TALIBON|\s+TPC|$)', raw_text)
                if len(programs) >= 4:
                    prog_lines = [f"{i}. {p.strip()}" for i, p in enumerate(programs, 1)]
                    ans = (
                        f"**Talibon Polytechnic College (TPC) officially offers the following 7 undergraduate degree programs:**\n\n"
                        + "\n".join(prog_lines)
                        + "\n\n*(Covered under CHED RA 10931 Free Higher Education / Universal Access to Quality Tertiary Education Act.)*"
                    )
                    return ans, [source_labels.get(chunk["source"], "TPC Student Handbook v.04")]

        # 2. Extract precision sentences for general policy queries
        candidate_sentences = []
        for chunk in chunks:
            raw_text = chunk["text"]
            splits = re.split(r'(?<=[.!?])\s+|(?<=\d\.)\s+|(?<=\-)\s+|SECTION\s+\d+\.\s*', raw_text)
            for s in splits:
                s_clean = s.strip()
                if len(s_clean.split()) >= 4 and not s_clean.startswith("===") and not s_clean.startswith("AN ORDINANCE") and not s_clean.isupper():
                    candidate_sentences.append({
                        "text": s_clean,
                        "source": chunk["source"]
                    })

        if not candidate_sentences:
            top_chunk = chunks[0]
            ans = f"**{source_labels.get(top_chunk['source'], top_chunk['source'])}:**\n\n• " + top_chunk["text"][:250] + "..."
            return ans, [source_labels.get(top_chunk["source"], top_chunk["source"])]

        # Semantic ranking of individual sentences
        query_vec = self.encoder.encode(query, normalize_embeddings=True)
        texts = [s["text"] for s in candidate_sentences]
        vecs = self.encoder.encode(texts, normalize_embeddings=True)

        similarities = np.dot(vecs, query_vec)
        ranked_indices = np.argsort(similarities)[::-1]

        selected = []
        seen = set()
        top_score = similarities[ranked_indices[0]] if len(ranked_indices) > 0 else 0.0

        for idx in ranked_indices:
            sent_text = candidate_sentences[idx]["text"]
            score = similarities[idx]
            if score < 0.50 or (selected and score < (top_score - 0.12)):
                continue

            norm_key = sent_text.lower()[:35]
            if norm_key not in seen:
                seen.add(norm_key)
                selected.append({
                    "text": sent_text,
                    "source": candidate_sentences[idx]["source"],
                    "score": float(score)
                })
            if len(selected) >= 2:
                break

        bullet_points = []
        cited_sources = []
        for item in selected:
            t = item["text"]
            t = re.sub(r'^[•\-\d\.\s]+', '', t).strip()
            bullet_points.append(f"• {t}")
            cited_sources.append(source_labels.get(item["source"], item["source"]))

        top_source = cited_sources[0] if cited_sources else source_labels.get(chunks[0]["source"], chunks[0]["source"])
        answer_text = f"**{top_source}:**\n\n" + "\n\n".join(bullet_points)
        return answer_text, list(dict.fromkeys(cited_sources))

    def generate_response(self, user_query: str, retrieved_chunks: list) -> dict:
        """
        Synthesize concise, grounded response using Generative LLM with automatic offline fallback.
        """
        max_similarity = max([c["score"] for c in retrieved_chunks]) if retrieved_chunks else 0.0

        # Strict scope containment filter: refuse off-topic questions
        if max_similarity < 0.50:
            return {
                "answer": (
                    "I cannot find specific information regarding your inquiry in the official "
                    "Talibon Polytechnic College (TPC) policies and guidelines.\n\n"
                    "Please consult the **TPC Registrar's Office** or the **Office of Student Affairs and Services (OSAS)** "
                    "for official guidance regarding off-policy matters."
                ),
                "sources": [],
                "confidence": max_similarity,
                "model_used": "Scope Containment Guardrail"
            }

        # 1. Try Generative LLM via Hugging Face Inference API if online
        if self.llm_client:
            try:
                formatted_prompt = format_rag_prompt(user_query, retrieved_chunks)
                response = self.llm_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are TPoliCynav, the institutional policy assistant for Talibon Polytechnic College. "
                                "Base your answer strictly on the provided institutional context. "
                                "Be concise, clear, and always cite official documents."
                            )
                        },
                        {"role": "user", "content": formatted_prompt}
                    ],
                    model=LLM_MODEL,
                    max_tokens=400,
                    temperature=0.1
                )
                generated_answer = response.choices[0].message.content.strip()
                cited = list(dict.fromkeys([c.get("source", "Official TPC Policy") for c in retrieved_chunks]))

                return {
                    "answer": generated_answer,
                    "sources": cited,
                    "confidence": max_similarity,
                    "model_used": f"Generative Cloud LLM ({LLM_MODEL})"
                }
            except Exception as e:
                # Fall through to local extractor on API error or rate limit
                pass

        # 2. Local Semantic Extractive Engine (100% Offline)
        answer_text, cited_sources = self.extract_relevant_content(user_query, retrieved_chunks)
        model_label = "Precision Policy Extractor (Offline Mode)" if self.mode == "offline" else "Precision Policy Extractor (Local Fallback)"

        return {
            "answer": answer_text,
            "sources": cited_sources,
            "confidence": max_similarity,
            "model_used": model_label
        }

    def chat_loop(self):
        """Interactive Terminal Chat Loop"""
        sample_questions = {
            "1": "What courses and degree programs are officially offered at TPC?",
            "2": "Are ripped jeans or shorts allowed during classes and entrance exams?",
            "3": "What are the curfew hours for boarding houses under Ordinance 127?",
            "4": "What is the minimum GWA required to qualify for the GSIS STEM subsidy?",
            "5": "What is the 500-meter alcohol prohibition zone around TPC?",
            "6": "What is the population of Tokyo, Japan?"
        }

        print("┌" + "─" * 63 + "┐")
        print("│ 💡 SAMPLE INQUIRIES YOU CAN ASK (Type 1-6 or ask anything)     │")
        print("├" + "─" * 63 + "┤")
        print("│ 🟢 IN-SCOPE QUESTIONS:                                        │")
        print("│   [1] What courses and degree programs are offered at TPC?    │")
        print("│   [2] Are ripped jeans or shorts allowed during exams/class?  │")
        print("│   [3] What are the curfew hours for boarding houses?          │")
        print("│   [4] What is the minimum GWA for the GSIS STEM subsidy?      │")
        print("│   [5] What is the 500-meter alcohol prohibition zone?         │")
        print("│                                                               │")
        print("│ 🔴 OUT-OF-SCOPE QUESTION (Tests Hallucination Filter):         │")
        print("│   [6] What is the population of Tokyo, Japan?                 │")
        print("└" + "─" * 63 + "┘")
        print("Commands: 'exit' or 'quit' to end session | 'benchmark' to run all tests\n")

        while True:
            try:
                raw_input = input("🧑‍🎓 Student: ").strip()
                if not raw_input:
                    continue
                if raw_input.lower() in ["exit", "quit"]:
                    print("\n👋 Thank you for using TPoliCynav. Have a great semester at TPC!")
                    break
                if raw_input.lower() == "benchmark":
                    self.run_benchmark()
                    continue

                # Support typing number shortcuts (1-6)
                if raw_input in sample_questions:
                    query = sample_questions[raw_input]
                    print(f"👉 Selected [{raw_input}]: \"{query}\"")
                else:
                    query = raw_input

                print("\n🔍 Searching policy records...")
                retrieved = self.retrieve_context(query, top_k=4)
                result = self.generate_response(query, retrieved)

                print("\n" + "─" * 65)
                print(f"🤖 TPoliCynav:\n{result['answer']}")
                print("─" * 65)
                if result["sources"]:
                    print(f"📚 Source: {', '.join(result['sources'])}")
                print(f"🎯 Match Confidence: {result['confidence']:.4f} | ⚙️ Engine: {result['model_used']}\n")

            except KeyboardInterrupt:
                print("\n\nSession terminated by user.")
                break
            except Exception as e:
                print(f"\n⚠️ Error processing request: {e}\n")

    def run_benchmark(self):
        """Run benchmark evaluation queries across all key policy domains"""
        test_cases = [
            "What courses and degree programs are offered at TPC?",
            "What is the dress code policy for entrance exam?",
            "What are the curfew hours under Talibon Municipal Ordinance 127?",
            "How can a student qualify for the GSIS STEM subsidy?",
            "What is the 500-meter alcohol prohibition zone around TPC?",
            "What is the population of Tokyo?"  # Out of scope test
        ]
        print("\n" + "=" * 65)
        print("🧪 RUNNING BENCHMARK EVALUATION TEST CASES")
        print("=" * 65)
        for i, q in enumerate(test_cases, 1):
            print(f"\n[{i}/6] ❓ Test Query: \"{q}\"")
            retrieved = self.retrieve_context(q, top_k=4)
            res = self.generate_response(q, retrieved)
            print(f"🤖 Answer:\n{res['answer']}")
            print(f"📚 Sources: {res['sources']} | Score: {res['confidence']:.4f} | Engine: {res['model_used']}")
        print("\n" + "=" * 65)
        print("✅ Benchmark execution completed!")
        print("=" * 65 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(description="TPoliCynav RAG Conversational Agent")
    parser.add_argument(
        "--mode",
        choices=["auto", "offline", "online"],
        default="auto",
        help="Operation mode: 'auto' (default: cloud with local fallback), 'offline' (100%% local), 'online' (cloud only)"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Shortcut to run in 100%% Offline Mode"
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="Shortcut to run in Online Only Mode"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    selected_mode = "offline" if args.offline else ("online" if args.online else args.mode)
    bot = TPoliCynavBot(mode=selected_mode)
    bot.chat_loop()
