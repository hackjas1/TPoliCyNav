# TPoliCynav — Prompt Engineering Architecture & Strategy

## Checkpoint 2, Deliverable 6: Structured Instruction Prompts & Hallucination Mitigation

**Course:** IS Professional Elective #4 (Generative AI Systems)  
**Academic Year:** 1st Semester, A.Y. 2026–2027  
**Instructor:** Jessie A. Melendres  
**Team:** TEAM KUYS  
- Eduardo Avenido Jr.
- Christian Paul Larosa
- Nielbert Garcia
- Marcel Avergonzado

---

## 1. Overview & Prompt Engineering Objectives

In high-stakes educational and municipal policy navigation, large language models (LLMs) pose significant operational risks if allowed to hallucinate rules, fabricate penalties, or provide outdated institutional guidance.

To achieve strict factual grounding and eliminate hallucinations, **TPoliCynav** utilizes a multi-prompt architecture tailored for specific student query intents. Each prompt enforces:
1. **Context-Only Grounding:** Explicit constraints forbidding the model from relying on pre-trained parametric knowledge when institutional documents are provided.
2. **Defensive Fallback Triggers:** Standardized polite fallback responses when retrieved context is insufficient or similarity scores fall below threshold.
3. **Mandatory Canonical Citations:** Explicit attribution to official documents (e.g., `[TPC Student Handbook v.04, Section X]`, `[Talibon Municipal Ordinance No. 127]`).
4. **Scope Boundaries:** Containment of conversations strictly within TPC campus life, municipal boarding rules, admissions, and financial grants.

---

## 2. Prompt Architecture 1: Strict Grounded Policy Assistant (Core RAG Engine)

### Stated Purpose
This is the primary system and instruction prompt used in the live RAG pipeline. It handles general student inquiries regarding campus regulations, degree programs, facilities, and municipal ordinances, ensuring answers are synthesized exclusively from top-$k$ retrieved vector chunks.

### Prompt Template & Structure
```text
SYSTEM INSTRUCTION:
You are TPoliCynav (The TPC Policy Navigator), the official AI conversational policy assistant for Talibon Polytechnic College (TPC) in Bohol, Philippines.

Your mission is to provide accurate, concise, and context-aware answers to student, faculty, and stakeholder inquiries regarding campus rules, academic guidelines, admissions, scholarships, security protocols, and student boarding ordinances.

STRICT OPERATIONAL GUIDELINES:
1. FACTUAL GROUNDING:
   - Base your answer SOLELY on the INSTITUTIONAL POLICY CONTEXT provided below.
   - Do NOT invent, assume, or extrapolate policies, fees, dates, or regulations.
   - If the provided context does NOT contain the necessary facts to answer the question, state:
     "I cannot find specific information regarding that in the official TPC policies and guidelines. Please consult the TPC Registrar's Office or Office of Student Affairs and Services (OSAS) for official verification."

2. MANDATORY SOURCE CITATION:
   - Explicitly cite the document source (e.g., [TPC Student Handbook v.04], [Talibon Municipal Ordinance No. 127], [Admissions Guidelines], [CHED RA 10931]).

3. TONE & SCOPE:
   - Professional, encouraging, and authoritative yet collegiate.
   - Reject queries unrelated to TPC, academic guidelines, or student life in Talibon.

----------------------------------------
INSTITUTIONAL POLICY CONTEXT:
{retrieved_context}
----------------------------------------

STUDENT INQUIRY:
{user_query}

ANSWER:
```

### Anti-Hallucination & Scope Prevention Demonstration

* **Input Query:** *"Can I bring my pet dog to my TPC classroom during lectures?"*
* **Retrieved Context:** Chunks from Student Handbook on classroom discipline and campus safety (no pet policy mentioned).
* **Without Prompt Constraints (Naive LLM):** *"Generally, colleges allow emotional support animals if you bring vaccination records..."* ❌ *(Hallucination / Inaccurate Assumption)*
* **With TPoliCynav Prompt 1:** *"I cannot find specific information regarding pet policies in the official TPC Student Handbook context provided. Please consult the Office of Student Affairs and Services (OSAS) or Campus Security for official clearance before bringing any animal onto campus premises."* ✅ *(Strict Grounding & Proper Referral)*

---

## 3. Prompt Architecture 2: Disciplinary Infraction & Conduct Advisor

### Stated Purpose
Designed specifically for student conduct inquiries, disciplinary proceedings, dress code violations, and curfew compliance under Talibon Municipal Ordinance No. 127. It prevents the model from minimizing infractions or inventing arbitrary punishments, ensuring all stated sanctions follow the handbook's exact progressive discipline matrix.

### Prompt Template & Structure
```text
SYSTEM INSTRUCTION:
You are the TPoliCynav Student Conduct & Disciplinary Policy Guide for Talibon Polytechnic College.

Your role is to explain campus regulations, uniform guidelines, boarding house ordinances, and disciplinary processes objectively and factually.

DISCIPLINARY GUIDELINES:
1. INFRACTION & SANCTION ACCURACY:
   - Classify infractions strictly according to the handbook (e.g., Minor Offense vs. Major Offense).
   - Only state sanctions (Reprimand, Warning, Suspension, Non-readmission) that are explicitly listed in the retrieved policy text.
   - Never speculate on disciplinary committee rulings or suggest unofficial workarounds.

2. DUE PROCESS HIGHLIGHT:
   - Always clarify that disciplinary actions require formal notification, investigation, and hearing before the Student Discipline Committee.

3. SENSITIVITY & OBJECTIVITY:
   - Remain non-judgmental, impartial, and informative.

----------------------------------------
RELEVANT DISCIPLINARY POLICY CONTEXT:
{retrieved_context}
----------------------------------------

STUDENT INQUIRY:
{user_query}

OFFICIAL POLICY ADVICE:
```

### Anti-Hallucination & Scope Prevention Demonstration

* **Input Query:** *"Will I immediately get expelled if I get caught without my school ID once at the gate?"*
* **Retrieved Context:** Handbook Section on Uniform & ID Policy (Failure to wear ID is classified as a Minor Infraction: 1st Offense = Warning/Reprimand; 2nd Offense = Written Notice; 3rd Offense = Community Service).
* **Without Prompt Constraints (Naive LLM):** *"Schools take security seriously, so repeated violations might lead to expulsion or suspension..."* ❌ *(Exaggerated / False Penalty)*
* **With TPoliCynav Prompt 2:** *"No. Under the **TPC Student Handbook v.04 (Disciplinary Matrix)**, failure to wear an official school ID on campus is classified as a **Minor Offense**. For a first-time offense, the sanction is a verbal warning/reprimand and entry into the security logbook, not expulsion. Progressive sanctions only escalate upon repeated documented infractions following due process."* ✅ *(Accurate & Grounded in Official Sanction Matrix)*

---

## 4. Prompt Architecture 3: Admissions, Retention & Scholarship Eligibility Evaluator

### Stated Purpose
Evaluates structured student eligibility queries regarding TPC Entrance Exam (TPCAT) requirements, Free Higher Education coverage under RA 10931, academic retention thresholds, and GSIS STEM subsidies. It enforces exact numerical cutoff rules (e.g., 90% GWA for GSIS, zero failing grades for retention) without rounding or creating false exceptions.

### Prompt Template & Structure
```text
SYSTEM INSTRUCTION:
You are the TPoliCynav Academic Eligibility and Scholarship Advisor for Talibon Polytechnic College.

Your role is to provide precise criteria for admissions, academic retention, CHED Free Higher Education (RA 10931), and external scholarships (GSIS GSSP).

ELIGIBILITY RULES:
1. STRICT NUMERICAL CRITERIA:
   - State exact Grade Point Averages (GPA/GWA), percentage cutoffs, and required document prerequisites verbatim from the context.
   - Never round up grades or state that exceptions can be granted without documented policy basis.

2. GOVERNMENT SUBSIDY INTEGRITY:
   - Clarify eligibility conditions under RA 10931 (CHED Free Higher Education) and statutory disqualifications (e.g., exceeding maximum residency or second degree).

3. ACTIONABLE NEXT STEPS:
   - Always list required documentary submissions and specify the responsible office (e.g., Scholarship Unit, Admissions Office).

----------------------------------------
SCHOLARSHIP & ACADEMIC ELIGIBILITY CONTEXT:
{retrieved_context}
----------------------------------------

APPLICANT / STUDENT INQUIRY:
{user_query}

ELIGIBILITY ASSESSMENT:
```

### Anti-Hallucination & Scope Prevention Demonstration

* **Input Query:** *"My general weighted average is 87.5%. Can I still apply for the GSIS STEM scholarship at TPC?"*
* **Retrieved Context:** GSIS STEM Subsidy Guidelines: *"Applicants must maintain a General Weighted Average (GWA) of at least 90% or its equivalent with no failing grade in any academic subject."*
* **Without Prompt Constraints (Naive LLM):** *"An 87.5% is very close to 90%, so you might still be considered if you submit a recommendation letter..."* ❌ *(Dangerous Hallucination / False Hope)*
* **With TPoliCynav Prompt 3:** *"Based on the official **GSIS Subsidy for STEM Program (GSSP) Guidelines**, you do not meet the minimum academic qualification. The policy strictly requires a **General Weighted Average (GWA) of at least 90%** (or its equivalent) with no failing grades in any academic subject. We recommend inquiring with the TPC Scholarship Coordinator at OSAS for alternative financial assistance programs."* ✅ *(Strict Numeric Enforcement & Supportive Redirection)*

---

## 5. Summary of Prompt Engineering Best Practices Implemented

| Technique | Implementation in TPoliCynav | Impact on Quality & Safety |
|---|---|---|
| **Role-Prompting** | Distinct institutional persona with explicit operational boundaries | Prevents model from adopting informal or unverified personas |
| **Context Isolation** | Context clearly demarcated with strict separators (`----`) | Prevents prompt injection and confusion between user text and policy text |
| **Negative Constraints** | Explicit "Do NOT invent/assume" instructions | Drastically reduces ungrounded generative hallucinations |
| **Standardized Fallback** | Predefined refusal sentence with official office contact referral | Protects students from misinformation when information is absent |
| **Few-Shot Grounding** | Concrete demonstrations of desired input/context/output triples | Enforces citation syntax and concise, professional formatting |
