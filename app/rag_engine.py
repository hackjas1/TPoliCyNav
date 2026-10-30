"""
=============================================================================
TPoliCynav — LangChain RAG Orchestration Engine
Checkpoint 3: Deliverable 11 & 12
=============================================================================
Orchestrates:
  1. Multi-Turn Query Contextualization via ConversationalMemoryManager
  2. Dense Vector Retrieval (LangChain Custom Retriever over Pinecone & NumPy)
  3. Strict Scope Containment Guardrail (Threshold < 0.50 refusal)
  4. Grounded Generative LLM Response Synthesis (Cloud / Offline Fallback)
  5. Canonical Institutional Policy Citations & Confidence Scoring
=============================================================================
"""

import os
import sys
import re
import json
import time
from typing import List, Dict, Any, Optional

import numpy as np
import torch
# Restrict PyTorch threads to reduce memory and CPU thrashing on cloud containers
try:
    torch.set_num_threads(2)
except Exception:
    pass
from dotenv import load_dotenv

# LangChain Imports
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import Field

# Local modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from app.memory_manager import ConversationalMemoryManager
from prompts.prompt_templates import format_rag_prompt, load_system_prompt
from app.scope_guard import (
    check_conversational_chitchat,
    is_explicitly_out_of_scope,
    get_institutional_refusal_message,
    verify_lexical_alignment
)

# Constants & Paths
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
EMBEDDINGS_PATH = os.path.join(PROCESSED_DIR, "embeddings.npy")
CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")

MODEL_NAME = "BAAI/bge-small-en-v1.5"
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tpolicynav")
HF_TOKEN = os.getenv("HF_TOKEN")
LLM_MODEL = "Qwen/Qwen2.5-72B-Instruct"

CONFIDENCE_THRESHOLD = 0.60

SOURCE_DISPLAY_NAMES = {
    "admissions_guidelines": "TPC Admissions Guidelines & Degree Offerings",
    "tpc_student_handbook": "TPC Student Handbook v.04",
    "tpc_uniform_and_dress_code_guide": "TPC School Uniform & Dress Code Policy",
    "municipal_ordinance_127": "Talibon Municipal Ordinance No. 127 (Boarding Houses)",
    "pnp_tpc_security": "PNP-TPC Joint Campus Safety Guidelines",
    "ched_free_education": "CHED Free Higher Education (RA 10931)",
    "gsis_stem_subsidy": "GSIS Subsidy for STEM (GSSP) Guidelines"
}


class TPCVectorRetriever(BaseRetriever):
    """
    LangChain-compliant Hybrid Retriever supporting Pinecone Cloud
    with seamless local NumPy in-memory fallback.
    """
    encoder: Any = Field(default=None)
    local_embeddings: Any = Field(default=None)
    local_chunks: Any = Field(default=None)
    pinecone_index: Any = Field(default=None)
    top_k: int = 4

    class Config:
        arbitrary_types_allowed = True

    def get_relevant_documents(self, query: str) -> List[Document]:
        """LangChain legacy & direct retrieval call."""
        return self._retrieve(query)

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        """LangChain BaseRetriever abstract method."""
        return self._retrieve(query)

    def _retrieve(self, query: str) -> List[Document]:
        """Retrieve top_k documents by cosine similarity with minimal memory overhead."""
        import gc
        with torch.no_grad():
            query_vec = self.encoder.encode(query, normalize_embeddings=True)
        gc.collect()

        # 1. Attempt Pinecone Cloud Retrieval
        if self.pinecone_index is not None:
            try:
                res = self.pinecone_index.query(
                    vector=query_vec.tolist(),
                    top_k=self.top_k,
                    include_metadata=True
                )
                docs = []
                for match in res.get("matches", []):
                    meta = match.get("metadata", {})
                    meta["score"] = float(match.get("score", 0.0))
                    meta["chunk_id"] = match.get("id")
                    meta["display_source"] = SOURCE_DISPLAY_NAMES.get(
                        meta.get("source", ""), meta.get("source", "Official TPC Policy")
                    )
                    docs.append(Document(page_content=meta.get("text", ""), metadata=meta))
                if docs:
                    return docs
            except Exception as e:
                pass

        # 2. Local In-Memory NumPy Cosine Retrieval Fallback
        if self.local_embeddings is not None and self.local_chunks is not None:
            sims = np.dot(self.local_embeddings, query_vec)
            top_indices = np.argsort(sims)[::-1][:self.top_k]
            docs = []
            for idx in top_indices:
                chunk = self.local_chunks[idx]
                meta = dict(chunk)
                meta["score"] = float(sims[idx])
                meta["display_source"] = SOURCE_DISPLAY_NAMES.get(
                    chunk.get("source", ""), chunk.get("source", "Official TPC Policy")
                )
                docs.append(Document(page_content=chunk.get("text", ""), metadata=meta))
            return docs

        return []


class TPCRagEngine:
    """
    Production LangChain RAG Orchestration Engine for Talibon Polytechnic College.
    Features:
      - Multi-turn conversational memory with coreference resolution
      - Scope containment guardrails (out-of-scope refusal)
      - Dual generation (Cloud HuggingFace Qwen-72B or Offline Extractor)
      - Canonical citations and latency tracking
    """

    def __init__(self, mode: str = "auto", max_history_turns: int = 5):
        self.mode = mode.lower()
        self.memory = ConversationalMemoryManager(max_turns=max_history_turns)

        # 1. Initialize Embedding Model
        from sentence_transformers import SentenceTransformer
        self.encoder = SentenceTransformer(MODEL_NAME)

        # 2. Load Local Vectors & Chunks
        self.local_embeddings = None
        self.local_chunks = None
        if os.path.exists(EMBEDDINGS_PATH) and os.path.exists(CHUNKS_PATH):
            try:
                self.local_embeddings = np.load(EMBEDDINGS_PATH)
                with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                    self.local_chunks = json.load(f)
            except Exception as e:
                pass

        # 3. Initialize Cloud Pinecone Index
        self.index = None
        if self.mode != "offline" and PINECONE_API_KEY and not PINECONE_API_KEY.startswith("your_"):
            try:
                from pinecone import Pinecone
                pc = Pinecone(api_key=PINECONE_API_KEY)
                self.index = pc.Index(INDEX_NAME)
                _ = pc.describe_index(INDEX_NAME)
            except Exception:
                self.index = None

        # 4. Instantiate LangChain Retriever
        self.retriever = TPCVectorRetriever(
            encoder=self.encoder,
            local_embeddings=self.local_embeddings,
            local_chunks=self.local_chunks,
            pinecone_index=self.index,
            top_k=4
        )

        # 5. Initialize Cloud LLM Client
        self.hf_client = None
        if self.mode != "offline" and HF_TOKEN and not HF_TOKEN.startswith("your_"):
            try:
                from huggingface_hub import InferenceClient
                self.hf_client = InferenceClient(token=HF_TOKEN, timeout=4)
            except Exception:
                self.hf_client = None

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Executes complete multi-turn RAG pipeline with multi-layer scope containment:
          Chitchat/Intent Check -> Contextualization -> Retrieval -> Threshold & Lexical Guardrails -> Generation -> Memory Update
        """
        start_time = time.time()
        user_query = user_query.strip()
        if not user_query:
            return {"error": "Empty query received"}

        # Step 0a: Conversational chitchat & bot identity check
        chitchat_answer = check_conversational_chitchat(user_query)
        if chitchat_answer:
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.memory.add_turn(user_query, chitchat_answer, sources=["Talibon Polytechnic College"], is_refusal=False)
            return {
                "answer": chitchat_answer,
                "sources": ["Talibon Polytechnic College"],
                "confidence": 1.0,
                "chunks": [],
                "engine_used": "Institutional Welcome & Identity Handler",
                "latency_ms": elapsed_ms,
                "reformulated_query": None,
                "is_refusal": False
            }

        # Step 0b: Explicit out-of-scope intent guardrail
        is_oos, oos_reason = is_explicitly_out_of_scope(user_query)
        if is_oos:
            refusal_answer = get_institutional_refusal_message(oos_reason)
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.memory.add_turn(user_query, refusal_answer, sources=[], is_refusal=True)
            return {
                "answer": refusal_answer,
                "sources": [],
                "confidence": 0.0,
                "chunks": [],
                "engine_used": f"Scope Guardrail: {oos_reason}",
                "latency_ms": elapsed_ms,
                "reformulated_query": None,
                "is_refusal": True
            }

        # Step 1: Contextualize query using dialogue history
        reformulated_query = self.memory.contextualize_query(user_query)
        if reformulated_query != user_query:
            is_ref_oos, ref_oos_reason = is_explicitly_out_of_scope(reformulated_query)
            if is_ref_oos:
                refusal_answer = get_institutional_refusal_message(ref_oos_reason)
                elapsed_ms = int((time.time() - start_time) * 1000)
                self.memory.add_turn(user_query, refusal_answer, sources=[], is_refusal=True)
                return {
                    "answer": refusal_answer,
                    "sources": [],
                    "confidence": 0.0,
                    "chunks": [],
                    "engine_used": f"Scope Guardrail: {ref_oos_reason}",
                    "latency_ms": elapsed_ms,
                    "reformulated_query": reformulated_query,
                    "is_refusal": True
                }

        # Step 2: Retrieve relevant documents via LangChain Retriever
        docs = self.retriever.get_relevant_documents(reformulated_query)

        # Compute max confidence score
        max_score = max([d.metadata.get("score", 0.0) for d in docs]) if docs else 0.0

        # Step 3a: Cosine Similarity Threshold Guardrail
        if max_score < CONFIDENCE_THRESHOLD:
            refusal_answer = get_institutional_refusal_message("Low Retrieval Confidence / Below Threshold")
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.memory.add_turn(user_query, refusal_answer, sources=[], is_refusal=True)
            return {
                "answer": refusal_answer,
                "sources": [],
                "confidence": max_score,
                "chunks": [],
                "engine_used": "Scope Containment Guardrail (Cosine Similarity < 0.60)",
                "latency_ms": elapsed_ms,
                "reformulated_query": reformulated_query if reformulated_query != user_query else None,
                "is_refusal": True
            }

        # Step 3b: Anti-Hallucination Lexical Alignment Guardrail
        if not verify_lexical_alignment(reformulated_query, docs):
            refusal_answer = get_institutional_refusal_message("Unindexed Topic / No Lexical Alignment")
            elapsed_ms = int((time.time() - start_time) * 1000)
            self.memory.add_turn(user_query, refusal_answer, sources=[], is_refusal=True)
            return {
                "answer": refusal_answer,
                "sources": [],
                "confidence": max_score,
                "chunks": [],
                "engine_used": "Anti-Hallucination Guardrail (Lexical Verification Failed)",
                "latency_ms": elapsed_ms,
                "reformulated_query": reformulated_query if reformulated_query != user_query else None,
                "is_refusal": True
            }

        # Step 4: Synthesize Answer (Cloud LLM or Local Precision Extractor)
        retrieved_chunks = [
            {"source": d.metadata.get("source", ""), "text": d.page_content, "score": d.metadata.get("score", 0.0)}
            for d in docs
        ]

        answer_text = None
        engine_label = None
        cited_sources = []
        is_refusal = False

        # 4a. Cloud Hugging Face Generation with Zero-Temperature
        if self.hf_client is not None:
            try:
                prompt_text = format_rag_prompt(reformulated_query, retrieved_chunks)
                response = self.hf_client.chat_completion(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are TPoliCynav, the institutional policy assistant for Talibon Polytechnic College (TPC). "
                                "Base your answers STRICTLY and EXCLUSIVELY on the provided institutional context. "
                                "Never speculate or invent answers. If the context does not state the answer, politely refuse."
                            )
                        },
                        {"role": "user", "content": prompt_text}
                    ],
                    model=LLM_MODEL,
                    max_tokens=450,
                    temperature=0.0
                )
                candidate_text = response.choices[0].message.content.strip()
                if any(phrase in candidate_text.lower() for phrase in [
                    "cannot find specific information", "not mentioned in the provided",
                    "not found in the provided context", "does not contain"
                ]):
                    answer_text = candidate_text
                    is_refusal = True
                    cited_sources = []
                    engine_label = f"LangChain + Grounded LLM Refusal ({LLM_MODEL})"
                else:
                    answer_text = candidate_text
                    engine_label = f"LangChain + Generative Cloud LLM ({LLM_MODEL})"
                    cited_sources = list(dict.fromkeys([
                        SOURCE_DISPLAY_NAMES.get(c["source"], c["source"]) for c in retrieved_chunks
                    ]))
            except Exception:
                answer_text = None  # Fall through to offline extractor

        # 4b. Local Precision Extractor Fallback
        if answer_text is None:
            extracted_ans, extracted_sources = self._extract_offline_answer(reformulated_query, docs)
            if extracted_ans:
                answer_text = extracted_ans
                cited_sources = extracted_sources
                engine_label = "LangChain + Precision Policy Extractor (Local Fallback)"
            else:
                answer_text = get_institutional_refusal_message("No Matching Policy Provision Found")
                cited_sources = []
                is_refusal = True
                engine_label = "Anti-Hallucination Extractor (Zero Overlap Refusal)"

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Step 5: Update conversational memory
        self.memory.add_turn(user_query, answer_text, sources=cited_sources, is_refusal=is_refusal)

        return {
            "answer": answer_text,
            "sources": cited_sources,
            "confidence": max_score,
            "chunks": [
                {
                    "source": d.metadata.get("display_source", d.metadata.get("source", "")),
                    "chunk_id": d.metadata.get("chunk_id", ""),
                    "score": d.metadata.get("score", 0.0),
                    "text": d.page_content[:350] + ("..." if len(d.page_content) > 350 else "")
                }
                for d in docs
            ] if not is_refusal else [],
            "engine_used": engine_label,
            "latency_ms": elapsed_ms,
            "reformulated_query": reformulated_query if reformulated_query != user_query else None,
            "is_refusal": is_refusal
        }

    def _extract_offline_answer(self, query: str, docs: List[Document]) -> tuple:
        """Fast, precision anti-hallucination policy extractor."""
        if not docs:
            return None, []

        # 1. Degree programs query handling
        is_course_query = bool(re.search(r'course|program|degree|offer|bachelor|curriculum|major', query, re.IGNORECASE))
        for doc in docs:
            raw = doc.page_content
            if "DEGREE PROGRAMS" in raw.upper() or (is_course_query and "BACHELOR OF" in raw.upper()):
                programs = re.findall(r'\d+\.\s+([A-Za-z\s\(\)\-]+?)(?=\s+\d+\.|\s+All degree|\s+TALIBON|\s+TPC|$)', raw)
                if len(programs) >= 4:
                    prog_lines = [f"{i}. {p.strip()}" for i, p in enumerate(programs, 1)]
                    ans = (
                        "**Talibon Polytechnic College (TPC) officially offers the following 7 undergraduate degree programs:**\n\n"
                        + "\n".join(prog_lines)
                        + "\n\n*(Recognized by CHED and covered under RA 10931 Free Higher Education Act.)*"
                    )
                    return ans, [SOURCE_DISPLAY_NAMES.get(doc.metadata.get("source", ""), "TPC Student Handbook v.04")]

        # 2. Extract best sentences from top documents using substantive keyword overlap
        stopwords = {
            "what", "is", "the", "are", "can", "for", "and", "under", "in", "of", "a", "an", "to", "how", "do", "i",
            "you", "we", "they", "this", "that", "there", "about", "who", "whom", "where", "when", "why", "which",
            "tell", "me", "give", "please", "kindly", "does", "have", "has", "had", "would", "should", "could"
        }
        query_words = set(re.findall(r'[a-zA-Z]{3,}', query.lower())) - stopwords

        if not query_words:
            return None, []

        top_sentences = []
        cited_sources = []

        for doc in docs[:2]:
            source_label = SOURCE_DISPLAY_NAMES.get(doc.metadata.get("source", ""), "Official TPC Policy")
            splits = re.split(r'(?<=[.!?])\s+|(?<=\d\.)\s+|SECTION\s+\d+\.\s*', doc.page_content)
            scored = []
            for s in splits:
                s_clean = s.strip()
                if len(s_clean.split()) >= 4 and not s_clean.startswith("===") and not s_clean.isupper():
                    s_words = set(re.findall(r'[a-zA-Z]{3,}', s_clean.lower()))
                    overlap = len(query_words & s_words)
                    # Anti-hallucination requirement: sentence must directly contain query terms
                    if overlap >= 1:
                        scored.append((overlap, s_clean))

            if scored:
                scored.sort(key=lambda x: x[0], reverse=True)
                if source_label not in cited_sources:
                    cited_sources.append(source_label)
                for _, sent in scored[:2]:
                    cleaned = re.sub(r'^[•\-\d\.\s]+', '', sent).strip()
                    if cleaned and cleaned not in top_sentences:
                        top_sentences.append(cleaned)
                    if len(top_sentences) >= 3:
                        break
            if len(top_sentences) >= 3:
                break

        if not top_sentences:
            return None, []

        primary_source = cited_sources[0] if cited_sources else "Official TPC Policy"
        bullets = [f"• {s}" for s in top_sentences]
        return f"**{primary_source}:**\n\n" + "\n\n".join(bullets), cited_sources

    def reset_memory(self):
        """Clear conversation history."""
        self.memory.clear()

    def get_system_status(self) -> Dict[str, Any]:
        """Return connectivity and resource diagnostics."""
        has_pinecone = self.index is not None
        has_llm = self.hf_client is not None
        chunk_count = len(self.local_chunks) if self.local_chunks else 0

        status = "Online (Cloud Vector + Cloud LLM)" if (has_pinecone and has_llm) else (
            "Hybrid (Cloud Vector + Local Fallback)" if has_pinecone else "Offline / Local Engine"
        )

        return {
            "status": status,
            "vector_backend": "Pinecone Serverless (AWS us-east-1)" if has_pinecone else "Local NumPy Matrix",
            "llm_engine": f"Hugging Face ({LLM_MODEL})" if has_llm else "Local Precision Policy Extractor",
            "indexed_chunks": chunk_count,
            "embedding_model": MODEL_NAME,
            "turns_in_memory": self.memory.get_turn_count()
        }
