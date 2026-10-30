import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets padding for a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tcMar)

def add_callout_box(doc, action_text, fill_hex="F1F5F9", border_color="0284C7"):
    """Creates a visual action callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Left border styling
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(f"🎥 SCREEN ACTION: {action_text}")
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    
    # Empty space after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def build_script_document():
    doc = Document()
    
    # Set standard margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    
    # Colors
    c_primary = RGBColor(6, 78, 59)      # Deep Forest Green (#064E3B)
    c_accent = RGBColor(5, 150, 105)     # Emerald (#059669)
    c_dark = RGBColor(15, 23, 42)        # Slate Dark (#0F172A)
    c_muted = RGBColor(100, 116, 139)    # Muted Slate (#64748B)

    # =========================================================================
    # DOCUMENT HEADER / TITLE
    # =========================================================================
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("TALIBON POLYTECHNIC COLLEGE (TPC) • BOHOL, PHILIPPINES")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = c_accent
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("TPoliCynav: Final Presentation & Video Demo Script")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = c_primary
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Official 5-to-8 Minute Video Recording Guide with Assigned Speaker Roles (final_presentation_guide.pdf)")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = c_muted

    # =========================================================================
    # PROJECT & SUBMISSION OVERVIEW TABLE
    # =========================================================================
    tbl_info = doc.add_table(rows=7, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    
    info_data = [
        ("Course & Project", "IS Professional Elective #4 (Generative AI Systems) — Capstone RAG Application"),
        ("Project Title", "TPoliCynav: The TPC Policy Navigator (AI Conversational Agent)"),
        ("Capstone Group (Team Kuys)", "Eduardo Avenido Jr. • Christian Paul G. La Rosa • Nielbert Garcia • Marcel Avergonzado • Ronald M. Barril"),
        ("System Creator & Architect", "Christian Paul G. La Rosa (Lead AI & System Developer — Creator of TPoliCynav)"),
        ("Assigned Video Presenters", "1. Eduardo Avenido Jr.  |  2. Nielbert Garcia  |  3. Marcel Avergonzado  |  4. Ronald M. Barril"),
        ("Live Deployed App URL", "https://tpolicynav-production.up.railway.app (Public, Zero-Login Required)"),
        ("Public GitHub Repository", "https://github.com/hackjas1/TPoliCyNav.git (Includes README & .env.example)")
    ]
    
    for row_idx, (k, v) in enumerate(info_data):
        row = tbl_info.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width = Inches(2.2)
        cell_v.width = Inches(4.3)
        
        bg_col = "F8FAFC" if row_idx % 2 == 0 else "FFFFFF"
        set_cell_background(cell_k, bg_col)
        set_cell_background(cell_v, bg_col)
        set_cell_margins(cell_k, top=70, bottom=70, left=100, right=100)
        set_cell_margins(cell_v, top=70, bottom=70, left=100, right=100)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.space_after = Pt(0)
        rk = pk.add_run(k)
        rk.font.name = "Calibri"
        rk.font.size = Pt(9.5)
        rk.font.bold = True
        rk.font.color.rgb = c_primary
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.space_after = Pt(0)
        rv = pv.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = c_dark

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(12)
    p_div.paragraph_format.space_after = Pt(12)

    # =========================================================================
    # TIMING & SPEAKER ASSIGNMENT BREAKDOWN
    # =========================================================================
    h_overview = doc.add_heading(level=1)
    r_h_over = h_overview.add_run("📋 Video Section Breakdown & Presenter Rotation")
    r_h_over.font.name = "Calibri"
    r_h_over.font.color.rgb = c_primary
    
    p_over_desc = doc.add_paragraph()
    p_over_desc.paragraph_format.space_after = Pt(8)
    r_od = p_over_desc.add_run(
        "According to the official grading rubric, the demo video must cover 5 parts in exact sequential order. "
        "The speaking roles are distributed across our 4 presenters (Christian Paul G. La Rosa is credited as the system creator):"
    )
    r_od.font.name = "Calibri"
    r_od.font.size = Pt(10.5)

    tbl_timing = doc.add_table(rows=6, cols=4)
    tbl_timing.alignment = WD_TABLE_ALIGNMENT.CENTER
    timing_data = [
        ("Part & Order", "Assigned Presenter", "Required Topic / Content", "Estimated Duration"),
        ("Part 1: Problem & Data", "Eduardo Avenido Jr.", "Team intro, problem statement, 7 official TPC policy sources", "0:00 – 1:30 (1m 30s)"),
        ("Part 2: Architecture", "Nielbert Garcia", "BGE-Small embedding, Pinecone vector store, 0.50 guardrail, LangChain", "1:30 – 2:45 (1m 15s)"),
        ("Part 3: Live Walkthrough", "Marcel Avergonzado", "Public Railway link, zero login, UI layout, mobile responsiveness", "2:45 – 3:45 (1m 00s)"),
        ("Part 4: Live Test Inquiries", "Marcel Avergonzado", "3 questions: Programs offered, Curfew rules, Out-of-scope refusal", "3:45 – 5:15 (1m 30s)"),
        ("Part 5: Improvements & Close", "Ronald M. Barril", "Multilingual (Bisaya), SIS integration, voice input, conclusion", "5:15 – 6:30 (1m 15s)")
    ]

    for r_idx, row_vals in enumerate(timing_data):
        row = tbl_timing.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, val in enumerate(row_vals):
            c = row.cells[c_idx]
            if c_idx == 0:
                c.width = Inches(1.5)
            elif c_idx == 1:
                c.width = Inches(1.6)
            elif c_idx == 2:
                c.width = Inches(2.3)
            else:
                c.width = Inches(1.1)
                
            bg_col = "E2E8F0" if is_hdr else ("F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            set_cell_background(c, bg_col)
            set_cell_margins(c, top=80, bottom=80, left=80, right=80)
            
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9 if not is_hdr else 9.5)
            run.font.bold = is_hdr
            if is_hdr:
                run.font.color.rgb = c_primary

    doc.add_page_break()

    # =========================================================================
    # PART 1: THE PROBLEM & KNOWLEDGE SOURCE (EDUARDO AVENIDO JR.)
    # =========================================================================
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("Part 1: The Problem & Knowledge Sources Used (0:00 – 1:30)")
    r1.font.name = "Calibri"
    r1.font.color.rgb = c_primary

    p_spk1 = doc.add_paragraph()
    p_spk1.paragraph_format.space_after = Pt(4)
    r_s1 = p_spk1.add_run("🎙️ ASSIGNED PRESENTER: EDUARDO AVENIDO JR.")
    r_s1.font.name = "Calibri"
    r_s1.font.bold = True
    r_s1.font.color.rgb = c_primary

    add_callout_box(
        doc,
        "Record screen showing the opening title slide with Team Kuys member names, or camera with Eduardo Avenido Jr. on screen. "
        "Transition to displaying the official documents folder (TPC Student Handbook v.04, Talibon Ordinance 127, etc.)."
    )

    p1_spk = doc.add_paragraph()
    p1_spk.paragraph_format.space_after = Pt(6)
    p1_spk.paragraph_format.line_spacing = 1.2
    
    r_spk_tag = p1_spk.add_run("SPEAKING SCRIPT:\n")
    r_spk_tag.bold = True
    r_spk_tag.font.color.rgb = c_accent
    
    p1_text = (
        '"Good day, instructor and classmates! Welcome to our Generative AI capstone presentation. '
        'We are Team Kuys from Talibon Polytechnic College in Bohol, composed of myself, Eduardo Avenido Jr., '
        'Christian Paul G. La Rosa — who is our lead AI developer and the creator of this entire project — along with '
        'Nielbert Garcia, Marcel Avergonzado, and Ronald M. Barril.\n\n'
        'Today, we are presenting TPoliCynav: The TPC Policy Navigator.\n\n'
        'Let’s begin with the problem we set out to solve:\n\n'
        'At Talibon Polytechnic College, thousands of students regularly have critical questions regarding institutional guidelines — '
        'from freshman admission criteria and retention GWA, to examination dress codes, municipal boarding house curfews, and '
        'CHED scholarship subsidies. However, these rules are scattered across thick 200-page printed PDF handbooks and municipal ordinances. '
        'Students often rely on word-of-mouth rumors, or face long queues at the Registrar and Student Affairs offices.\n\n'
        'To solve this, our group developed TPoliCynav: a specialized, retrieval-augmented conversational agent that delivers authoritative, '
        'instant, and verified answers grounded exclusively in official institutional records.\n\n'
        'Our knowledge base is built from 7 verified college sources:\n'
        '1. The latest 202-page approved TPC Student Handbook Version 04;\n'
        '2. Talibon Municipal Ordinance Number 127 regarding boarding house safety standards and 10:00 PM curfews;\n'
        '3. The official TPC Uniform and Grooming Standards Guide;\n'
        '4. TPC Admissions and TPCAT Examination Guidelines;\n'
        '5. Republic Act 10931 on CHED Free Higher Education;\n'
        '6. GSIS STEM Scholarship Subsidy maintainability rules; and\n'
        '7. Joint PNP-TPC Campus Safety and Curfew Inspection Memorandums.\n\n'
        'Now, I will pass the floor over to Nielbert Garcia to explain the technical architecture and RAG pipeline powering TPoliCynav."'
    )
    p1_spk.add_run(p1_text).font.size = Pt(11)

    # =========================================================================
    # PART 2: THE ARCHITECTURE (NIELBERT GARCIA)
    # =========================================================================
    h2 = doc.add_heading(level=1)
    r2 = h2.add_run("Part 2: Technical Architecture & RAG Pipeline (1:30 – 2:45)")
    r2.font.name = "Calibri"
    r2.font.color.rgb = c_primary

    p_spk2 = doc.add_paragraph()
    p_spk2.paragraph_format.space_after = Pt(4)
    r_s2 = p_spk2.add_run("🎙️ ASSIGNED PRESENTER: NIELBERT GARCIA")
    r_s2.font.name = "Calibri"
    r_s2.font.bold = True
    r_s2.font.color.rgb = c_primary

    add_callout_box(
        doc,
        "Display the 'About the Chatbot & Architecture' tab on the live website, or a clean architecture diagram slide "
        "showing the flow: PDF Documents -> Chunking -> BGE-Small -> Pinecone Vector Store -> 0.50 Cosine Guardrail -> LLM -> Streamlit UI."
    )

    p2_spk = doc.add_paragraph()
    p2_spk.paragraph_format.space_after = Pt(6)
    p2_spk.paragraph_format.line_spacing = 1.2
    
    r_spk_tag = p2_spk.add_run("SPEAKING SCRIPT:\n")
    r_spk_tag.bold = True
    r_spk_tag.font.color.rgb = c_accent
    
    p2_text = (
        '"Thank you, Eduardo! Good day everyone, I am Nielbert Garcia, and I will walk you through the technical architecture '
        'powering TPoliCynav.\n\n'
        'We designed a production-grade, zero-hallucination RAG pipeline following these five technical pillars:\n\n'
        '1. Text Ingestion & Chunking: We ingested our 7 institutional sources, parsed them, and split them into 128 normalized chunks. '
        'Each chunk contains rich metadata identifying the exact document name, page number, and policy section.\n\n'
        '2. Dense Embedding Model: For vector representation, we selected BAAI/bge-small-en-v1.5 from Hugging Face. '
        'It generates highly accurate 384-dimensional dense vectors with exceptional semantic precision for legal and institutional terminology.\n\n'
        '3. Vector Database & Storage: We implemented a hybrid architecture. In the cloud, we use Pinecone Serverless deployed in AWS us-east-1 '
        'for lightning-fast sub-50-millisecond cosine vector searches. As a resilience backup, our system includes an automatic local NumPy dense matrix '
        'fallback so the chatbot never goes down even during cloud network blips.\n\n'
        '4. Scope Containment Guardrail (Strict 0.50 Cosine Threshold): This is our most critical guardrail against hallucinations. '
        'Before any LLM generates an answer, we evaluate the cosine similarity of the retrieved passages. If the highest score is below 0.50, '
        'the system safely refuses to answer and redirects the student to the Registrar or OSAS, guaranteeing zero false policy advice.\n\n'
        '5. Orchestration & Conversational Memory: We used LangChain with a 5-turn sliding window memory buffer. '
        'This allows students to ask natural follow-up questions — like saying \"What about shoes?\" after asking about uniforms — and the model '
        'resolves the context accurately.\n\n'
        '6. Deployment & Hosting: The application is containerized with Docker and continuously deployed on Railway Cloud via GitHub CI/CD, '
        'running 24/7 on a public link without requiring any login.\n\n'
        'Now, I will turn the presentation over to Marcel Avergonzado for a live walkthrough of our deployed app and sample test questions."'
    )
    p2_spk.add_run(p2_text).font.size = Pt(11)

    # =========================================================================
    # PART 3: LIVE WALKTHROUGH (MARCEL AVERGONZADO)
    # =========================================================================
    h3 = doc.add_heading(level=1)
    r3 = h3.add_run("Part 3: Live Walkthrough of the Public Deployed App (2:45 – 3:45)")
    r3.font.name = "Calibri"
    r3.font.color.rgb = c_primary

    p_spk3 = doc.add_paragraph()
    p_spk3.paragraph_format.space_after = Pt(4)
    r_s3 = p_spk3.add_run("🎙️ ASSIGNED PRESENTER: MARCEL AVERGONZADO")
    r_s3.font.name = "Calibri"
    r_s3.font.bold = True
    r_s3.font.color.rgb = c_primary

    add_callout_box(
        doc,
        "Open a fresh incognito browser tab and navigate to: https://tpolicynav-production.up.railway.app. "
        "Highlight that it loads instantly without any login screen or software installation. "
        "Show the TPC Seal, the header banner, the tabs, the sidebar diagnostics, and the pinned bottom chatbox."
    )

    p3_spk = doc.add_paragraph()
    p3_spk.paragraph_format.space_after = Pt(6)
    p3_spk.paragraph_format.line_spacing = 1.2
    
    r_spk_tag = p3_spk.add_run("SPEAKING SCRIPT:\n")
    r_spk_tag.bold = True
    r_spk_tag.font.color.rgb = c_accent
    
    p3_text = (
        '"Thank you, Nielbert! Hello everyone, I am Marcel Avergonzado, and I will be demonstrating the live, publicly deployed application.\n\n'
        'As you can see on my screen, our app is hosted live on Railway at tpolicynav-production.up.railway.app. '
        'Meeting the project rubric 100%, anyone can open this link on their laptop, tablet, or smartphone without installing anything or creating an account.\n\n'
        'Let’s take a quick tour of the user interface:\n'
        '• At the top, we have our official TPC masthead displaying the official Talibon Polytechnic College seal and portal title.\n'
        '• On the left sidebar, we have real-time System Diagnostics showing the Pinecone vector connection, active corpus chunk count, '
        'and categorized quick-launch topics for students.\n'
        '• We also included a QOL feature in the sidebar: an \"Export Policy Summary\" button where students can download a clean text memorandum '
        'of their consultation for their records.\n'
        '• At the bottom, we have our high-visibility chat input, styled with our institutional emerald focus ring, pinned so students always have easy access.\n'
        '• Most importantly, we implemented a top-focused result layout: whenever an answer is generated, it immediately displays at the top under the header, '
        'so students don’t have to scroll down to read the policy resolution."'
    )
    p3_spk.add_run(p3_text).font.size = Pt(11)

    # =========================================================================
    # PART 4: AT LEAST 3 SAMPLE QUESTIONS (MARCEL AVERGONZADO)
    # =========================================================================
    h4 = doc.add_heading(level=1)
    r4 = h4.add_run("Part 4: Live Test Inquiries — 3 Sample Questions (3:45 – 5:15)")
    r4.font.name = "Calibri"
    r4.font.color.rgb = c_primary

    p_spk4 = doc.add_paragraph()
    p_spk4.paragraph_format.space_after = Pt(4)
    r_s4 = p_spk4.add_run("🎙️ ASSIGNED PRESENTER: MARCEL AVERGONZADO (CONTINUED)")
    r_s4.font.name = "Calibri"
    r_s4.font.bold = True
    r_s4.font.color.rgb = c_primary

    # Question 1
    add_callout_box(
        doc,
        "Type or click: 'What courses and undergraduate degree programs are officially offered at TPC?' "
        "Wait 1-2 seconds for retrieval, then show the response bubble, the green verification strip, "
        "and click to expand the 'Inspect Retrieved Policy Excerpts' to show cosine scores."
    )

    p4_q1 = doc.add_paragraph()
    p4_q1.paragraph_format.space_after = Pt(6)
    p4_q1.paragraph_format.line_spacing = 1.2
    p4_q1.add_run("SPEAKING SCRIPT (Sample Question 1 — Academic Scope):\n").bold = True
    p4_q1_text = (
        '"Now let’s run our three test questions.\n\n'
        'Sample Question 1: An in-scope academic inquiry.\n'
        'We type: \"What courses and undergraduate degree programs are officially offered at TPC?\"\n\n'
        '[Wait for output]\n\n'
        'Notice how quickly the response appears right at the top under LATEST POLICY RESOLUTION.\n'
        'The model provides an authoritative, complete answer identifying all 7 CHED-recognized undergraduate programs: '
        'Bachelor of Arts in English Language, Bachelor of Arts in Political Science, Bachelor of Science in Agriculture, '
        'BSAIS, BS Criminology, BS Information Systems, and Bachelor of Early Childhood Education.\n\n'
        'Look at the verification strip below the answer: it shows a High Match confidence of over 90%, '
        'cites \"TPC Student Handbook v.04\", and displays latency in milliseconds.\n'
        'If we expand the \"Inspect Retrieved Policy Excerpts\" drawer, we can see the exact chunks retrieved from the handbook '
        'along with their mathematical cosine similarity scores. This demonstrates full RAG transparency."'
    )
    p4_q1.add_run(p4_q1_text).font.size = Pt(11)

    # Question 2
    add_callout_box(
        doc,
        "Type or click: 'What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?' "
        "Show the answer citing Ordinance 127 and the 10:00 PM to 4:00 AM rule. Show the dynamic follow-up chips at the bottom."
    )

    p4_q2 = doc.add_paragraph()
    p4_q2.paragraph_format.space_after = Pt(6)
    p4_q2.paragraph_format.line_spacing = 1.2
    p4_q2.add_run("SPEAKING SCRIPT (Sample Question 2 — Community & Municipal Policy):\n").bold = True
    p4_q2_text = (
        '"Sample Question 2: A community boarding house and safety policy.\n'
        'We type: \"What are the curfew hours for boarding houses under Talibon Municipal Ordinance 127?\"\n\n'
        '[Wait for output]\n\n'
        'The chatbot accurately answers that under Ordinance Number 127, the mandatory curfew hours are from 10:00 PM to 4:00 AM. '
        'It explains landlord safety obligations, sanitary permits, and fire exit regulations.\n\n'
        'Notice that it cited \"Talibon Ordinance 127\". Below the answer, the previous question on degree programs '
        'was automatically archived into the \"Earlier Inquiries in this Session\" expander, keeping the screen clutter-free. '
        'Also, look at the dynamic follow-up prompt chips generated below: students can click one to immediately explore '
        'boarding house safety standards or penalty schedules."'
    )
    p4_q2.add_run(p4_q2_text).font.size = Pt(11)

    # Question 3 (Negative / Out-of-Scope Test)
    add_callout_box(
        doc,
        "Click the sidebar button '🔴 Out-of-Scope Test (Refusal Guardrail)' or type: "
        "'What is the capital city and total population of Tokyo, Japan?' "
        "Highlight the polite refusal message and notice that it refuses without hallucinating."
    )

    p4_q3 = doc.add_paragraph()
    p4_q3.paragraph_format.space_after = Pt(6)
    p4_q3.paragraph_format.line_spacing = 1.2
    p4_q3.add_run("SPEAKING SCRIPT (Sample Question 3 — Out-of-Scope Refusal Guardrail):\n").bold = True
    p4_q3_text = (
        '"Sample Question 3: The critical negative test — a question the documents CANNOT answer.\n'
        'The project rubric strictly requires that our chatbot handle out-of-scope inquiries without making things up.\n'
        'Let’s test this by asking a completely unrelated general knowledge question: '
        '\"What is the capital city and total population of Tokyo, Japan?\"\n\n'
        '[Wait for output]\n\n'
        'Notice the result! The chatbot does NOT hallucinate or pretend to know. '
        'Because Tokyo’s population is not in the TPC policy corpus, the cosine similarity score fell below our 0.50 threshold. '
        'Our guardrail intercepted the request and safely responded: '
        '\"I apologize, but this topic is outside the official scope of Talibon Polytechnic College institutional policies. '
        'For college-related inquiries, please consult the Registrar or Office of Student Affairs.\"\n\n'
        'This proves our RAG pipeline has strict containment and will never mislead students with fabricated answers.\n\n'
        'Now, I will pass the microphone to Ronald M. Barril to discuss our planned future improvements and conclude our presentation."'
    )
    p4_q3.add_run(p4_q3_text).font.size = Pt(11)

    # =========================================================================
    # PART 5: WHAT YOU WOULD IMPROVE & CONCLUSION (RONALD M. BARRIL)
    # =========================================================================
    h5 = doc.add_heading(level=1)
    r5 = h5.add_run("Part 5: What We Would Improve & Conclusion (5:15 – 6:30)")
    r5.font.name = "Calibri"
    r5.font.color.rgb = c_primary

    p_spk5 = doc.add_paragraph()
    p_spk5.paragraph_format.space_after = Pt(4)
    r_s5 = p_spk5.add_run("🎙️ ASSIGNED PRESENTER: RONALD M. BARRIL")
    r_s5.font.name = "Calibri"
    r_s5.font.bold = True
    r_s5.font.color.rgb = c_primary

    add_callout_box(
        doc,
        "Switch back to showing the GitHub repository page (https://github.com/hackjas1/TPoliCyNav), "
        "briefly scroll through the comprehensive README, point out the .env.example, and show closing presenter slide or camera."
    )

    p5_spk = doc.add_paragraph()
    p5_spk.paragraph_format.space_after = Pt(6)
    p5_spk.paragraph_format.line_spacing = 1.2
    p5_spk.add_run("SPEAKING SCRIPT:\n").bold = True
    p5_text = (
        '"Thank you, Marcel! Good day everyone, I am Ronald M. Barril, and I will present our roadmap for future improvements '
        'and conclude our presentation.\n\n'
        'While TPoliCynav successfully resolves the core challenges of institutional policy retrieval, here are the four concrete '
        'improvements we would implement in future versions:\n\n'
        '1. Vernacular Language Support (Cebuano / Bisaya): While our current model handles English and Tagalog well, '
        'many students in Bohol express complex policy inquiries naturally in Bisaya. Adding bilingual embeddings will further increase accessibility.\n\n'
        '2. Voice-to-Text & Audio Accessibility: Integrating speech-to-text models like Whisper so visually impaired students '
        'or users on mobile devices can speak their policy questions and listen to synthesized audio answers.\n\n'
        '3. Direct Student Information System (SIS) Integration: Connecting the chatbot securely to student clearance databases '
        'so enrolled students can authenticate to check personalized items, such as graduation clearances and remaining scholarship balances.\n\n'
        '4. Dynamic Administrative Knowledge Updates: Building an administrative web upload portal for college deans and coordinators '
        'to re-index new academic calendars and department announcements in real time without restarting the server.\n\n'
        'All source code, Docker configs, documentation, and the .env.example are publicly available in our GitHub repository at '
        'github.com/hackjas1/TPoliCyNav.\n\n'
        'On behalf of Team Kuys — Eduardo Avenido Jr., Christian Paul G. La Rosa, Nielbert Garcia, Marcel Avergonzado, and myself, '
        'Ronald M. Barril — thank you very much for your time and guidance throughout our Generative AI course! '
        'We are now open for any questions."'
    )
    p5_spk.add_run(p5_text).font.size = Pt(11)

    # =========================================================================
    # PART 6: RECORDING & SUBMISSION CHECKLIST (RUBRIC 100/100)
    # =========================================================================
    doc.add_page_break()
    h6 = doc.add_heading(level=1)
    r6 = h6.add_run("✅ Demo Video Recording & Submission Checklist (100/100 Points)")
    r6.font.name = "Calibri"
    r6.font.color.rgb = c_primary

    p_chk_desc = doc.add_paragraph()
    p_chk_desc.paragraph_format.space_after = Pt(8)
    p_chk_desc.add_run(
        "Use this checklist before and after recording your video to ensure you don't lose any points from automatic deductions:"
    )

    checklist_items = [
        ("Video Timing", "Between 5:00 and 8:00 minutes. (Script is designed for ~6:15 at normal speaking pace)."),
        ("Public Access Link", "Verify that https://tpolicynav-production.up.railway.app opens in an Incognito window without login."),
        ("Required Parts Covered", "Covered in order: 1) Problem & Data, 2) Architecture, 3) Walkthrough, 4) 3 Inquiries, 5) Improvements."),
        ("Speaker Rotation", "1. Eduardo Avenido Jr.  |  2. Nielbert Garcia  |  3. Marcel Avergonzado  |  4. Ronald M. Barril."),
        ("Creator Credit", "Christian Paul G. La Rosa credited in group roster as lead creator and system architect."),
        ("Negative Question Tested", "Tokyo population inquiry demonstrated clearly to prove 0.50 Cosine guardrail prevents hallucinations."),
        ("Google Drive / YouTube Sharing", "Set sharing to 'Anyone with the link (Viewer)'. Test video playback in an Incognito window."),
        ("GitHub Repository", "Confirm repo https://github.com/hackjas1/TPoliCyNav is Public with README and .env.example."),
        ("No Committed Secrets", "Double-check that no real API keys are committed in code or commits."),
        ("Submission Bin", "Submit all 3 links together in Google Classroom: 1) Live App URL, 2) Video Link, 3) GitHub Repo URL.")
    ]

    tbl_chk = doc.add_table(rows=len(checklist_items)+1, cols=2)
    tbl_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_chk.rows[0].cells[0].paragraphs[0].add_run("Checklist Item").bold = True
    tbl_chk.rows[0].cells[1].paragraphs[0].add_run("Verification Details").bold = True
    set_cell_background(tbl_chk.rows[0].cells[0], "064E3B")
    set_cell_background(tbl_chk.rows[0].cells[1], "064E3B")
    tbl_chk.rows[0].cells[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    tbl_chk.rows[0].cells[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    for idx, (item, detail) in enumerate(checklist_items, 1):
        row = tbl_chk.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        bg = "F8FAFC" if idx % 2 == 0 else "FFFFFF"
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_margins(c0, top=70, bottom=70, left=90, right=90)
        set_cell_margins(c1, top=70, bottom=70, left=90, right=90)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(f"☐ {item}")
        r0.font.name = "Calibri"
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = c_primary
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(detail)
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = c_dark

    # Save to project root and project_guide
    out_path_root = os.path.join(os.getcwd(), "TPoliCynav_Final_Presentation_Script.docx")
    doc.save(out_path_root)
    print(f"Saved root script: {out_path_root}")

    guide_dir = os.path.join(os.getcwd(), "project_guide")
    if os.path.exists(guide_dir):
        out_path_guide = os.path.join(guide_dir, "TPoliCynav_Final_Presentation_Script.docx")
        doc.save(out_path_guide)
        print(f"Saved guide script: {out_path_guide}")

if __name__ == "__main__":
    build_script_document()
