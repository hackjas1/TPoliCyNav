"""
=============================================================================
TPoliCynav: The TPC Policy Navigator
Talibon Polytechnic College — Institutional Policy Conversational Agent
Checkpoint 4: Deliverable 16 (Professional Web Application Interface)
=============================================================================
Built with Streamlit, LangChain, Pinecone Serverless, and Hugging Face.
Official Institutional Theme: Green, Light Green, Dark Green, and White.
=============================================================================
"""

import os
import sys
import time
import streamlit as st

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from app.rag_engine import TPCRagEngine

# Page configuration
st.set_page_config(
    page_title="TPoliCynav — TPC Policy Navigator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling with TPC Official Colors: Green, Light Green, Dark Green, White
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Background and main container */
    .stApp {
        background-color: #F0FDF4;
    }

    /* Main Header Container */
    .tpc-header {
        background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #10B981 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        margin-bottom: 1.5rem;
        border-left: 8px solid #34D399;
    }
    .tpc-header h1 {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.02em;
    }
    .tpc-header p {
        font-size: 1.05rem;
        margin: 0.35rem 0 0 0;
        color: #D1FAE5;
        font-weight: 500;
    }

    /* Badge Pills */
    .pill-badge {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-top: 0.5rem;
    }
    .pill-green {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .pill-darkgreen {
        background-color: #064E3B;
        color: #FFFFFF;
    }
    .pill-amber {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
    }

    /* Quick Prompt Buttons */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #065F46;
        border: 1.5px solid #10B981;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 0.5rem 0.85rem;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
    }
    div.stButton > button:hover {
        background-color: #065F46;
        color: #FFFFFF;
        border-color: #065F46;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(6, 95, 70, 0.2);
    }

    /* Citations expander */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #065F46 !important;
    }

    /* Footer text */
    .tpc-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        color: #047857;
        font-size: 0.82rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="🏛️ Initializing TPoliCynav RAG Engine...")
def get_rag_engine():
    """Cache the RAG engine instance so it initializes only once."""
    return TPCRagEngine(mode="auto")


# Initialize RAG Engine
engine = get_rag_engine()
system_status = engine.get_system_status()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Good day, TPCian!** I am **TPoliCynav**, the official AI Policy Navigator for "
                "**Talibon Polytechnic College (TPC)** in Bohol.\n\n"
                "I can answer your inquiries regarding:\n"
                "• 🎓 **Degree programs and admissions requirements**\n"
                "• 👔 **School uniforms and entrance exam dress codes**\n"
                "• 🏠 **Boarding house curfews and municipal safety (Ordinance 127)**\n"
                "• 💰 **CHED Free Higher Education (RA 10931) and GSIS STEM subsidies**\n"
                "• ⚖️ **Student conduct, retention policies, and disciplinary matrices**\n\n"
                "How may I assist you with college policies today?"
            ),
            "sources": [],
            "confidence": 1.0,
            "engine": "System Greeting"
        }
    ]

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Seal_of_Bohol.svg/200px-Seal_of_Bohol.svg.png",
        width=85
    )
    st.markdown("### 🏛️ **TPoliCynav**")
    st.caption("Talibon Polytechnic College Policy Navigator")
    st.markdown("---")

    # System Status Indicator
    st.markdown("#### ⚙️ **System Diagnostics**")
    if "Cloud" in system_status["status"]:
        st.success(f"🟢 **Status:** {system_status['status']}")
    else:
        st.info(f"🔄 **Status:** {system_status['status']}")

    st.write(f"🌲 **Vector Store:** {system_status['vector_backend']}")
    st.write(f"🤖 **LLM Engine:** {system_status['llm_engine']}")
    st.write(f"📚 **Indexed Chunks:** `{system_status['indexed_chunks']} chunks`")
    st.write(f"🎯 **Embedding Model:** `{system_status['embedding_model']}`")
    st.markdown("---")

    # Quick Inquiry Topic Chips
    st.markdown("#### 💡 **Frequent Student Inquiries**")
    st.caption("Click any topic below to test instant grounded retrieval:")

    sample_queries = [
        ("🎓 Official Degree Programs", "What courses and undergraduate degree programs are officially offered at TPC?"),
        ("👔 Entrance Exam Dress Code", "Are ripped jeans, shorts, or slippers allowed during the TPC entrance exam?"),
        ("🏠 Boarding House Curfew", "What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?"),
        ("💰 GSIS STEM Scholarship", "What is the minimum GWA required to qualify for the GSIS STEM subsidy?"),
        ("🚫 Alcohol Prohibition Zone", "What is the 500-meter alcohol and entertainment prohibition zone around TPC?"),
        ("🔴 Out-of-Scope Test (Refusal)", "What is the capital city and total population of Tokyo, Japan?")
    ]

    selected_query = None
    for label, query_text in sample_queries:
        if st.button(label, key=f"btn_{label}"):
            selected_query = query_text

    st.markdown("---")

    # Official Knowledge Base Explorer
    with st.expander("📂 **Official Policy Knowledge Base (7 Sources)**"):
        st.markdown("""
        1. **TPC Student Handbook v.04 (Latest Approved 202-Page Edition)**  
           *Academics, Grading, Retention, Disciplinary Matrix*
        2. **Talibon Municipal Ordinance No. 127**  
           *Boarding Houses, Safety Standards, Curfew Hours*
        3. **TPC Uniform & Dress Code Policy Guide**  
           *General Type A Uniform, Prohibited Attires, Shoes*
        4. **TPC Admissions & TPCAT Guidelines**  
           *Freshmen Requirements, Examination Day Etiquette*
        5. **CHED Free Higher Education (Republic Act 10931)**  
           *LUC Exemption, TES Subsidy Eligibility*
        6. **GSIS Subsidy for STEM (GSSP) Guidelines**  
           *Scholarship Criteria & 90% GWA Maintenance*
        7. **PNP-TPC Joint Safety Memorandums**  
           *Curfew Patrols & Boarding House Inspections*
        """)

    # Free-Tier Quota Note (Required by Final Presentation Guide)
    st.markdown("---")
    st.markdown("#### ℹ️ **Usage & Deployment Note**")
    st.caption(
        "Deployed on **Railway Cloud** via GitHub CI/CD. Utilizes free-tier Pinecone Serverless and "
        "Hugging Face Inference API with automatic offline vector fallback. In case of API rate limits, "
        "the local precision extractor seamlessly resolves policy inquiries."
    )

    # Session Reset
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = [st.session_state.messages[0]]
        engine.reset_memory()
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN CONTENT AREA
# -----------------------------------------------------------------------------
st.markdown("""
<div class="tpc-header">
    <h1>🏛️ TPoliCynav: The TPC Policy Navigator</h1>
    <p>Official AI-Driven RAG Assistant for Talibon Polytechnic College Institutional Policies</p>
    <div style="margin-top: 0.6rem;">
        <span class="pill-badge pill-darkgreen">🌲 Pinecone Serverless</span>
        <span class="pill-badge pill-green">🤖 LangChain Orchestrated</span>
        <span class="pill-badge pill-green">🧠 BGE-Small Embeddings</span>
        <span class="pill-badge pill-green">🛡️ Strict Anti-Hallucination</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display Sources and Confidence if present
        if msg.get("sources"):
            sources_str = ", ".join(msg["sources"])
            st.markdown(
                f"<div style='margin-top: 0.5rem; font-size: 0.85rem; color: #047857; font-weight: 600;'>"
                f"📚 <b>Official Source:</b> {sources_str} &nbsp;|&nbsp; "
                f"🎯 <b>Match Confidence:</b> {msg.get('confidence', 0.0) * 100:.1f}%</div>",
                unsafe_allow_html=True
            )
        
        # Display Expandable Chunks
        if msg.get("chunks"):
            with st.expander("🔍 View Official Policy Passages & Retrieved Chunks"):
                for idx, chunk in enumerate(msg["chunks"], 1):
                    st.markdown(f"**[{idx}] {chunk.get('source', 'TPC Policy')}** *(Match: {chunk.get('score', 0.0) * 100:.1f}%)*")
                    st.info(chunk.get("text", ""))

# User Input Handling
user_input = st.chat_input("Ask a question about TPC policies, admissions, uniforms, or curfew...")

# Trigger query from either chat input or sidebar quick-ask buttons
active_query = user_input or selected_query

if active_query:
    # Append user question to history
    st.session_state.messages.append({"role": "user", "content": active_query})
    with st.chat_message("user"):
        st.markdown(active_query)

    # Process Query with RAG Engine
    with st.chat_message("assistant"):
        with st.spinner("🔍 Navigating TPC institutional records..."):
            response = engine.query(active_query)

        answer_text = response.get("answer", "")
        sources = response.get("sources", [])
        confidence = response.get("confidence", 0.0)
        chunks = response.get("chunks", [])
        engine_used = response.get("engine_used", "LangChain RAG")
        is_refusal = response.get("is_refusal", False)

        st.markdown(answer_text)

        if sources:
            sources_str = ", ".join(sources)
            st.markdown(
                f"<div style='margin-top: 0.5rem; font-size: 0.85rem; color: #047857; font-weight: 600;'>"
                f"📚 <b>Official Source:</b> {sources_str} &nbsp;|&nbsp; "
                f"🎯 <b>Match Confidence:</b> {confidence * 100:.1f}%</div>",
                unsafe_allow_html=True
            )

        if chunks:
            with st.expander("🔍 View Official Policy Passages & Retrieved Chunks"):
                for idx, chunk in enumerate(chunks, 1):
                    st.markdown(f"**[{idx}] {chunk.get('source', 'TPC Policy')}** *(Match: {chunk.get('score', 0.0) * 100:.1f}%)*")
                    st.info(chunk.get("text", ""))

    # Save Assistant Response to Session
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer_text,
        "sources": sources,
        "confidence": confidence,
        "chunks": chunks,
        "engine": engine_used
    })

# Footer
st.markdown("""
<div class="tpc-footer">
    Talibon Polytechnic College (TPC) • IS Professional Elective #4 Generative AI Capstone Project • A.Y. 2026–2027<br>
    Team Kuys: Eduardo Avenido Jr. • Christian Paul Larosa • Nielbert Garcia • Marcel Avergonzado
</div>
""", unsafe_allow_html=True)

