"""
=============================================================================
TPoliCynav — Institutional Scope Containment & Guardrails Module
Checkpoint 3 & 4: Multi-Layer Scope Containment (Defense-in-Depth)
=============================================================================
Provides:
  1. Fast deterministic intent classification for explicit out-of-scope queries
  2. Conversational chitchat handling (greetings, identity, bot capabilities)
  3. Context-sensitive lexical relevance verification
  4. Institutional refusal formulation with campus contact redirection
=============================================================================
"""

import re
from typing import Tuple, Optional, Dict, Any, List

# Official TPC institutional domain topics
IN_SCOPE_KEYWORDS = {
    "tpc", "talibon", "handbook", "ordinance", "curfew", "uniform", "dress",
    "attire", "shoes", "pants", "shirt", "id", "haircut", "grooming",
    "admission", "admissions", "enrollment", "entrance", "exam", "tpcat",
    "course", "courses", "program", "programs", "degree", "degrees", "bachelor",
    "curriculum", "retention", "gwa", "grade", "grades", "grading", "failing",
    "inc", "prerequisite", "transferee", "shifter", "cross", "overload",
    "scholarship", "scholarships", "subsidy", "subsidies", "ched", "gsis",
    "gssp", "tes", "10931", "127", "free", "tuition", "miscellaneous",
    "boarding", "dormitory", "dorm", "landlord", "safety", "fire", "sanitation",
    "inspection", "pnp", "police", "security", "patrol", "500", "meter",
    "alcohol", "liquor", "gambling", "smoking", "vaping", "drugs", "disciplinary",
    "sanction", "sanctions", "suspension", "dismissal", "probation", "offense",
    "offenses", "grievance", "board", "osas", "registrar", "president",
    "campus", "college", "student", "students", "faculty", "leave", "clearance"
}


def check_conversational_chitchat(query: str) -> Optional[str]:
    """
    Checks if query is a simple greeting, bot identity question, or capability check.
    Returns a friendly, scoped institutional response or None.
    """
    q = query.strip().lower()
    q_clean = re.sub(r'[^\w\s]', ' ', q).strip()
    words = q_clean.split()

    # Greetings
    greeting_pattern = r'^(hi|hello|hey|mabuhay|good\s+morning|good\s+afternoon|good\s+evening|kamusta|kumusta)\b'
    if re.search(greeting_pattern, q) and len(words) <= 5:
        return (
            "👋 **Mabuhay and welcome, TPCian!** I am **TPoliCynav**, the official AI-driven "
            "Institutional Policy Navigator for **Talibon Polytechnic College (TPC)**.\n\n"
            "I provide grounded policy guidance directly from verified college publications:\n"
            "• 🎓 **Admissions & Degree Programs Offered**\n"
            "• 👔 **School Uniform Standards & Exam Dress Code**\n"
            "• 🏠 **Boarding House Curfew & Safety (Ordinance 127)**\n"
            "• 💰 **CHED Free Higher Education (RA 10931) & GSIS STEM Grants**\n"
            "• ⚖️ **Academic Retention (GWA) & Disciplinary Sanctions**\n\n"
            "How may I assist your college journey today? You may ask any question about TPC policies!"
        )

    # Bot Identity / Who are you
    identity_queries = [
        "who are you", "what are you", "sino ka", "what is your name",
        "who made you", "who created you", "tell me about yourself", "what is tpolicynav"
    ]
    if any(q_clean.startswith(pat) for pat in identity_queries) or q_clean in identity_queries:
        return (
            "🏛️ **I am TPoliCynav (The TPC Policy Navigator)** — the official institutional policy "
            "conversational agent developed for **Talibon Polytechnic College (TPC)** in Bohol, Philippines.\n\n"
            "Developed as an **IS Professional Elective #4 Capstone Project** by **Team Kuys** "
            "(Eduardo Avenido Jr., Christian Paul G. La Rosa, Nielbert Garcia, Marcel Avergonzado, and Ronald M. Barril).\n\n"
            "My knowledge base is strictly grounded on the *TPC Student Handbook v.04*, *Talibon Municipal Ordinance No. 127*, "
            "*CHED RA 10931*, and official college memorandums."
        )

    return None


def is_explicitly_out_of_scope(query: str) -> Tuple[bool, Optional[str]]:
    """
    High-precision deterministic intent classifier for queries that are completely
    outside the institutional domain of Talibon Polytechnic College.

    Returns:
        (is_out_of_scope: bool, reason: Optional[str])
    """
    q = query.strip().lower()

    # 1. Programming & Coding
    code_patterns = [
        r'\b(write|create|generate|debug|fix)\s+(a\s+)?(python|javascript|java|c\+\+|c#|php|html|css|sql|react|code|script|function|program)\b',
        r'\b(reverse\s+a\s+(string|list|array)|sort\s+an\s+array|binary\s+search|linked\s+list)\b',
        r'\b(write\s+code\b|how\s+to\s+code\b|print\(|def\s+\w+\(|function\(|console\.log)\b',
        r'\bwhat\s+is\s+(python|javascript|java|c\+\+|html|css|react)\s+programming\b'
    ]
    for pat in code_patterns:
        if re.search(pat, q):
            return True, "Software Development / Programming Inquiry"

    # 2. General Math / Homework Equation Solving
    math_patterns = [
        r'\b(solve|calculate|evaluate)\s+.*[=+\-*/^]{1,}.*\d',
        r'\bsolve\s+for\s+[xyz]\b',
        r'\b(math\s+homework|integral\s+of|derivative\s+of|quadratic\s+formula)\b',
        r'\b\d+\s*[\+\-\*\/]\s*\d+\s*='
    ]
    for pat in math_patterns:
        if re.search(pat, q):
            return True, "General Mathematical Computation / Homework Task"

    # 3. Creative Writing / Entertainment / Jokes
    creative_patterns = [
        r'\b(tell|make|give)\s+(me\s+)?(a\s+)?(joke|riddle|pun)\b',
        r'\b(write|compose|generate)\s+(a\s+)?(poem|story|song|rap|lyrics|essay)\b',
        r'\b(sing\s+a\s+song|entertain\s+me)\b'
    ]
    for pat in creative_patterns:
        if re.search(pat, q):
            return True, "Creative Writing & Entertainment Request"

    # 4. General World Trivia, Geography & Global Politics
    trivia_patterns = [
        r'\bwhat\s+is\s+the\s+capital\s+of\b',
        r'\bwho\s+is\s+the\s+president\s+of\s+(the\s+united\s+states|america|russia|china|france|uk|japan)\b',
        r'\bwho\s+won\s+(miss\s+universe|the\s+world\s+cup|the\s+nba|the\s+super\s+bowl|the\s+oscar)\b',
        r'\bwho\s+is\s+(taylor\s+swift|elon\s+musk|messi|ronaldo|donald\s+trump|joe\s+biden)\b',
        r'\b(best\s+movie\s+of|top\s+grossing\s+movie|box\s+office)\b',
        r'\bwhat\s+is\s+the\s+tallest\s+mountain\b',
        r'\bwhat\s+is\s+the\s+population\s+of\s+(tokyo|japan|china|india|usa|new\s+york|paris)\b'
    ]
    for pat in trivia_patterns:
        if re.search(pat, q):
            return True, "External World Trivia & Global Affairs"

    # 5. Cooking & Culinary Recipes
    cooking_patterns = [
        r'\b(how\s+to\s+(cook|bake|make|prepare|fry|roast)|recipe\s+for)\s+(chicken|pork|beef|cake|adobo|sinigang|bread|cookie|food|dish)\b'
    ]
    for pat in cooking_patterns:
        if re.search(pat, q):
            return True, "Culinary & Cooking Inquiries"

    # 6. Real-time Weather & Stock Market
    realtime_patterns = [
        r'\b(weather\s+(today|tomorrow|forecast)|typhoon\s+signal|stock\s+price|bitcoin\s+price|exchange\s+rate\s+today)\b'
    ]
    for pat in realtime_patterns:
        if re.search(pat, q):
            return True, "Real-time Weather & External Market Updates"

    # 7. Unrelated Philippine Laws / External Municipal Affairs
    # (e.g. RA 9165 Comprehensive Dangerous Drugs Act, or who is the mayor of Talibon)
    external_civic_patterns = [
        r'\bwho\s+is\s+the\s+(mayor|vice\s+mayor|governor|senator|congressman)\b',
        r'\bwhat\s+is\s+republic\s+act\s+(9165|10175|8484|6713|9262)\b',
        r'\bhow\s+to\s+apply\s+for\s+a\s+(passport|driver\'s\s+license|postal\s+id|nbi\s+clearance)\b'
    ]
    for pat in external_civic_patterns:
        if re.search(pat, q):
            return True, "External Civic, Municipal Official, or Non-Campus Legal Inquiry"

    return False, None


def get_institutional_refusal_message(reason: Optional[str] = None) -> str:
    """
    Constructs a clear, polite, and authoritative institutional refusal message
    guiding the user back to TPC policy matters.
    """
    reason_clause = f" Regarding *{reason}*, that" if reason else " That"
    return (
        f"🏛️ **Institutional Scope Notice:**{reason_clause} inquiry falls outside the authorized "
        f"operational scope of **TPoliCynav** (The TPC Policy Navigator).\n\n"
        f"I am an institutional conversational agent dedicated strictly to **Talibon Polytechnic College (TPC)** "
        f"publications and verified local student ordinances.\n\n"
        f"💡 **You may ask me about:**\n"
        f"• 🎓 **Admissions & Degree Programs:** Freshman requirements, TPCAT, 7 Bachelor's degrees\n"
        f"• 👔 **School Uniform Standards:** Type A uniform specifications & exam attire prohibitions\n"
        f"• 🏠 **Boarding House Guidelines:** Curfew hours (10:00 PM) & safety (Talibon Ordinance 127)\n"
        f"• 💰 **Student Subsidies:** CHED Free Higher Education (RA 10931) & GSIS STEM Grants\n"
        f"• ⚖️ **Academic & Discipline Policies:** Retention GWA, grading systems, and sanction matrix\n\n"
        f"*For inquiries outside official TPC publications, please consult the **TPC Registrar's Office** "
        f"(`registrar@tpc.edu.ph`) or the **Office of Student Affairs and Services (OSAS)**.*"
    )


def verify_lexical_alignment(query: str, retrieved_docs: List[Any], min_content_words: int = 1) -> bool:
    """
    Verifies that the retrieved documents have actual content word overlap with the user query,
    preventing spurious extraction of random sentences from dense vector proximity.
    """
    if not retrieved_docs:
        return False

    stopwords = {
        "what", "is", "the", "are", "can", "for", "and", "under", "in", "of", "a",
        "an", "to", "how", "do", "i", "you", "we", "he", "she", "they", "it",
        "about", "my", "your", "does", "did", "have", "has", "had", "would",
        "should", "could", "there", "their", "this", "that", "these", "those",
        "where", "when", "why", "which", "who", "whom", "whose", "be", "been",
        "being", "am", "was", "were", "tell", "me", "give", "please", "kindly"
    }

    query_words = set(re.findall(r'[a-zA-Z]{3,}', query.lower())) - stopwords
    if not query_words:
        # If query has no substantive words, rely on domain keyword presence
        return any(w in query.lower() for w in IN_SCOPE_KEYWORDS)

    # Check across top 2 retrieved documents
    combined_doc_text = " ".join([
        (getattr(d, "page_content", "") or d.get("text", "")).lower()
        for d in retrieved_docs[:2]
    ])

    matched_words = query_words.intersection(set(re.findall(r'[a-zA-Z]{3,}', combined_doc_text)))
    return len(matched_words) >= min_content_words
