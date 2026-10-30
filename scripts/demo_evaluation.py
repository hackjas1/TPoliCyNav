"""
=============================================================================
TPoliCynav — Live Demo & Multi-Query Evaluation Suite
Checkpoint 3: Deliverable 14
=============================================================================
Runs an automated benchmark of 6 realistic queries (5 in-scope + 1 out-of-scope
hallucination test), measures latency and confidence, and validates grounded citations.
=============================================================================
"""

import os
import sys
import json
import time
from datetime import datetime

# Windows encoding fix
sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from app.rag_engine import TPCRagEngine

EVALUATION_RESULTS_PATH = os.path.join(PROJECT_ROOT, "docs", "evaluation_results.json")

TEST_CASES = [
    {
        "id": "TC-01",
        "category": "Academic Offerings",
        "query": "What courses and undergraduate degree programs are officially offered at TPC?",
        "expected_source": "TPC Student Handbook v.04 / Admissions Guidelines",
        "should_refuse": False
    },
    {
        "id": "TC-02",
        "category": "Admissions & Dress Code",
        "query": "Are ripped jeans, shorts, or slippers allowed during the TPC entrance examination?",
        "expected_source": "TPC Admissions Guidelines & Dress Code Annex",
        "should_refuse": False
    },
    {
        "id": "TC-03",
        "category": "Municipal Student Housing",
        "query": "What are the curfew hours for boarding houses and dormitories under Talibon Municipal Ordinance 127?",
        "expected_source": "Talibon Municipal Ordinance No. 127",
        "should_refuse": False
    },
    {
        "id": "TC-04",
        "category": "Financial Subsidy",
        "query": "What is the minimum GWA required to qualify for the GSIS STEM scholarship subsidy?",
        "expected_source": "GSIS Subsidy for STEM (GSSP) Guidelines",
        "should_refuse": False
    },
    {
        "id": "TC-05",
        "category": "Campus Safety & Vicinity",
        "query": "What is the 500-meter alcohol and entertainment prohibition zone around TPC?",
        "expected_source": "Talibon Municipal Ordinance No. 127 / PNP Guidelines",
        "should_refuse": False
    },
    {
        "id": "TC-06",
        "category": "Out-of-Scope (Hallucination Test)",
        "query": "What is the capital city and total population of Tokyo, Japan?",
        "expected_source": "None (Graceful Refusal)",
        "should_refuse": True
    }
]


def run_evaluation():
    print("=" * 75)
    print("  🧪 TPOLICYNAV — LIVE BENCHMARK & EVALUATION TEST HARNESS")
    print("  Talibon Polytechnic College Generative AI System (Checkpoints 3 & 4)")
    print("=" * 75)

    engine = TPCRagEngine(mode="auto")
    status = engine.get_system_status()
    print(f"📊 Engine Status: {status['status']}")
    print(f"🌲 Vector Backend: {status['vector_backend']}")
    print(f"🤖 LLM Generator: {status['llm_engine']}")
    print(f"📚 Indexed Chunks: {status['indexed_chunks']}")
    print("=" * 75 + "\n")

    results = []
    total_passed = 0

    for tc in TEST_CASES:
        print(f"───────────────────────────────────────────────────────────────────────────")
        print(f"[{tc['id']}] Category: {tc['category']}")
        print(f"❓ Query: \"{tc['query']}\"")

        res = engine.query(tc["query"])

        confidence = res.get("confidence", 0.0)
        sources = res.get("sources", [])
        is_refusal = res.get("is_refusal", False)
        latency = res.get("latency_ms", 0)
        answer = res.get("answer", "")

        # Verify test pass criteria
        passed = False
        if tc["should_refuse"]:
            passed = is_refusal
            verdict = "✅ PASSED (Correctly Refused Off-Topic Query)" if passed else "❌ FAILED (Hallucinated on Out-of-Scope)"
        else:
            passed = (not is_refusal) and (confidence >= 0.50) and len(sources) > 0
            verdict = "✅ PASSED (Grounded Answer with Citations)" if passed else "❌ FAILED (Low Confidence or Missing Citations)"

        if passed:
            total_passed += 1

        print(f"🤖 Answer:\n{answer}")
        print(f"📚 Sources: {sources or 'None (Refusal)'}")
        print(f"🎯 Match Confidence: {confidence:.4f} | ⏱️ Latency: {latency} ms")
        print(f"📋 Test Verdict: {verdict}\n")

        results.append({
            "id": tc["id"],
            "category": tc["category"],
            "query": tc["query"],
            "expected_source": tc["expected_source"],
            "answer": answer,
            "sources": sources,
            "confidence": confidence,
            "latency_ms": latency,
            "is_refusal": is_refusal,
            "passed": passed
        })

    # Summary
    print("=" * 75)
    print(f"🏆 EVALUATION SUMMARY: {total_passed}/{len(TEST_CASES)} Tests Passed ({total_passed / len(TEST_CASES) * 100:.1f}%)")
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)
    avg_conf_in_scope = sum(r["confidence"] for r in results if not r["is_refusal"]) / max(1, len([r for r in results if not r["is_refusal"]]))
    print(f"⚡ Average Latency: {avg_latency:.1f} ms")
    print(f"🎯 In-Scope Average Confidence: {avg_conf_in_scope:.4f}")
    print("=" * 75)

    # Save to JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(TEST_CASES),
        "total_passed": total_passed,
        "pass_rate_pct": float(f"{total_passed / len(TEST_CASES) * 100:.1f}"),
        "average_latency_ms": round(avg_latency, 2),
        "average_in_scope_confidence": round(avg_conf_in_scope, 4),
        "system_status": status,
        "test_results": results
    }

    with open(EVALUATION_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"💾 Benchmark report saved to: {EVALUATION_RESULTS_PATH}\n")


if __name__ == "__main__":
    run_evaluation()

