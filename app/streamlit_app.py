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
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

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

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
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
try:
    engine = get_rag_engine()
    system_status = engine.get_system_status()
except Exception as init_err:
    st.error(f"⚠️ Engine Initialization Warning: {init_err}")
    engine = None
    system_status = {
        "status": "Offline Fallback",
        "vector_backend": "Local NumPy Matrix",
        "llm_engine": "Local Policy Extractor",
        "indexed_chunks": 128,
        "embedding_model": "BAAI/bge-small-en-v1.5"
    }

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
            "chunks": []
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
    if "Cloud" in system_status.get("status", ""):
        st.success(f"🟢 **Status:** {system_status['status']}")
    else:
        st.info(f"🔄 **Status:** {system_status['status']}")

    st.write(f"🌲 **Vector Store:** {system_status.get('vector_backend', 'Local Cache')}")
    st.write(f"🤖 **LLM Engine:** {system_status.get('llm_engine', 'Local Extractor')}")
    st.write(f"📚 **Indexed Chunks:** `{system_status.get('indexed_chunks', 128)} chunks`")
    st.write(f"🎯 **Embedding Model:** `{system_status.get('embedding_model', 'bge-small-en-v1.5')}`")
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
        if engine:
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
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display Sources and Confidence cleanly with native Streamlit caption
        if msg.get("sources"):
            sources_str = ", ".join(msg["sources"])
            conf = msg.get("confidence", 0.0) * 100
            st.caption(f"📚 **Official Source:** {sources_str} &nbsp;|&nbsp; 🎯 **Match Confidence:** {conf:.1f}%")
        
        # Display Expandable Chunks
        chunks = msg.get("chunks", [])
        if chunks:
            with st.expander(f"🔍 View Policy Passages & Retrieved Excerpts ({len(chunks)})"):
                for idx, chunk in enumerate(chunks, 1):
                    score_pct = chunk.get("score", 0.0) * 100
                    st.markdown(f"**[{idx}] {chunk.get('source', 'TPC Policy')}** *(Match: {score_pct:.1f}%)*")
                    st.caption(chunk.get("text", ""))

# User Input Handling
user_input = st.chat_input("Ask a question about TPC policies, admissions, uniforms, or curfew...")

# Trigger query from either chat input or sidebar quick-ask buttons
active_query = user_input or selected_query

if active_query:
    # 1. Add and render user question immediately
    st.session_state.messages.append({"role": "user", "content": active_query})
    with st.chat_message("user"):
        st.markdown(active_query)

    # 2. Render assistant bubble immediately with in-place generation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("🔍 Navigating TPC institutional records..."):
            if engine:
                try:
                    response = engine.query(active_query)
                    answer_text = response.get("answer", "No answer found in policy records.")
                    sources = response.get("sources", [])
                    confidence = response.get("confidence", 0.0)
                    chunks = response.get("chunks", [])
                    engine_used = response.get("engine_used", "LangChain RAG")
                except Exception as query_err:
                    answer_text = f"⚠️ An error occurred while retrieving policy records: {query_err}\n\nPlease try again."
                    sources = []
                    confidence = 0.0
                    chunks = []
                    engine_used = "Error Fallback"
            else:
                answer_text = "⚠️ RAG Engine is not currently initialized."
                sources = []
                confidence = 0.0
                chunks = []
                engine_used = "System"

        # Display answer in-place
        message_placeholder.markdown(answer_text)
        if sources:
            sources_str = ", ".join(sources)
            conf = confidence * 100
            st.caption(f"📚 **Official Source:** {sources_str} &nbsp;|&nbsp; 🎯 **Match Confidence:** {conf:.1f}%")
        if chunks:
            with st.expander(f"🔍 View Policy Passages & Retrieved Excerpts ({len(chunks)})"):
                for idx, chunk in enumerate(chunks, 1):
                    score_pct = chunk.get("score", 0.0) * 100
                    st.markdown(f"**[{idx}] {chunk.get('source', 'TPC Policy')}** *(Match: {score_pct:.1f}%)*")
                    st.caption(chunk.get("text", ""))

    # 3. Append assistant response to history
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
