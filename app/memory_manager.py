"""
=============================================================================
TPoliCynav — Multi-Turn Conversational Memory & Coreference Resolution
Checkpoint 3: Deliverable 12
=============================================================================
Maintains dialogue history and reformulates context-dependent follow-up questions
into standalone semantic retrieval queries.
=============================================================================
"""

import re
from typing import List, Dict, Any


class ConversationTurn:
    """Represents a single turn in a student-bot dialogue."""
    def __init__(self, user_query: str, bot_response: str, sources: List[str] = None):
        self.user_query = user_query
        self.bot_response = bot_response
        self.sources = sources or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_query": self.user_query,
            "bot_response": self.bot_response,
            "sources": self.sources
        }


class ConversationalMemoryManager:
    """
    Manages session dialogue history with sliding window memory and
    contextual coreference resolution for institutional policy inquiries.
    """

    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history: List[ConversationTurn] = []

    def add_turn(self, user_query: str, bot_response: str, sources: List[str] = None):
        """Add a completed turn to history, maintaining sliding window."""
        turn = ConversationTurn(user_query, bot_response, sources)
        self.history.append(turn)
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_history_summary(self) -> str:
        """Format history turns into a clean text transcript."""
        if not self.history:
            return ""
        lines = []
        for i, turn in enumerate(self.history, 1):
            lines.append(f"Turn {i} - Student: {turn.user_query}")
            lines.append(f"Turn {i} - Assistant: {turn.bot_response[:180]}...")
        return "\n".join(lines)

    def contextualize_query(self, current_query: str) -> str:
        """
        Reformulates an ambiguous or pronoun-heavy follow-up question
        into a standalone retrieval query using recent conversational context.

        Example:
            Turn 1: "What is the dress code policy for entrance exams?"
            Turn 2: "Can I wear ripped jeans?"
            Reformulated: "Can I wear ripped jeans during TPC entrance exams dress code?"
        """
        if not self.history:
            return current_query

        last_turn = self.history[-1]
        last_query = last_turn.user_query.lower()
        query_lower = current_query.lower()

        # Pronouns or context-dependent signals
        follow_up_signals = [
            r'\b(it|this|that|they|them|these|those)\b',
            r'\b(what about|how about|and what|what if)\b',
            r'^(can i|is it|are they|why|when|where)\b',
            r'\b(under it|for that|in that case|with that)\b'
        ]

        is_follow_up = any(re.search(pat, query_lower) for pat in follow_up_signals) or len(query_lower.split()) <= 4

        if not is_follow_up:
            return current_query

        # Extract dominant context keywords from previous turns
        topics = []
        if any(w in last_query for w in ["dress", "uniform", "clothes", "wear", "pants", "shirt"]):
            topics.append("dress code uniform policy")
        if any(w in last_query for w in ["exam", "tpcat", "admission", "freshmen", "entrance"]):
            topics.append("admissions entrance exam")
        if any(w in last_query for w in ["curfew", "boarding", "dormitory", "ordinance"]):
            topics.append("boarding house curfew Ordinance 127")
        if any(w in last_query for w in ["scholarship", "subsidy", "gsis", "ched", "gwa"]):
            topics.append("scholarship subsidy GWA requirements")
        if any(w in last_query for w in ["course", "degree", "program", "major"]):
            topics.append("official degree programs offered")
        if any(w in last_query for w in ["sanction", "disciplinary", "infraction", "violation"]):
            topics.append("student disciplinary sanction matrix")

        if topics:
            augmented = f"{current_query} ({', '.join(topics)})"
            return augmented

        # General context fallback: append main subject from previous query
        clean_last = re.sub(r'^(what is|what are|tell me about|how can i|can i)\s+', '', last_query).strip(' ?.')
        return f"{current_query} in relation to {clean_last}"

    def clear(self):
        """Reset conversation memory."""
        self.history.clear()

    def get_turn_count(self) -> int:
        """Return number of stored turns."""
        return len(self.history)

