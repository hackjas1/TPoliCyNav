import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from app.rag_engine import TPCRagEngine

print("=" * 80)
print("INITIALIZING TPCRagEngine FOR VALIDATION...")
print("=" * 80)
engine = TPCRagEngine()

test_suite = [
    # 1. Chitchat
    ("Hello, good morning!", "CHITCHAT"),
    ("Who are you?", "CHITCHAT"),

    # 2. Out-of-Scope (Should all be REFUSED with is_refusal=True, sources=[])
    ("What is the capital of the Philippines?", "OUT_OF_SCOPE"),
    ("Can you write a poem about Bohol?", "OUT_OF_SCOPE"),
    ("How do I cook chicken adobo?", "OUT_OF_SCOPE"),
    ("What is Python programming?", "OUT_OF_SCOPE"),
    ("Write code to reverse a list", "OUT_OF_SCOPE"),
    ("Tell me a joke", "OUT_OF_SCOPE"),
    ("Who is the President of the United States?", "OUT_OF_SCOPE"),
    ("Solve 3x + 12 = 30", "OUT_OF_SCOPE"),
    ("What is the weather today in Bohol?", "OUT_OF_SCOPE"),
    ("Who is the mayor of Talibon?", "OUT_OF_SCOPE"),
    ("Can I bring a pet dog to class?", "OUT_OF_SCOPE"),

    # 3. Legitimate In-Scope TPC Policies (Must be ANSWERED with is_refusal=False, sources populated)
    ("What are the freshman admission requirements and steps for TPC?", "IN_SCOPE"),
    ("What is the official Type A school uniform description?", "IN_SCOPE"),
    ("What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?", "IN_SCOPE"),
    ("What is the minimum GWA required to qualify for the GSIS STEM subsidy?", "IN_SCOPE"),
    ("What courses and undergraduate degree programs are officially offered at TPC?", "IN_SCOPE")
]

passed_count = 0
failed_count = 0

for q, expected_cat in test_suite:
    res = engine.query(q)
    is_refusal = res.get("is_refusal", False)
    sources = res.get("sources", [])
    answer = res.get("answer", "")
    engine_used = res.get("engine_used", "")
    conf = res.get("confidence", 0.0)

    if expected_cat == "CHITCHAT":
        passed = (not is_refusal) and ("TPoliCynav" in answer or "welcome" in answer.lower())
    elif expected_cat == "OUT_OF_SCOPE":
        passed = is_refusal and (len(sources) == 0) and ("cannot find" in answer.lower() or "outside" in answer.lower() or "scope" in answer.lower())
    elif expected_cat == "IN_SCOPE":
        passed = (not is_refusal) and (len(sources) > 0) and len(answer) > 50

    status_str = "PASS" if passed else "FAIL"
    if passed:
        passed_count += 1
    else:
        failed_count += 1

    print(f"[{status_str}] [{expected_cat}] Query: '{q}'")
    print(f"       -> Conf: {conf:.4f} | is_refusal: {is_refusal} | Sources: {sources}")
    print(f"       -> Engine: {engine_used}")
    print(f"       -> Preview: {answer[:110].replace(chr(10), ' ')}...")
    print("-" * 80)

print(f"\nTEST RESULTS: {passed_count}/{len(test_suite)} PASSED, {failed_count} FAILED.")
