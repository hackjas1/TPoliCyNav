"""
TPoliCynav — Root Entry Point for Streamlit Web Application
Talibon Polytechnic College (TPC) Institutional Policy Conversational Agent
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.streamlit_app import run_app

# Unconditionally invoke run_app on every Streamlit script execution / rerun
run_app()
