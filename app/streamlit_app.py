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


@st.cache_resource(show_spinner="🏛️ Initializing TPoliCynav RAG Engine & Vector Cache...")
def get_rag_engine():
    """Cache the RAG engine instance so it initializes only once across user sessions."""
    return TPCRagEngine(mode="auto")


# =============================================================================
# HIGH-FIDELITY INSTITUTIONAL CSS THEME (TPC PALETTE)
# =============================================================================
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }

    /* Overall page background */
    .stApp {
        background-color: #F4FBF7;
    }

    /* Header Banner Container */
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

    /* Starter Launchpad Cards */
    .starter-header {
        font-size: 0.95rem;
        font-weight: 700;
        color: #064E3B;
        margin: 1.25rem 0 0.75rem 0;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Custom Button Styling */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #065F46;
        border: 1.5px solid #10B981;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.84rem;
        padding: 0.55rem 0.9rem;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        text-align: left;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    div.stButton > button:hover {
        background-color: #065F46;
        color: #FFFFFF;
        border-color: #065F46;
        transform: translateY(-2px);
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
        gap: 0.6rem;
        font-size: 0.8rem;
    }
    .verif-badge {
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        font-size: 0.76rem;
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

    /* Footer text */
    .tpc-footer {
        text-align: center;
        padding: 2.5rem 0 1.25rem 0;
        color: #64748B;
        font-size: 0.82rem;
        line-height: 1.5;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
    }
    .tpc-footer strong {
        color: #065F46;
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
                Eduardo Avenido Jr. • Christian Paul Larosa<br>
                Nielbert Garcia • Marcel Avergonzado
            </div>
            <div style="font-size: 0.68rem; color: #94A3B8; margin-top: 0.45rem; border-top: 1px dashed #CBD5E1; padding-top: 0.35rem;">
                Official AI Policy Conversational Agent
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # MAIN CONTENT AREA: HEADER & CHAT CANVAS
    # -------------------------------------------------------------------------
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
            <span class="pill pill-light">🛡️ Cosine Scope Guardrail (0.50)</span>
            <span class="pill pill-light">⚡ Latency-Optimized</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Empty State Starter Launchpad (Displayed only when dialogue is at initial state)
    if len(st.session_state.messages) == 1:
        st.markdown("""
        <div class="starter-header">
            <span>🚀 Quick Launchpad — Popular Student Inquiries:</span>
        </div>
        """, unsafe_allow_html=True)

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
        
        st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # RENDER COMPLETE CHAT HISTORY
    # -------------------------------------------------------------------------
    for msg_idx, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        avatar_icon = "🎓" if is_user else (TPC_LOGO_PATH if (TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH)) else "🏛️")

        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])

            # Render Verification Strip for Assistant Responses
            if not is_user:
                sources = msg.get("sources", [])
                confidence = msg.get("confidence", 0.0)
                latency_ms = msg.get("latency_ms", 0)
                engine_name = msg.get("engine", "RAG Pipeline")

                # Color-code confidence badge
                if confidence >= 0.80:
                    conf_class = "verif-emerald"
                    conf_label = f"🟢 High Match ({confidence*100:.1f}%)"
                elif confidence >= 0.60:
                    conf_class = "verif-light"
                    conf_label = f"🟢 Grounded Match ({confidence*100:.1f}%)"
                elif confidence >= 0.50:
                    conf_class = "verif-amber"
                    conf_label = f"🟡 Moderate Match ({confidence*100:.1f}%)"
                else:
                    conf_class = "verif-amber"
                    conf_label = "⚪ Out-of-Scope Refusal"

                # Verification and citation badges
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
                            chunk_id = chunk.get("chunk_id", f"chunk_{idx}")
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

                # Feedback & Micro-Interactions (Available for non-initial messages)
                if msg_idx > 0:
                    fb_col1, fb_col2, fb_col3 = st.columns([1, 1, 8])
                    fb_key = f"fb_{msg_idx}"
                    current_fb = st.session_state.feedback_log.get(fb_key)

                    with fb_col1:
                        if st.button("👍 Helpful", key=f"btn_up_{msg_idx}"):
                            st.session_state.feedback_log[fb_key] = "up"
                            st.toast("Thank you! Feedback recorded for TPC knowledge base optimization.", icon="✅")
                    with fb_col2:
                        if st.button("👎 Clarify", key=f"btn_down_{msg_idx}"):
                            st.session_state.feedback_log[fb_key] = "down"
                            st.toast("Noted. We will continue refining TPC policy grounding.", icon="📝")

                    # Suggested Follow-Up Prompt Chips
                    follow_ups = msg.get("follow_ups", [])
                    if not follow_ups and msg_idx > 0:
                        prev_user_query = st.session_state.messages[msg_idx - 1]["content"] if msg_idx - 1 >= 0 else ""
                        follow_ups = get_suggested_follow_ups(prev_user_query, msg["content"])

                    if follow_ups and msg_idx == len(st.session_state.messages) - 1:
                        st.markdown("""
                        <div class="followup-label">
                            <span>💡 Recommended Follow-Up Inquiries:</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        f_cols = st.columns(len(follow_ups))
                        for f_idx, (f_label, f_query) in enumerate(follow_ups):
                            with f_cols[f_idx]:
                                if st.button(f_label, key=f"fup_{msg_idx}_{f_idx}"):
                                    st.session_state.pending_prompt = f_query
                                    st.rerun()

    # -------------------------------------------------------------------------
    # FIXED BOTTOM CANVAS: INPUT FIELD & DOCKED FOOTER
    # -------------------------------------------------------------------------
    with st.bottom:
        user_typed = st.chat_input("Ask any question regarding TPC admissions, degree programs, uniform rules, curfew...")
        st.markdown("""
        <div style="text-align: center; font-size: 0.74rem; color: #64748B; padding: 0.25rem 0 0.45rem 0; line-height: 1.45;">
            <strong>Talibon Polytechnic College (TPC)</strong> • Bohol, Philippines &nbsp;|&nbsp; 
            <em>IS Professional Elective #4 Capstone Project</em> &nbsp;|&nbsp; 
            <strong style="color: #059669;">Team Kuys</strong><br>
            <span style="font-size: 0.70rem; color: #94A3B8;">
                Disclaimer: Synthesized from official TPC documents (Handbook v.04, Ord. 127, RA 10931). For official certifications, consult the Registrar.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Determine Active Prompt: from quick launch buttons, follow-ups, or chat input
    active_prompt = None
    if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
        active_prompt = st.session_state.pop("pending_prompt")
    elif user_typed:
        active_prompt = user_typed

    # Process Active Query
    if active_prompt:
        # 1. Append and render user message
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user", avatar="🎓"):
            st.markdown(active_prompt)

        # 2. Render assistant response bubble with animated institutional spinner
        assistant_avatar = TPC_LOGO_PATH if (TPC_LOGO_PATH and os.path.exists(TPC_LOGO_PATH)) else "🏛️"
        with st.chat_message("assistant", avatar=assistant_avatar):
            with st.spinner("🔍 Navigating TPC institutional records & vector embeddings..."):
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
                    except Exception as query_err:
                        answer_text = f"⚠️ An error occurred while retrieving policy records: {query_err}\n\nPlease try again."
                        sources = []
                        confidence = 0.0
                        chunks = []
                        engine_used = "Error Fallback"
                        latency_ms = int((time.time() - start_query_t) * 1000)
                else:
                    answer_text = "⚠️ RAG Engine is not currently initialized."
                    sources = []
                    confidence = 0.0
                    chunks = []
                    engine_used = "System"
                    latency_ms = 0

            # Display generated answer
            st.markdown(answer_text)

            # Generate dynamic follow-ups
            follow_ups = get_suggested_follow_ups(active_prompt, answer_text)

        # 3. Append assistant response to session state & rerun to sync clean history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer_text,
            "sources": sources,
            "confidence": confidence,
            "chunks": chunks,
            "engine": engine_used,
            "latency_ms": latency_ms,
            "follow_ups": follow_ups
        })
        st.rerun()


if __name__ == "__main__":
    run_app()
