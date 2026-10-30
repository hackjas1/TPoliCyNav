# Development of an AI-Driven Retrieval-Augmented Generation Conversational Agent for Institutional Policy Navigation at Talibon Polytechnic College

## Project Proposal & System Architecture (Checkpoint 1 & Bridge to Checkpoint 2)

**MEMBERS:**  
- EDUARDO AVENIDO JR.  
- CHRISTIAN PAUL LAROSA  
- NIELBERT GARCIA  
- MARCEL AVERGONZADO  

---

## PROBLEM STATEMENT

The fundamental challenge facing the Talibon Polytechnic College (TPC) ecosystem is the high cognitive friction students experience when navigating fragmented institutional policies. Students must comply with the comprehensive TPC Student Handbook, which dictates strict academic and behavioral guidelines, as well as external regulations like Talibon Municipal Ordinance No. 127, which governs off-campus boarding houses. Currently, students risk disciplinary infractions or enrollment delays because traditional keyword search systems cannot efficiently retrieve or synthesize highly specific rules hidden within dozens of pages of text. This project proposes building a Generative AI conversational agent capable of semantic retrieval to bypass the limitations of exact-string matching, providing students with highly accurate, context-aware answers to campus policy questions.

---

## TARGET USERS

The primary users of this application are the approximately **4,900 students** currently enrolled at TPC. This demographic ranges from incoming freshmen who require immediate clarification on entrance exam dress codes (such as the strict prohibition of ripped jeans, shorts, and slippers), to graduating seniors navigating 240-hour practical training requirements. A highly critical subset of users includes students residing in local boarding houses, who must balance academic rules with municipal curfews and behavioral mandates enforced by the local Philippine National Police. Secondary stakeholders include the faculty, the Dean of Student Discipline, and the Chief Security Officer, who will utilize the tool as a rapid reference utility to ensure uniform policy enforcement across the campus.

---

## CHOSEN THEME

In strict alignment with the course syllabus requirements, this project adopts the **"Document/Knowledge-Base Q&A Assistant"** theme. The specific application being developed is a campus policy and rules assistant officially titled **"TPoliCynav: The TPC Policy Navigator."**

---

## DATASET SOURCE(S)

To satisfy the foundational data pipeline requirements, a highly curated, domain-specific corpus totaling over 30+ pages (aggregated into 119 overlapping semantic chunks) was collected and processed from official collegiate and municipal publications:

• **TPC Student Handbook v.04 (Latest Approved Edition, 202-Page / 199-Page Corpus):**  
  The primary institutional knowledge base covering academic policies, grading system, GWA computation, admissions & TPCAT protocols, enrollment procedures, academic retention, all 7 official degree programs (BSIS, BSCrim, BSAIS, BSAgri, BAEL, BAPoS, BECEd), graduation requirements, and student disciplinary matrices.

• **Talibon Municipal Ordinance No. 127:**  
  Official local government ordinance detailing regulations for off-campus boarding houses, dormitories, and homestays near TPC, including mandatory CCTV installations, 10:00 PM / 11:00 PM student curfews, and the strict 500-meter alcohol and entertainment prohibition zone around the campus.

• **TPC School Uniform & Dress Code Guide (Handbook Annexes):**  
  Official institutional annex specifying proper wearing etiquette for the General Type A Uniform (untucked blouse for women, polo with sando for men, knee-level skirts, black closed shoes), transition attire for first-year freshmen (plain white shirt and long pants), Criminology uniform types (A, B, C), and the 12 strictly prohibited attires on campus.

• **LGU & PNP Collaborative Security Memorandums:**  
  Documents joint safety monitoring, surprise boarding house inspections, logbook compliance, and curfew enforcement between the college and the Philippine National Police (PNP) Talibon Station.

• **CHED Free Higher Education Guidelines (Republic Act No. 10931):**  
  Outlines free tuition and miscellaneous fee exemption parameters for TPC as a CHED-recognized Local University and College (LUC), along with Tertiary Education Subsidy (TES) eligibility.

• **GSIS Subsidy for STEM (GSSP) Guidelines:**  
  Details scholarship prerequisites and financial grants for qualified dependents of GSIS members pursuing STEM programs, requiring maintenance of at least a 90% GWA.

• **TPC Admissions & 2nd Semester Enrollment Announcements:**  
  Official institutional memos defining freshmen application requirements, examination protocols, and academic advising schedules.

---

## SUCCESS CRITERIA

The success of this foundational pipeline and the resulting prototype is empirically evaluated against the following criteria:

● **Data Sanitization:** The text preprocessing scripts must demonstrably eliminate formatting noise, HTML artifacts, and erratic line breaks without truncating vital policy constraints or numerical data.  
● **Embedding Stability:** The chosen embedding model (`BAAI/bge-small-en-v1.5`) must successfully convert the tokenized text chunks into a uniform 384-dimensional dense vector space without triggering sequence-length truncation errors.  
● **Retrieval Accuracy:** When subjected to user queries, the vector database similarity search must consistently rank the correct institutional document within the top results, successfully bridging semantic gaps (e.g., matching a query about "torn pants" to the document prohibiting "ripped jeans").  
● **Scope Containment:** By employing strict system prompts, the orchestration framework must gracefully refuse queries that fall entirely outside the scope of the 30-page institutional dataset, ensuring zero generative hallucination.

---

## SEAMLESS BRIDGE: FROM CHECKPOINT 1 TO CHECKPOINT 2

The foundational data pipeline and dense representations established in Checkpoint 1 directly power the Checkpoint 2 deliverables:

1. **Embeddings to Cloud Vector Index:** The 119 cleaned and tokenized text chunks and their 384-dimensional dense vectors (`embeddings.npy`) produced in Checkpoint 1 are loaded into a Pinecone Serverless cloud vector database (`tpolicynav`) on AWS `us-east-1`.
2. **Similarity Metric Optimization:** The embedded corpus serves as the empirical evaluation benchmark for comparing **Cosine Similarity, Euclidean Distance ($L_2$), and Dot Product**, validating optimal retrieval accuracy for normalized BGE embeddings.
3. **Knowledge Base to Multi-Prompt Orchestration:** The curated institutional rules form the grounding context for a 3-tier prompt architecture (Strict Policy Assistant, Disciplinary Conduct Advisor, and Scholarship Evaluator), enabling our live RAG Chatbot (`app/rag_chatbot.py`) to synthesize hallucination-free answers with precise canonical citations.

---

## WORKS CITED

1. GenAI Capstone Semester Project Guide.docx.pdf, uploaded: *GenAI Capstone Semester Project Guide.docx.pdf*
2. Talibon Polytechnic College Student Handbook | PDF - Scribd, [https://www.scribd.com/document/712840267/TPC-Student-Handbook-for-August22-2023-Orientation](https://www.scribd.com/document/712840267/TPC-Student-Handbook-for-August22-2023-Orientation)
3. Municipality of Talibon, Bohol. *127- Regulating the Establishment, Management, and operation of apartments, boarding houses, homestay and dormitories near the TPC*, [https://talibon.gov.ph/wp-content/uploads/2026/02/127-Regulating-the-Establishment-Management-and-operation-of-apartments-boarding-houses-homestay-and-dormitories-near-the-TPC.pdf](https://talibon.gov.ph/wp-content/uploads/2026/02/127-Regulating-the-Establishment-Management-and-operation-of-apartments-boarding-houses-homestay-and-dormitories-near-the-TPC.pdf)
4. Local Government Unit of Talibon. *WELCOME BACK | TALIBON POLYTECHNIC COLLEGE – 2ND SEMESTER AY 2025–2026*, [https://talibon.gov.ph/welcome-back-talibon-polytechnic-college-2nd-semester-ay-2025-2026/](https://talibon.gov.ph/welcome-back-talibon-polytechnic-college-2nd-semester-ay-2025-2026/)
5. Local Government Unit of Talibon. *Calling all aspiring Freshmen! - The Local Government Unit of Talibon, Bohol*, [https://talibon.gov.ph/calling-all-aspiring-freshmen/](https://talibon.gov.ph/calling-all-aspiring-freshmen/)
6. Talibon Polytechnic College. *BSA Practicum Request at Talibon College | PDF - Scribd*, [https://www.scribd.com/document/890815185/Updated-LOI-Ponce](https://www.scribd.com/document/890815185/Updated-LOI-Ponce)
7. Philippine National Police & TPC. *PNP and Talibon Polytechnic College Collaborate to Strengthen Student Safety*, [https://talibon.gov.ph/pnp-and-talibon-polytechnic-college-collaborate-to-strengthen-student-safety/](https://talibon.gov.ph/pnp-and-talibon-polytechnic-college-collaborate-to-strengthen-student-safety/)
8. Melendres, J. A. (2026). *2.Data Preprocessing and Embeddings.pdf*, uploaded: *2.Data Preprocessing and Embeddings.pdf*
9. Commission on Higher Education (CHED). *More Filipino students can avail free higher education with 27 newly CHED-recognized LUCs*, [https://legacy.ched.gov.ph/more-filipino-students-can-avail-free-higher-education-with-27-newly-ched-recognized-lucs/](https://legacy.ched.gov.ph/more-filipino-students-can-avail-free-higher-education-with-27-newly-ched-recognized-lucs/)
10. Government Service Insurance System (GSIS). *GSIS Subsidy for Science, Technology, Engineering, and Mathematics (GSSP)*, [https://www.gsis.gov.ph/ginhawa-for-all/gsis-subsidy-for-science-technology-engineering-and-mathematics-gssp/](https://www.gsis.gov.ph/ginhawa-for-all/gsis-subsidy-for-science-technology-engineering-and-mathematics-gssp/)
11. BAAI. (2023). *BAAI/bge-small-en-v1.5 - Hugging Face*, [https://huggingface.co/BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)
