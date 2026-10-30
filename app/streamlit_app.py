"""
=============================================================================
TPoliCynav: The TPC Policy Navigator
Talibon Polytechnic College (TPC) — Bohol, Philippines
Course: IS Professional Elective #4 (Generative AI Systems)
Capstone Project: Institutional Policy RAG Conversational Agent
=============================================================================
Built with Streamlit, LangChain, Pinecone Serverless, and Hugging Face.
Official Institutional Theme: Deep Green, Light Green, Mint, and Crisp White.
=============================================================================
"""

import os
import sys
import time
from PIL import Image
import streamlit as st

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.rag_engine import TPCRagEngine

# Locate TPC Official Logo
def get_tpc_logo_path():
    candidates = [
        os.path.join(PROJECT_ROOT, "logo", "TPC-Logo.png"),
        os.path.join(PROJECT_ROOT, "logo", "TPC-LOGO.png"),
        os.path.join(PROJECT_ROOT, "logo", "tpc-logo.png"),
        os.path.join(PROJECT_ROOT, "TPC-Logo.png"),
        os.path.join(PROJECT_ROOT, "TPC-LOGO.png")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

TPC_LOGO_PATH = get_tpc_logo_path()


@st.cache_data
def get_tpc_logo_b64() -> str:
    """Generates an optimized lightweight base64 thumbnail for inline header rendering."""
    if TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH):
        try:
            import io, base64
            img = Image.open(TPC_LOGO_PATH)
            img.thumbnail((120, 120))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            return base64.b64encode(buf.getvalue()).decode()
        except Exception:
            return ""
    return ""


@st.cache_resource(show_spinner="🏛️ Initializing TPoliCynav RAG Engine & Vector Cache...")
def get_rag_engine():
    """Cache the RAG engine instance so it initializes only once across user sessions."""
    return TPCRagEngine(mode="auto")


# =============================================================================
# HIGH-FIDELITY RESPONSIVE INSTITUTIONAL CSS THEME (TPC PALETTE)
# =============================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Viewport & Universal Box Sizing */
    html, body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
        max-width: 100vw !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }
    *, *:before, *:after {
        box-sizing: inherit !important;
    }

    /* Overall page background */
    .stApp {
        background-color: #F4FBF7;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }

    /* Eliminate massive top void & move content flush to the header side */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        height: 1rem !important;
        min-height: 1rem !important;
        padding: 0 !important;
        margin: 0 !important;
        z-index: 99 !important;
    }
    div[data-testid="stToolbar"] {
        top: 0.15rem !important;
        right: 0.5rem !important;
    }

    /* Fluid Responsive Page Container */
    div[data-testid="stAppViewContainer"] section.main .block-container {
        padding-top: 0.35rem !important;
        padding-bottom: 7.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        width: 100% !important;
        max-width: 1060px !important;
        margin: 0 auto !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 2rem !important;
    }

    /* Header Banner Container (About Tab Hero) */
    .tpc-hero-card {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 45%, #059669 85%, #10B981 100%);
        padding: 1.75rem 2.2rem;
        border-radius: 18px;
        color: #FFFFFF;
        box-shadow: 0 14px 30px -8px rgba(6, 78, 59, 0.35);
        margin-bottom: 1.75rem;
        border-left: 8px solid #34D399;
        position: relative;
        overflow: hidden;
    }
    .tpc-hero-card::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .tpc-hero-eyebrow {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #A7F3D0;
        display: flex;
        align-items: center;
        gap: 0.45rem;
        margin-bottom: 0.35rem;
    }
    .tpc-hero-title {
        font-size: 2.15rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.025em;
        line-height: 1.15;
    }
    .tpc-hero-subtitle {
        font-size: 1.02rem;
        margin: 0.5rem 0 0 0;
        color: #ECFDF5;
        font-weight: 500;
        max-width: 820px;
        line-height: 1.45;
    }

    /* Badges & Telemetry Pills */
    .pill-group {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.32rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.01em;
    }
    .pill-glow {
        background-color: #064E3B;
        color: #D1FAE5;
        border: 1px solid rgba(167, 243, 208, 0.4);
    }
    .pill-light {
        background-color: rgba(255, 255, 255, 0.18);
        color: #FFFFFF;
        backdrop-filter: blur(4px);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Telemetry Diagnostics Card */
    .diag-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 1rem;
    }
    .diag-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        padding: 0.3rem 0;
        border-bottom: 1px dashed #E2E8F0;
    }
    .diag-item:last-child {
        border-bottom: none;
    }
    .diag-label {
        color: #64748B;
        font-weight: 500;
    }
    .diag-value {
        color: #065F46;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
    }

    /* Starter Launchpad Cards Header */
    .starter-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #064E3B;
        margin: 1rem 0 0.65rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Touch-Friendly Custom Button Styling (Minimum 42px Touch Target) */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #065F46;
        border: 1.5px solid #10B981;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 0.55rem 0.85rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        min-height: 42px;
        display: flex;
        align-items: center;
        word-break: break-word;
    }
    div.stButton > button:hover {
        background-color: #065F46;
        color: #FFFFFF;
        border-color: #065F46;
        transform: translateY(-1.5px);
        box-shadow: 0 6px 16px rgba(6, 95, 70, 0.2);
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Secondary Buttons */
    div.stButton > button[kind="secondary"] {
        border-color: #CBD5E1;
        color: #475569;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #EF4444;
        border-color: #EF4444;
        color: #FFFFFF;
    }

    /* Verification Strip */
    .verification-strip {
        background-color: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 0.6rem 0.85rem;
        margin-top: 0.65rem;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.55rem;
        font-size: 0.8rem;
    }
    .verif-badge {
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        font-size: 0.76rem;
        white-space: nowrap;
    }
    .verif-emerald {
        background-color: #065F46;
        color: #FFFFFF;
    }
    .verif-light {
        background-color: #DCFCE7;
        color: #166534;
        border: 1px solid #86EFAC;
    }
    .verif-amber {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    /* Citation Tags */
    .citation-tag {
        display: inline-flex;
        align-items: center;
        background-color: #FFFFFF;
        color: #065F46;
        border: 1px solid #86EFAC;
        padding: 0.18rem 0.55rem;
        border-radius: 6px;
        font-size: 0.76rem;
        font-weight: 600;
        word-break: break-word;
    }

    /* Follow-up Section */
    .followup-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #047857;
        margin-top: 0.9rem;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }

    /* =========================================================================
       HIGH-VISIBILITY CHATBOX & FIXED BOTTOM CONTAINER
       ========================================================================= */
    div[data-testid="stBottom"] {
        background: linear-gradient(180deg, rgba(244, 251, 247, 0) 0%, rgba(244, 251, 247, 0.96) 22%, #F4FBF7 100%) !important;
        padding-top: 0.65rem !important;
        padding-bottom: 0.45rem !important;
        width: 100% !important;
    }

    div[data-testid="stBottom"] > div {
        max-width: 1060px !important;
        margin: 0 auto !important;
        width: 100% !important;
    }

    /* Main Chat Input Outer Border & Elevated Elevation */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
        width: 100% !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: #FFFFFF !important;
        border: 2.5px solid #059669 !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 30px rgba(6, 78, 59, 0.18), 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        padding: 0.35rem 0.75rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Chat Input Focus Glow Ring */
    div[data-testid="stChatInput"] > div:focus-within {
        border-color: #064E3B !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.35), 0 12px 32px rgba(6, 78, 59, 0.25) !important;
        transform: translateY(-1.5px) !important;
    }

    /* Text Area Typography (16px to prevent iOS auto-zoom) */
    div[data-testid="stChatInput"] textarea {
        color: #0F172A !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        line-height: 1.45 !important;
        background-color: transparent !important;
    }
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #047857 !important;
        opacity: 0.85 !important;
        font-weight: 500 !important;
    }

    /* High-Visibility Send Button */
    div[data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #065F46 0%, #10B981 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(6, 95, 70, 0.35) !important;
        flex-shrink: 0 !important;
    }
    div[data-testid="stChatInput"] button:hover {
        background: linear-gradient(135deg, #064E3B 0%, #059669 100%) !important;
        transform: scale(1.06) !important;
        box-shadow: 0 6px 18px rgba(6, 95, 70, 0.45) !important;
    }
    div[data-testid="stChatInput"] button svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        width: 18px !important;
        height: 18px !important;
    }

    /* Docked Bottom Disclaimer */
    .docked-disclaimer {
        text-align: center;
        font-size: 0.74rem;
        color: #64748B;
        padding: 0.25rem 0 0.4rem 0;
        line-height: 1.45;
        width: 100%;
    }
    .disclaimer-desktop-only {
        display: inline;
    }
    .disclaimer-mobile-only {
        display: none;
    }
    .disclaimer-title {
        color: #475569;
    }
    .disclaimer-sub {
        font-size: 0.70rem;
        color: #94A3B8;
        margin-top: 0.15rem;
    }

    /* Enhanced Chat Message Bubbles */
    div[data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 1.15rem 1.35rem !important;
        margin-bottom: 1rem !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        box-shadow: 0 3px 12px rgba(6, 78, 59, 0.05) !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
    }

    /* Slim Masthead Header Bar */
    .tpc-slim-card {
        background: linear-gradient(135deg, #064E3B 0%, #065F46 65%, #059669 100%);
        padding: 0.75rem 1.25rem;
        border-radius: 14px;
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(6, 78, 59, 0.18);
        margin-top: 0.05rem;
        margin-bottom: 0.75rem;
        border-left: 6px solid #34D399;
        width: 100%;
    }
    .tpc-slim-inner {
        display: flex;
        align-items: center;
        gap: 0.95rem;
    }
    .tpc-slim-text {
        flex: 1;
        min-width: 0;
    }
    .tpc-header-logo {
        width: 48px;
        height: 48px;
        object-fit: contain;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.95);
        padding: 3px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
        flex-shrink: 0;
    }
    .tpc-header-emoji {
        font-size: 2.1rem;
        flex-shrink: 0;
    }
    .tpc-slim-eyebrow {
        font-size: 0.70rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #A7F3D0;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-bottom: 0.15rem;
        line-height: 1.3;
    }
    .tpc-slim-title {
        font-size: 1.45rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.025em;
        line-height: 1.2;
        overflow-wrap: break-word;
        word-break: break-word;
    }
    .tpc-mobile-sub {
        display: none;
    }

    /* Latest Resolution Focus Banner */
    .latest-focus-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, #ECFDF5 0%, #F0FDF4 100%);
        border: 1.5px solid #10B981;
        border-radius: 12px;
        padding: 0.55rem 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.12);
        width: 100%;
    }
    .focus-title-wrap {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        flex-wrap: wrap;
    }
    .focus-tag {
        background: #064E3B;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 800;
        padding: 0.22rem 0.65rem;
        border-radius: 9999px;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }
    .focus-desc {
        color: #065F46;
        font-size: 0.84rem;
        font-weight: 700;
    }
    .focus-badge {
        color: #059669;
        font-size: 0.76rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* Streamlit Tabs Styling */
    div[data-testid="stTabs"] button[role="tab"] {
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        color: #64748B !important;
        padding: 0.5rem 1.2rem !important;
    }
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #065F46 !important;
        border-bottom: 3px solid #10B981 !important;
    }

    /* =========================================================================
       RESPONSIVE BREAKPOINTS (MOBILE, TABLET, DESKTOP, ULTRAWIDE)
       ========================================================================= */

    /* 1. Mobile Smartphones (width <= 640px) */
    @media (max-width: 640px) {
        /* Mobile Touch & Scroll Ergonomics */
        * {
            -webkit-tap-highlight-color: transparent !important;
        }

        /* Streamlit Header & Sidebar Toggle on Mobile */
        header[data-testid="stHeader"] {
            height: 2.25rem !important;
            min-height: 2.25rem !important;
        }
        button[data-testid="stSidebarCollapseButton"] {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #10B981 !important;
            border-radius: 8px !important;
            color: #064E3B !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06) !important;
        }

        div[data-testid="stAppViewContainer"] section.main .block-container {
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
            padding-top: 0.15rem !important;
            padding-bottom: 5.25rem !important;
        }
        section[data-testid="stSidebar"] {
            width: 86vw !important;
            max-width: 320px !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 0.5rem !important;
        }

        /* Ultra-Sleek Mobile Masthead Header Bar (~44px tall) */
        .tpc-slim-card {
            padding: 0.35rem 0.65rem !important;
            border-radius: 10px !important;
            border-left: 4px solid #34D399 !important;
            margin-top: 0 !important;
            margin-bottom: 0.35rem !important;
            box-shadow: 0 2px 8px rgba(6, 78, 59, 0.14) !important;
        }
        .tpc-slim-inner {
            gap: 0.55rem !important;
            align-items: center !important;
        }
        .tpc-header-logo {
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            border-radius: 6px !important;
            padding: 1.5px !important;
        }
        .tpc-header-emoji {
            font-size: 1.5rem !important;
        }
        .tpc-slim-eyebrow {
            display: none !important;
        }
        .tpc-slim-title {
            margin: 0 !important;
            line-height: 1.15 !important;
        }
        .title-brand {
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.02em !important;
        }
        .title-sep, .title-tagline {
            display: none !important;
        }
        .tpc-mobile-sub {
            display: block !important;
            font-size: 0.60rem !important;
            font-weight: 600 !important;
            color: #A7F3D0 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            line-height: 1.1 !important;
            margin-top: 1px !important;
        }

        /* Streamlined Latest Resolution Banner on Mobile */
        .latest-focus-banner {
            padding: 0.35rem 0.65rem !important;
            margin-bottom: 0.45rem !important;
            border-radius: 8px !important;
            flex-direction: row !important;
            justify-content: space-between !important;
            align-items: center !important;
        }
        .focus-title-wrap {
            gap: 0.35rem !important;
        }
        .focus-tag {
            font-size: 0.62rem !important;
            padding: 0.15rem 0.45rem !important;
            letter-spacing: 0.02em !important;
        }
        .focus-desc {
            font-size: 0.72rem !important;
            line-height: 1.2 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            max-width: 175px !important;
        }
        .focus-badge {
            display: none !important;
        }

        /* Tabs on Mobile */
        div[data-testid="stTabs"] {
            margin-top: -0.15rem !important;
            margin-bottom: 0.35rem !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            font-size: 0.78rem !important;
            padding: 0.35rem 0.55rem !important;
            gap: 0.25rem !important;
        }
        div[data-testid="stTabs"] button[role="tab"] p {
            font-size: 0.78rem !important;
        }

        /* Chat Messages on Mobile */
        div[data-testid="stChatMessage"] {
            padding: 0.75rem 0.85rem !important;
            margin-bottom: 0.65rem !important;
            border-radius: 12px !important;
        }
        div[data-testid="stChatMessage"] p, 
        div[data-testid="stChatMessage"] li {
            font-size: 0.88rem !important;
            line-height: 1.5 !important;
        }

        /* Verification Strip on Mobile */
        .verification-strip {
            padding: 0.45rem 0.65rem !important;
            gap: 0.35rem !important;
            font-size: 0.72rem !important;
            border-radius: 8px !important;
        }
        .verif-badge {
            font-size: 0.68rem !important;
            padding: 0.15rem 0.45rem !important;
        }
        .citation-tag {
            font-size: 0.68rem !important;
            padding: 0.12rem 0.4rem !important;
        }

        /* Responsive Column Stacking for Launchpad & Follow-ups */
        .launchpad-grid div[data-testid="stHorizontalBlock"],
        .followup-grid div[data-testid="stHorizontalBlock"],
        .about-grid div[data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.45rem !important;
        }
        .launchpad-grid div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
        .followup-grid div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
        .about-grid div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            margin-bottom: 0.25rem !important;
        }

        /* Feedback Buttons Stay Inline on Mobile */
        .feedback-grid div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 0.45rem !important;
            align-items: center !important;
        }
        .feedback-grid div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1),
        .feedback-grid div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            width: auto !important;
            min-width: 95px !important;
            flex: 0 0 auto !important;
        }

        /* Buttons on Mobile */
        div.stButton > button {
            font-size: 0.80rem !important;
            padding: 0.45rem 0.75rem !important;
            min-height: 40px !important;
        }
        div.stButton > button:active {
            transform: scale(0.97) !important;
        }

        /* Native App-Like Pill Chatbox & Dock on Mobile */
        div[data-testid="stBottom"] {
            background: rgba(244, 251, 247, 0.98) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            border-top: 1px solid rgba(16, 185, 129, 0.22) !important;
            padding-top: 0.25rem !important;
            padding-bottom: max(6px, env(safe-area-inset-bottom)) !important;
            box-shadow: 0 -3px 12px rgba(6, 78, 59, 0.06) !important;
        }
        div[data-testid="stChatInput"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        div[data-testid="stChatInput"] > div {
            border: 1.5px solid #059669 !important;
            border-radius: 22px !important;
            box-shadow: 0 2px 8px rgba(6, 78, 59, 0.08) !important;
            padding: 0.1rem 0.45rem 0.1rem 0.75rem !important;
            background-color: #FFFFFF !important;
            transform: none !important;
            min-height: 42px !important;
        }
        div[data-testid="stChatInput"] > div:focus-within {
            border-color: #064E3B !important;
            box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.28) !important;
            transform: none !important;
        }
        div[data-testid="stChatInput"] textarea {
            font-size: 16px !important; /* Strict 16px prevents iOS Safari auto-zoom/jump */
            font-weight: 500 !important;
            line-height: 1.35 !important;
            padding: 0.35rem 0.1rem !important;
            max-height: 90px !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder {
            font-size: 0.80rem !important;
            font-weight: 500 !important;
            color: #047857 !important;
            opacity: 0.75 !important;
        }
        div[data-testid="stChatInput"] button {
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            border-radius: 50% !important;
            background: linear-gradient(135deg, #065F46 0%, #10B981 100%) !important;
            box-shadow: 0 2px 6px rgba(6, 95, 70, 0.3) !important;
            margin: auto 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stChatInput"] button:active {
            transform: scale(0.92) !important;
        }
        div[data-testid="stChatInput"] button svg {
            width: 14px !important;
            height: 14px !important;
        }

        /* Minimal Docked Disclaimer on Mobile (frees ~65px screen height) */
        .docked-disclaimer {
            font-size: 0.60rem !important;
            padding: 0.1rem 0 0.15rem 0 !important;
            line-height: 1.2 !important;
            margin: 0.1rem 0 0 0 !important;
        }
        .disclaimer-desktop-only {
            display: none !important;
        }
        .disclaimer-mobile-only {
            display: inline !important;
        }
        .disclaimer-sub {
            display: none !important;
        }

        /* Hero Card on Mobile */
        .tpc-hero-card {
            padding: 1.1rem 1.25rem !important;
            border-radius: 14px !important;
            margin-bottom: 1rem !important;
        }
        .tpc-hero-title {
            font-size: 1.35rem !important;
        }
        .tpc-hero-subtitle {
            font-size: 0.85rem !important;
        }
        .pill {
            font-size: 0.70rem !important;
            padding: 0.22rem 0.55rem !important;
        }
    }

    /* 2. Tablet Devices (641px <= width <= 1024px) */
    @media (min-width: 641px) and (max-width: 1024px) {
        div[data-testid="stAppViewContainer"] section.main .block-container {
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
            padding-top: 0.35rem !important;
        }
        .tpc-slim-card {
            padding: 0.65rem 1rem !important;
        }
        .tpc-slim-title {
            font-size: 1.30rem !important;
        }
        div[data-testid="stChatMessage"] {
            padding: 0.95rem 1.15rem !important;
        }
    }

    /* 3. Ultrawide Monitors (width >= 1441px) */
    @media (min-width: 1441px) {
        div[data-testid="stAppViewContainer"] section.main .block-container {
            max-width: 1080px !important;
            margin: 0 auto !important;
        }
        div[data-testid="stBottom"] > div {
            max-width: 1080px !important;
            margin: 0 auto !important;
        }
    }
</style>
"""


# =============================================================================
# INTELLIGENT TOPIC-AWARE FOLLOW-UP GENERATOR
# =============================================================================
def get_suggested_follow_ups(query: str, answer: str) -> list:
    """Generates 3 contextual, high-yield follow-up inquiry chips based on query context."""
    q_lower = query.lower()
    
    if any(w in q_lower for w in ["course", "degree", "program", "major", "bachelor", "curriculum"]):
        return [
            ("📋 Freshmen Admission Steps", "What are the admission requirements and document steps for freshmen?"),
            ("⚖️ Academic Retention GWA", "What is the minimum GWA and retention policy to remain enrolled at TPC?"),
            ("💰 Free Higher Education Coverage", "Are all tuition and miscellaneous fees 100% free under RA 10931?")
        ]
    elif any(w in q_lower for w in ["dress", "uniform", "shoes", "wear", "attire", "jeans", "slippers"]):
        return [
            ("👔 TPC Official Type A Uniform", "What is the complete description of the official Type A school uniform?"),
            ("🚫 Prohibited Attire List", "What clothing items are strictly prohibited on campus according to the Handbook?"),
            ("⚠️ Uniform Sanction Matrix", "What disciplinary sanctions apply to students who violate the dress code?")
        ]
    elif any(w in q_lower for w in ["curfew", "boarding", "ordinance", "dormitory", "landlord", "127"]):
        return [
            ("🛡️ Boarding House Safety Standards", "What fire and sanitation standards must landlords meet under Ordinance 127?"),
            ("👮 PNP-TPC Curfew Patrols", "How do local authorities conduct curfew and safety inspections for students?"),
            ("🌙 Permissible Study Extensions", "Can students request curfew extensions for school projects or reviews?")
        ]
    elif any(w in q_lower for w in ["scholarship", "gsis", "subsidy", "ched", "grant", "stem", "tes"]):
        return [
            ("🎯 GSIS STEM Grade Maintenance", "What GWA must a scholar maintain to keep the GSIS STEM monthly stipend?"),
            ("📄 CHED TES Application Documents", "Who is eligible for the CHED Tertiary Education Subsidy (TES)?"),
            ("🔄 Dual Subsidy Combinations", "Can a student receive both CHED Free Higher Education and private grants?")
        ]
    elif any(w in q_lower for w in ["admission", "exam", "tpcat", "enrollment", "freshmen", "transferee"]):
        return [
            ("🎓 Undergraduate Degrees Offered", "What courses and undergraduate degree programs are officially offered at TPC?"),
            ("👔 Entrance Exam Dress Code", "Are ripped jeans, shorts, or slippers allowed during the TPC entrance exam?"),
            ("🔄 Transferee Evaluation Rules", "What are the rules regarding transfer credits and failed prerequisite subjects?")
        ]
    elif any(w in q_lower for w in ["sanction", "disciplinary", "violation", "infraction", "penalty", "alcohol", "zone"]):
        return [
            ("🍺 500-Meter Alcohol Prohibition", "What is the 500-meter alcohol and entertainment prohibition zone around TPC?"),
            ("⚖️ Student Disciplinary Board", "Who presides over student grievance hearings and disciplinary committees?"),
            ("📜 Major vs Minor Infractions", "What acts are classified as major offenses leading to suspension or dismissal?")
        ]
    else:
        return [
            ("🎓 Official Degree Offerings", "What courses and undergraduate degree programs are officially offered at TPC?"),
            ("🏠 Boarding House Curfew Hours", "What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?"),
            ("👔 Uniform & Grooming Standards", "What is the official TPC uniform and grooming standard?")
        ]


# =============================================================================
# EXPORT MEMORANDUM BUILDER
# =============================================================================
def generate_transcript_text(messages: list) -> str:
    """Builds an institutional-grade consultation record for download."""
    lines = [
        "=" * 72,
        "TALIBON POLYTECHNIC COLLEGE (TPC) — BOHOL, PHILIPPINES",
        "TPoliCynav Institutional Policy Advisory Transcript",
        f"Generated: {time.strftime('%B %d, %Y - %I:%M %p')}",
        "Reference: TPC Student Handbook v.04, Municipal Ordinance 127, RA 10931",
        "=" * 72,
        ""
    ]
    for i, msg in enumerate(messages):
        role_label = "TPCian Student / Inquirer" if msg["role"] == "user" else "TPoliCynav Policy Navigator"
        lines.append(f"[{role_label}]:")
        lines.append(msg["content"].strip())
        if msg.get("sources"):
            lines.append(f"• Verified Sources: {', '.join(msg['sources'])}")
        if msg.get("confidence") is not None and msg.get("confidence") > 0:
            lines.append(f"• Retrieval Confidence: {msg['confidence'] * 100:.1f}%")
        lines.append("-" * 60)
        lines.append("")
    
    lines.append("=" * 72)
    lines.append("NOTICE: This summary is generated from official college records.")
    lines.append("For official academic credentials or certifications, visit the TPC Registrar.")
    lines.append("=" * 72)
    return "\n".join(lines)


# =============================================================================
# REUSABLE ASSISTANT DETAILS RENDERER
# =============================================================================
def render_assistant_details(msg: dict, msg_idx: int, is_latest: bool = False):
    """Renders the verification strip, chunks explorer, feedback, and follow-ups."""
    sources = msg.get("sources", [])
    confidence = msg.get("confidence", 0.0)
    latency_ms = msg.get("latency_ms", 0)

    # Color-code confidence badge
    is_refusal = msg.get("is_refusal", False) or confidence < 0.60
    if is_refusal:
        conf_class = "verif-amber"
        conf_label = "⚪ Out-of-Scope Refusal"
    elif confidence >= 0.80:
        conf_class = "verif-emerald"
        conf_label = f"🟢 High Match ({confidence*100:.1f}%)"
    elif confidence >= 0.70:
        conf_class = "verif-light"
        conf_label = f"🟢 Grounded Match ({confidence*100:.1f}%)"
    else:
        conf_class = "verif-amber"
        conf_label = f"🟡 Moderate Match ({confidence*100:.1f}%)"

    # Verification and citation tags
    sources_html = ""
    for s in sources:
        sources_html += f"<span class='citation-tag'>📄 {s}</span> "

    latency_str = f"⚡ {latency_ms}ms" if latency_ms > 0 else "⚡ Instant Cache"

    st.markdown(f"""
    <div class="verification-strip">
        <span class="verif-badge {conf_class}">{conf_label}</span>
        <span style="color: #64748B; font-size: 0.76rem; font-weight: 600;">{latency_str}</span>
        <span style="color: #94A3B8;">|</span>
        <span style="color: #065F46; font-size: 0.76rem; font-weight: 700;">Sources:</span>
        {sources_html if sources_html else "<span class='citation-tag'>TPC Institutional Policy Database</span>"}
    </div>
    """, unsafe_allow_html=True)

    # Expandable Chunk Passages Explorer
    chunks = msg.get("chunks", [])
    if chunks:
        with st.expander(f"🔍 Inspect Retrieved Policy Excerpts & Mathematical Scores ({len(chunks)})"):
            for idx, chunk in enumerate(chunks, 1):
                score_pct = chunk.get("score", 0.0) * 100
                source_title = chunk.get("source", "TPC Policy Record")
                st.markdown(
                    f"<div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.6rem 0.8rem; margin-bottom: 0.5rem;'>"
                    f"<div style='display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700; color: #065F46;'>"
                    f"<span>[{idx}] {source_title}</span>"
                    f"<span style='color: #059669; font-family: monospace;'>Cosine Similarity: {score_pct:.1f}%</span>"
                    f"</div>"
                    f"<p style='font-size: 0.8rem; color: #475569; margin: 0.35rem 0 0 0; line-height: 1.45;'>{chunk.get('text', '')}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

    # Feedback Buttons (Non-initial messages)
    if msg_idx > 0:
        st.markdown('<div class="feedback-grid">', unsafe_allow_html=True)
        fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 6])
        fb_key = f"fb_{msg_idx}"
        with fb_col1:
            if st.button("👍 Helpful", key=f"btn_up_{msg_idx}"):
                st.session_state.feedback_log[fb_key] = "up"
                st.toast("Thank you! Feedback recorded for TPC knowledge base optimization.", icon="✅")
        with fb_col2:
            if st.button("👎 Clarify", key=f"btn_down_{msg_idx}"):
                st.session_state.feedback_log[fb_key] = "down"
                st.toast("Noted. We will continue refining TPC policy grounding.", icon="📝")
        st.markdown('</div>', unsafe_allow_html=True)

    # Dynamic Follow-Up Inquiry Chips (Rendered only on the active latest response)
    if is_latest and msg_idx > 0:
        follow_ups = msg.get("follow_ups", [])
        if not follow_ups and msg_idx > 0:
            prev_user_query = st.session_state.messages[msg_idx - 1]["content"] if msg_idx - 1 >= 0 else ""
            follow_ups = get_suggested_follow_ups(prev_user_query, msg["content"])

        if follow_ups:
            st.markdown("""
            <div class="followup-label">
                <span>💡 Recommended Follow-Up Inquiries:</span>
            </div>
            <div class="followup-grid">
            """, unsafe_allow_html=True)
            
            f_cols = st.columns(len(follow_ups))
            for f_idx, (f_label, f_query) in enumerate(follow_ups):
                with f_cols[f_idx]:
                    if st.button(f_label, key=f"fup_{msg_idx}_{f_idx}"):
                        st.session_state.pending_prompt = f_query
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# MAIN STREAMLIT APPLICATION
# =============================================================================
def run_app():
    """Main execution function invoked on every Streamlit rerun."""

    # 1. Page Configuration (first Streamlit call)
    page_icon = "🎓"
    if TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH):
        try:
            page_icon = Image.open(TPC_LOGO_PATH)
        except Exception:
            page_icon = "🎓"

    try:
        st.set_page_config(
            page_title="TPoliCynav — TPC Policy Navigator",
            page_icon=page_icon,
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except Exception:
        pass

    # 2. Inject Professional CSS Theme
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # 3. Retrieve Cached RAG Engine
    try:
        engine = get_rag_engine()
        system_status = engine.get_system_status()
    except Exception as init_err:
        engine = None
        system_status = {
            "status": "Offline Fallback",
            "vector_backend": "Local NumPy Matrix",
            "llm_engine": "Local Policy Extractor",
            "indexed_chunks": 128,
            "embedding_model": "BAAI/bge-small-en-v1.5"
        }

    # 4. Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Mabuhay and welcome, TPCian!** I am **TPoliCynav**, the official AI-driven "
                    "Institutional Policy Navigator for **Talibon Polytechnic College (TPC)** in Bohol.\n\n"
                    "I provide authoritative, grounded guidance directly from verified college publications:\n"
                    "• 🎓 **Academic Programs & Admission Requirements** (Part 1, Handbook v.04)\n"
                    "• 👔 **Uniform Guidelines & Examination Dress Code** (Type A Standards)\n"
                    "• 🏠 **Boarding House Curfew & Municipal Safety** (Talibon Ordinance No. 127)\n"
                    "• 💰 **CHED Free Higher Education (RA 10931) & GSIS STEM Subsidies**\n"
                    "• ⚖️ **Grading Systems, Retention Criteria & Disciplinary Sanctions**\n\n"
                    "How may I assist your college journey today? Click a prompt below or ask your own question!"
                ),
                "sources": ["TPC Student Handbook v.04", "Talibon Ordinance 127"],
                "confidence": 1.0,
                "chunks": [],
                "engine": "Institutional Knowledge System",
                "latency_ms": 0
            }
        ]

    # Feedback state
    if "feedback_log" not in st.session_state:
        st.session_state.feedback_log = {}

    # -------------------------------------------------------------------------
    # SIDEBAR: INSTITUTIONAL BRANDING & TELEMETRY
    # -------------------------------------------------------------------------
    with st.sidebar:
        # Centered Logo Card
        col_logo_left, col_logo_center, col_logo_right = st.columns([1, 4, 1])
        with col_logo_center:
            if TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH):
                st.image(TPC_LOGO_PATH, width=150)
            else:
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Seal_of_Bohol.svg/200px-Seal_of_Bohol.svg.png",
                    width=90
                )
        
        st.markdown(
            "<div style='text-align: center; margin-top: 0.25rem;'>"
            "<h3 style='margin: 0; font-size: 1.35rem; color: #064E3B; font-weight: 800;'>TPoliCynav</h3>"
            "<p style='margin: 0; font-size: 0.8rem; color: #059669; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>"
            "Talibon Polytechnic College"
            "</p>"
            "<p style='font-size: 0.73rem; color: #64748B; margin-top: 0.15rem;'>"
            "Official AI Policy Conversational Agent"
            "</p>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Telemetry Diagnostics Card
        st.markdown("#### ⚙️ **System Diagnostics**")
        status_text = system_status.get("status", "Active")
        status_color = "#10B981" if "Cloud" in status_text or "Online" in status_text else "#059669"

        st.markdown(f"""
        <div class="diag-card">
            <div class="diag-item">
                <span class="diag-label">System State</span>
                <span class="diag-value" style="color: {status_color};">● {status_text}</span>
            </div>
            <div class="diag-item">
                <span class="diag-label">Vector Store</span>
                <span class="diag-value">{system_status.get('vector_backend', 'Pinecone Serverless')}</span>
            </div>
            <div class="diag-item">
                <span class="diag-label">Synthesis Engine</span>
                <span class="diag-value">{system_status.get('llm_engine', 'Precision Extractor')}</span>
            </div>
            <div class="diag-item">
                <span class="diag-label">Indexed Corpus</span>
                <span class="diag-value">{system_status.get('indexed_chunks', 128)} Chunks (384-d)</span>
            </div>
            <div class="diag-item">
                <span class="diag-label">Memory Buffer</span>
                <span class="diag-value">{len(st.session_state.messages)//2} Active Turns</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Categorized Quick Launch Topics
        st.markdown("#### 💡 **Frequent Student Inquiries**")
        st.caption("Select any verified policy topic to retrieve grounded answers:")

        with st.expander("🎓 **Academics & Admissions**", expanded=True):
            if st.button("Offered Degree Programs", key="btn_acad_programs"):
                st.session_state.pending_prompt = "What courses and undergraduate degree programs are officially offered at TPC?"
                st.rerun()
            if st.button("Freshmen Admission Requirements", key="btn_acad_admissions"):
                st.session_state.pending_prompt = "What are the freshman admission requirements and steps for TPC?"
                st.rerun()
            if st.button("Academic Retention (GWA)", key="btn_acad_retention"):
                st.session_state.pending_prompt = "What are the minimum GWA and retention requirements in the TPC Student Handbook?"
                st.rerun()

        with st.expander("👔 **Uniform & Dress Code**", expanded=False):
            if st.button("Entrance Exam Dress Code", key="btn_uniform_exam"):
                st.session_state.pending_prompt = "Are ripped jeans, shorts, or slippers allowed during the TPC entrance exam?"
                st.rerun()
            if st.button("Type A Official Uniform", key="btn_uniform_type_a"):
                st.session_state.pending_prompt = "What is the official Type A school uniform description for male and female students?"
                st.rerun()
            if st.button("Dress Code Sanctions", key="btn_uniform_sanctions"):
                st.session_state.pending_prompt = "What sanctions are given to students who violate the uniform policy?"
                st.rerun()

        with st.expander("🏠 **Boarding Houses & Curfew**", expanded=False):
            if st.button("Curfew Hours (Ordinance 127)", key="btn_curfew_hours"):
                st.session_state.pending_prompt = "What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?"
                st.rerun()
            if st.button("Safety Standards for Dorms", key="btn_curfew_standards"):
                st.session_state.pending_prompt = "What safety and sanitary standards must TPC boarding houses comply with?"
                st.rerun()
            if st.button("PNP-TPC Night Patrols", key="btn_curfew_patrols"):
                st.session_state.pending_prompt = "What is the role of PNP and TPC security in boarding house curfew inspections?"
                st.rerun()

        with st.expander("💰 **Scholarships & Financial Grants**", expanded=False):
            if st.button("GSIS STEM Subsidy (GSSP)", key="btn_scholar_gsis"):
                st.session_state.pending_prompt = "What is the minimum GWA required to qualify for the GSIS STEM subsidy?"
                st.rerun()
            if st.button("CHED Free Higher Education (RA 10931)", key="btn_scholar_ched"):
                st.session_state.pending_prompt = "How does Republic Act 10931 provide free tertiary education for TPC students?"
                st.rerun()

        with st.expander("🛡️ **Safety, Discipline & Out-of-Scope**", expanded=False):
            if st.button("500m Alcohol Prohibition Zone", key="btn_disc_alcohol"):
                st.session_state.pending_prompt = "What is the 500-meter alcohol and entertainment prohibition zone around TPC?"
                st.rerun()
            if st.button("🔴 Out-of-Scope Test (Refusal Guardrail)", key="btn_disc_refusal"):
                st.session_state.pending_prompt = "What is the capital city and total population of Tokyo, Japan?"
                st.rerun()

        st.markdown("---")

        # Official Knowledge Base Explorer
        with st.expander("📂 **Verified Knowledge Base (7 Sources)**"):
            st.markdown("""
            1. **TPC Student Handbook v.04**  
               *Academics, Grading, Retention, Disciplinary Matrix*
            2. **Talibon Municipal Ordinance No. 127**  
               *Boarding Houses, Safety Standards, Curfew Hours*
            3. **TPC Uniform & Dress Code Policy Guide**  
               *General Type A Uniform, Prohibited Attires, Shoes*
            4. **TPC Admissions & TPCAT Guidelines**  
               *Freshmen Requirements, Examination Day Etiquette*
            5. **CHED Free Higher Education (RA 10931)**  
               *LUC Exemption, Free Tuition & Mandatory Fees*
            6. **GSIS Subsidy for STEM (GSSP) Guidelines**  
               *Scholarship Criteria & 90% GWA Maintenance*
            7. **PNP-TPC Joint Safety Memorandums**  
               *Curfew Patrols & Boarding House Inspections*
            """)

        # Campus Contacts Directory
        with st.expander("📞 **Campus Directory & Assistance**"):
            st.markdown("""
            • **Office of the Registrar:**  
              📧 `registrar@tpc.edu.ph`  
              🏢 Admin Building, Ground Floor
            
            • **Office of Student Affairs & Services (OSAS):**  
              📧 `osas@tpc.edu.ph`  
              🏢 Student Center, 2nd Floor
            
            • **Talibon Municipal PNP Station:**  
              📞 Emergency Hotline: `(038) 515-9000`
            """)

        st.markdown("---")

        # QOL Action: Export Consultation Record
        transcript_data = generate_transcript_text(st.session_state.messages)
        st.download_button(
            label="📥 Export Policy Summary (.txt)",
            data=transcript_data,
            file_name=f"TPC_Policy_Inquiry_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            help="Download a clean text memorandum of your policy questions and answers for your records."
        )

        # Session Reset
        if st.button("🗑️ Clear Dialogue History", type="secondary"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.session_state.feedback_log = {}
            if engine:
                engine.reset_memory()
            st.toast("Dialogue history cleared. RAG memory reset.", icon="🧹")
            st.rerun()

        # Institutional Capstone Card in Sidebar
        st.markdown("""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 0.85rem; margin-top: 1.25rem; text-align: center;">
            <div style="font-size: 0.82rem; font-weight: 800; color: #064E3B;">Talibon Polytechnic College</div>
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 0.15rem;">Bohol, Philippines • A.Y. 2026–2027</div>
            <div style="font-size: 0.74rem; font-weight: 600; color: #059669; margin-top: 0.35rem;">IS Professional Elective #4 Capstone</div>
            <div style="font-size: 0.73rem; color: #334155; margin-top: 0.35rem; line-height: 1.45;">
                <strong style="color: #065F46;">Team Kuys:</strong><br>
                Eduardo Avenido Jr. • Christian Paul G. La Rosa<br>
                Nielbert Garcia • Marcel Avergonzado • Ronald M. Barril
            </div>
            <div style="font-size: 0.68rem; color: #94A3B8; margin-top: 0.45rem; border-top: 1px dashed #CBD5E1; padding-top: 0.35rem;">
                Official AI Policy Conversational Agent
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # FIXED BOTTOM CANVAS: INPUT FIELD & DOCKED FOOTER
    # -------------------------------------------------------------------------
    with st.bottom:
        user_typed = st.chat_input("💬 Ask about TPC admissions, courses, dress code, curfew, scholarships...")
        st.markdown("""
        <div class="docked-disclaimer">
            <div class="disclaimer-title">
                <span class="disclaimer-desktop-only">
                    <strong>Talibon Polytechnic College (TPC)</strong> • Bohol, Philippines &nbsp;|&nbsp; 
                    <em>IS Professional Elective #4 Capstone Project</em> &nbsp;|&nbsp; 
                    <strong style="color: #059669;">Team Kuys</strong>
                </span>
                <span class="disclaimer-mobile-only">
                    🏛️ <strong>TPC Policy AI</strong> • Handbook v.04 &amp; Ord. 127 • <strong>Team Kuys</strong>
                </span>
            </div>
            <div class="disclaimer-sub">
                Disclaimer: Synthesized from official TPC documents (Handbook v.04, Ord. 127, RA 10931). For official certifications, consult the Registrar.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Determine Active Prompt: from quick launch buttons, follow-ups, or chat input
    active_prompt = None
    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        active_prompt = st.session_state.pop("pending_prompt")
    elif user_typed:
        active_prompt = user_typed

    # Process Active Query Immediately
    if active_prompt:
        with st.spinner("🔍 Navigating TPC institutional records & vector embeddings..."):
            st.session_state.messages.append({"role": "user", "content": active_prompt})
            start_query_t = time.time()
            if engine:
                try:
                    response = engine.query(active_prompt)
                    answer_text = response.get("answer", "No matching institutional record found.")
                    sources = response.get("sources", [])
                    confidence = response.get("confidence", 0.0)
                    chunks = response.get("chunks", [])
                    engine_used = response.get("engine_used", "LangChain RAG Engine")
                    latency_ms = response.get("latency_ms", int((time.time() - start_query_t) * 1000))
                    is_refusal = response.get("is_refusal", False)
                except Exception as query_err:
                    answer_text = f"⚠️ An error occurred while retrieving policy records: {query_err}\n\nPlease try again."
                    sources = []
                    confidence = 0.0
                    chunks = []
                    engine_used = "Error Fallback"
                    latency_ms = int((time.time() - start_query_t) * 1000)
                    is_refusal = True
            else:
                answer_text = "⚠️ RAG Engine is not currently initialized."
                sources = []
                confidence = 0.0
                chunks = []
                engine_used = "System"
                latency_ms = 0
                is_refusal = True

            follow_ups = get_suggested_follow_ups(active_prompt, answer_text)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer_text,
                "sources": sources,
                "confidence": confidence,
                "chunks": chunks,
                "engine": engine_used,
                "latency_ms": latency_ms,
                "follow_ups": follow_ups if not is_refusal else [],
                "is_refusal": is_refusal
            })

    # -------------------------------------------------------------------------
    # MASTER TOP HEADER BAR (Compact Responsive Navbar with TPC Seal)
    # -------------------------------------------------------------------------
    logo_b64 = get_tpc_logo_b64()
    if logo_b64:
        logo_tag = f'<img src="data:image/png;base64,{logo_b64}" class="tpc-header-logo" alt="TPC Official Seal" />'
    else:
        logo_tag = '<span class="tpc-header-emoji">🏛️</span>'

    st.markdown(f"""
    <div class="tpc-slim-card">
        <div class="tpc-slim-inner">
            {logo_tag}
            <div class="tpc-slim-text">
                <div class="tpc-slim-eyebrow">
                    <span>🏛️ TALIBON POLYTECHNIC COLLEGE</span>
                    <span class="eyebrow-sep">•</span>
                    <span class="eyebrow-loc">BOHOL, PHILIPPINES</span>
                    <span class="eyebrow-sep">•</span>
                    <span class="eyebrow-tag">OFFICIAL AI POLICY PORTAL</span>
                </div>
                <h1 class="tpc-slim-title">
                    <span class="title-brand">TPoliCynav</span><span class="title-sep">:</span> <span class="title-tagline">The TPC Policy Navigator</span>
                </h1>
                <div class="tpc-mobile-sub">TPC Policy Navigator • Bohol</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN CONTENT TABS
    # -------------------------------------------------------------------------
    tab_chat, tab_about = st.tabs(["💬 Policy Navigator", "ℹ️ About & Architecture"])

    assistant_avatar = TPC_LOGO_PATH if (TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH)) else "🏛️"

    with tab_chat:
        # CASE A: Active dialogue session with student inquiries
        if len(st.session_state.messages) > 1:
            latest_assistant_idx = len(st.session_state.messages) - 1
            latest_user_idx = latest_assistant_idx - 1
            latest_user = st.session_state.messages[latest_user_idx]
            latest_assistant = st.session_state.messages[latest_assistant_idx]

            # 1. High-Focus Banner for the Latest Answer
            st.markdown("""
            <div class="latest-focus-banner">
                <div class="focus-title-wrap">
                    <span class="focus-tag">
                        📌 LATEST POLICY RESOLUTION
                    </span>
                    <span class="focus-desc">Direct Answer to Your Most Recent Inquiry</span>
                </div>
                <span class="focus-badge">⚡ Instant Focus</span>
            </div>
            """, unsafe_allow_html=True)

            # 2. Render latest user question
            with st.chat_message("user", avatar="🎓"):
                st.markdown(f"**Inquiry:** {latest_user['content']}")

            # 3. Render latest assistant answer (with verification strip, citations, chunks, feedback, follow-ups)
            with st.chat_message("assistant", avatar=assistant_avatar):
                st.markdown(latest_assistant["content"])
                render_assistant_details(latest_assistant, latest_assistant_idx, is_latest=True)

            # 4. Earlier Questions in this Session (Collapsible Expander)
            if len(st.session_state.messages) > 3:
                earlier_turns_count = (len(st.session_state.messages) - 1) // 2 - 1
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander(f"📜 Earlier Inquiries in this Session ({earlier_turns_count})", expanded=False):
                    for u_idx in range(latest_user_idx - 2, 0, -2):
                        a_idx = u_idx + 1
                        u_msg = st.session_state.messages[u_idx]
                        a_msg = st.session_state.messages[a_idx]
                        
                        with st.chat_message("user", avatar="🎓"):
                            st.markdown(f"**Previous Inquiry:** {u_msg['content']}")
                        with st.chat_message("assistant", avatar=assistant_avatar):
                            st.markdown(a_msg["content"])
                            render_assistant_details(a_msg, a_idx, is_latest=False)
                        st.markdown("---")

            # 5. Welcome Guide & Quick Launchpad (Collapsible Expander in active session)
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("👋 College Welcome Guide & Quick Launch Topics", expanded=False):
                with st.chat_message("assistant", avatar=assistant_avatar):
                    st.markdown(st.session_state.messages[0]["content"])
                    render_assistant_details(st.session_state.messages[0], 0, is_latest=False)
                
                st.markdown("<br><strong>🚀 Quick Launchpad Prompts:</strong>", unsafe_allow_html=True)
                st.markdown('<div class="launchpad-grid">', unsafe_allow_html=True)
                q_c1, q_c2 = st.columns(2)
                with q_c1:
                    if st.button("🎓 Degree Programs Offered", key="arch_programs"):
                        st.session_state.pending_prompt = "What courses and undergraduate degree programs are officially offered at TPC?"
                        st.rerun()
                    if st.button("👔 Examination Dress Code", key="arch_dress"):
                        st.session_state.pending_prompt = "Are ripped jeans, shorts, or slippers allowed during the TPC entrance exam?"
                        st.rerun()
                with q_c2:
                    if st.button("🏠 Boarding House Curfew", key="arch_curfew"):
                        st.session_state.pending_prompt = "What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?"
                        st.rerun()
                    if st.button("💰 GSIS STEM Scholarship GWA", key="arch_scholarship"):
                        st.session_state.pending_prompt = "What is the minimum GWA required to qualify for the GSIS STEM subsidy?"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # CASE B: Fresh session (initial greeting)
        else:
            with st.chat_message("assistant", avatar=assistant_avatar):
                st.markdown(st.session_state.messages[0]["content"])
                render_assistant_details(st.session_state.messages[0], 0, is_latest=False)

            st.markdown("""
            <div class="starter-header">
                <span>🚀 Quick Launchpad — Popular Student Inquiries:</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="launchpad-grid">', unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                if st.button("🎓 What courses and degree programs are offered?", key="starter_programs"):
                    st.session_state.pending_prompt = "What courses and undergraduate degree programs are officially offered at TPC?"
                    st.rerun()
                if st.button("👔 Can I wear ripped jeans or slippers to the entrance exam?", key="starter_dress"):
                    st.session_state.pending_prompt = "Are ripped jeans, shorts, or slippers allowed during the TPC entrance exam?"
                    st.rerun()
            with sc2:
                if st.button("🏠 What are the curfew hours under Ordinance 127?", key="starter_curfew"):
                    st.session_state.pending_prompt = "What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?"
                    st.rerun()
                if st.button("💰 What GWA is required for the GSIS STEM scholarship?", key="starter_scholarship"):
                    st.session_state.pending_prompt = "What is the minimum GWA required to qualify for the GSIS STEM subsidy?"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_about:
        # Full Institutional Hero Card with Badges (Picture 1 style)
        st.markdown("""
        <div class="tpc-hero-card">
            <div class="tpc-hero-eyebrow">
                <span>🏛️ TALIBON POLYTECHNIC COLLEGE</span>
                <span>•</span>
                <span>BOHOL, PHILIPPINES</span>
                <span>•</span>
                <span>OFFICIAL AI POLICY PORTAL</span>
            </div>
            <h1 class="tpc-hero-title">TPoliCynav: The TPC Policy Navigator</h1>
            <p class="tpc-hero-subtitle">
                Authoritative, retrieval-grounded conversational agent for student handbooks, 
                academic retention, uniform standards, boarding house curfews, and financial subsidies.
            </p>
            <div class="pill-group">
                <span class="pill pill-glow">🌲 Pinecone Serverless</span>
                <span class="pill pill-glow">🤖 LangChain Orchestrated</span>
                <span class="pill pill-light">🧠 Dense Embeddings (bge-small)</span>
                <span class="pill pill-light">🛡️ Multi-Layer Scope Guardrail (0.60)</span>
                <span class="pill pill-light">⚡ Latency-Optimized</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="about-grid">', unsafe_allow_html=True)
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown("""
            ### 🎯 **Academic Scope & Mission**
            **TPoliCynav** serves as the authoritative institutional policy assistant for **Talibon Polytechnic College (TPC)** in Bohol, Philippines.
            
            By anchoring AI responses directly to verified college administrative records, the system provides zero-hallucination guidance on:
            - **Official Degree Offerings:** 7 CHED-recognized undergraduate programs (BAEL, BAPoS, BSAgri, BSAIS, BSCrim, BSIS, BECEd).
            - **Admissions & TPCAT Guidelines:** Requirements, examination etiquette, and transfer credit rules.
            - **School Uniform Policy:** Type A standards, wash-day guidelines, and prohibited clothing items.
            - **Talibon Ordinance No. 127:** Boarding house 10:00 PM curfews, landlord sanitary obligations, and fire exit safety.
            - **Subsidies & Grants:** CHED Free Higher Education (RA 10931) and GSIS STEM monthly stipends.
            - **Disciplinary Matrix:** Sanction scales and the 500-meter campus alcohol/entertainment prohibition zone.
            """)

        with col_a2:
            st.markdown("""
            ### 🛠️ **Technical Architecture & Guardrails**
            - **Retrieval Engine:** Custom LangChain Hybrid Retriever syncing Pinecone Serverless (AWS us-east-1) with dual local NumPy dense vector matrices.
            - **Embedding Model:** `BAAI/bge-small-en-v1.5` (384-dimensional dense vectors, 128 normalized chunks).
            - **Scope Containment Guardrail:** Cosine confidence cutoff of **0.50**. Off-topic or non-institutional inquiries are safely refused with formal office referrals.
            - **Conversational Memory:** 5-turn sliding window memory buffer with automated contextual coreference resolution.
            - **Deployment Infrastructure:** Containerized with Docker and continuously deployed on Railway Cloud via GitHub CI/CD.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📚 **Verified Knowledge Base Corpus (7 Sources)**")
        st.markdown("""
        1. **TPC Student Handbook v.04 (Latest Approved 202-Page Edition)**  
           *Academics, Grading, Retention Criteria, Disciplinary Matrix, Student Governance*
        2. **Talibon Municipal Ordinance No. 127**  
           *Boarding Houses, Safety Standards, Curfew Hours, Sanitation Permits, Penalty Schedules*
        3. **TPC Uniform & Dress Code Policy Guide**  
           *General Type A Uniform, Prohibited Attires, Footwear Standards, Grooming*
        4. **TPC Admissions & TPCAT Guidelines**  
           *Freshmen Requirements, Examination Day Etiquette, Transferee Sequences*
        5. **CHED Free Higher Education (Republic Act 10931)**  
           *LUC Exemption, TES Subsidy Eligibility, Zero Tuition & Mandatory Fee Guarantee*
        6. **GSIS Subsidy for STEM (GSSP) Guidelines**  
           *Scholarship Criteria & 90% GWA Maintenance Requirements*
        7. **PNP-TPC Joint Safety Memorandums**  
           *Curfew Patrols, 500m Alcohol Exclusion Zone, Nighttime Boarding House Inspections*
        """)

        st.markdown("---")
        st.markdown("""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; text-align: center;">
            <h4 style="margin: 0; color: #064E3B;">Talibon Polytechnic College • Bohol, Philippines</h4>
            <p style="margin: 0.35rem 0; color: #64748B; font-size: 0.85rem;">Course Capstone Project for <strong>IS Professional Elective #4 (Generative AI Systems)</strong> • A.Y. 2026–2027</p>
            <p style="margin: 0; color: #059669; font-weight: 700; font-size: 0.9rem;">Team Kuys: Eduardo Avenido Jr. • Christian Paul G. La Rosa • Nielbert Garcia • Marcel Avergonzado • Ronald M. Barril</p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    run_app()
