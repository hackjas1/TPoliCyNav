"""
=============================================================================
TPoliCynav — Prompt Architecture & Templates
Checkpoint 2: Prompt Architecture
=============================================================================
Defines prompt templates for RAG orchestration, few-shot demonstrations,
and context formatting.
=============================================================================
"""

import os

PROMPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEM_PROMPT_PATH = os.path.join(PROMPTS_DIR, "system_prompt.txt")


def load_system_prompt() -> str:
    """Load the master system prompt from file."""
    if os.path.exists(SYSTEM_PROMPT_PATH):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "You are TPoliCynav, the institutional policy assistant for Talibon Polytechnic College."


# RAG Augmented Generation Template
RAG_PROMPT_TEMPLATE = """{system_prompt}

----------------------------------------
INSTITUTIONAL POLICY CONTEXT:
----------------------------------------
{retrieved_context}
----------------------------------------

STUDENT INQUIRY:
{user_query}

INSTRUCTIONS:
1. Answer the inquiry based ONLY on the context provided above.
2. Explicitly cite the document source (e.g., [TPC Student Handbook, Page X] or [Municipal Ordinance No. 127]).
3. If the context does not contain the answer, politely state that you do not have that information and direct the student to the appropriate office.

ANSWER:"""


# Few-Shot Demonstrations for Grounded Policy Navigation
FEW_SHOT_EXAMPLES = [
    {
        "query": "Can I wear shorts during the entrance exam?",
        "context": "[Source: admissions_guidelines]\nIMPORTANT REMINDERS FOR EXAMINEES:\n- Come in proper attire. The following are NOT ALLOWED:\n  - Ripped jeans\n  - Shorts\n  - Sleeveless tops\n  - Slippers",
        "answer": "No, you cannot wear shorts during the TPC Entrance Examination. According to the **TPC Admissions and Entrance Examination Guidelines**, examinees must come in proper attire, and shorts, ripped jeans, sleeveless tops, and slippers are strictly prohibited."
    },
    {
        "query": "What is the curfew for boarding houses near TPC?",
        "context": "[Source: municipal_ordinance_127]\nSECTION 6. CURFEW HOURS AND LOGBOOK MONITORING\n1. Mandatory Curfew: A standard curfew of 10:00 PM is hereby enforced for all student residents from Sunday through Thursday, and 11:00 PM on Friday and Saturday.",
        "answer": "Under **Talibon Municipal Ordinance No. 127 (Section 6)**, the mandatory curfew for students in boarding houses and dormitories near TPC is:\n- **10:00 PM** from Sunday through Thursday\n- **11:00 PM** on Friday and Saturday\n\nExceptions apply only when academic activities are certified in writing by the TPC Administration."
    }
]


def format_rag_prompt(user_query: str, retrieved_chunks: list) -> str:
    """
    Assemble the complete prompt with system instructions and retrieved context.

    Args:
        user_query: The student's question
        retrieved_chunks: List of retrieved chunk dictionaries with 'source' and 'text'
    """
    system_prompt = load_system_prompt()
    
    context_blocks = []
    for i, chunk in enumerate(retrieved_chunks, 1):
        source = chunk.get("source", "Official TPC Policy")
        text = chunk.get("text", "").strip()
        context_blocks.append(f"[{i}] SOURCE: {source}\n{text}\n")
    
    retrieved_context = "\n".join(context_blocks)
    
    return RAG_PROMPT_TEMPLATE.format(
        system_prompt=system_prompt,
        retrieved_context=retrieved_context,
        user_query=user_query
    )
