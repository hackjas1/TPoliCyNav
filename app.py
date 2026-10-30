"""
TPoliCynav — Root entry point for Streamlit Web Application (Railway & Cloud Deployment)
"""
import os
import sys

# Ensure current working directory is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.streamlit_app import *

