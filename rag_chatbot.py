"""
Root shortcut to launch TPoliCynav RAG Chatbot (Hybrid Online/Offline)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.rag_chatbot import TPoliCynavBot, parse_args

if __name__ == "__main__":
    args = parse_args()
    selected_mode = "offline" if args.offline else ("online" if args.online else args.mode)
    bot = TPoliCynavBot(mode=selected_mode)
    bot.chat_loop()
