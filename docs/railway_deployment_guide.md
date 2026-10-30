# Deployment Guide: Shipping TPoliCynav to Railway Cloud via GitHub

**Course:** IS Professional Elective #4 — Generative AI Systems  
**Project:** TPoliCynav: The TPC Policy Navigator  
**Authors:** Eduardo Avenido Jr., Christian Paul Larosa, Nielbert Garcia, Marcel Avergonzado  
**Institution:** Talibon Polytechnic College, Bohol, Philippines  
**Checkpoint:** Checkpoint 4 (Deliverable 18: Deployment Evidence)  

---

## 1. Prerequisites Checklist

Before triggering deployment, ensure you have:
- [x] A **GitHub account** with public repository permissions.
- [x] A **Railway account** (connected via GitHub at [railway.app](https://railway.app)).
- [x] Your **Pinecone API Key** and index name (`tpolicynav`).
- [x] Your **Hugging Face Token** (`HF_TOKEN`).

---

## 2. Step-by-Step Deployment Instructions

### Step 1: Initialize Git and Push to Public GitHub
Run the following commands in your workspace root (`d:\THESIS CHATBOT\Tpolicynav_1.0`):

```bash
# 1. Initialize git if not already initialized
git init

# 2. Add all project files
git add .

# 3. Commit the Checkpoints 3 & 4 codebase
git commit -m "feat: complete Checkpoints 3 and 4 RAG chatbot and web UI"

# 4. Set main branch
git branch -M main

# 5. Link your GitHub remote repository (replace with your repo URL)
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/tpolicynav.git

# 6. Push code to GitHub
git push -u origin main
```

> [!IMPORTANT]
> Ensure your GitHub repository visibility is set to **Public** (`Settings` -> `Danger Zone` -> `Change visibility` -> `Make Public`) as required by the course guidelines.

---

### Step 2: Connect Repository to Railway

1. Open your browser and go to [railway.app](https://railway.app/dashboard).
2. Click **"+ New Project"**.
3. Select **"Deploy from GitHub repo"**.
4. Choose your `tpolicynav` repository from the list.
5. Click **"Deploy Now"**.

Railway will automatically detect `railway.json` and the multi-stage `Dockerfile`.

---

### Step 3: Configure Environment Secrets in Railway

1. In your Railway project canvas, click on the **tpolicynav** service card.
2. Navigate to the **"Variables"** tab.
3. Click **"+ New Variable"** and add:
   - `PINECONE_API_KEY`: *(paste your real Pinecone API key)*
   - `PINECONE_INDEX_NAME`: `tpolicynav`
   - `HF_TOKEN`: *(paste your real Hugging Face user access token)*
4. Railway will automatically trigger a redeploy with your encrypted environment variables.

---

### Step 4: Generate Public URL

1. In your service card, go to the **"Settings"** tab.
2. Scroll to the **"Networking"** section.
3. Under **Public Networking**, click **"Generate Domain"**.
4. Railway will issue a public HTTPS domain (e.g., `https://tpolicynav-production.up.railway.app`).
5. Open this URL in an **Incognito Window** to verify:
   - ✅ The app opens immediately without asking for a login.
   - ✅ The green collegiate TPC theme renders crisply.
   - ✅ Clicking a quick-ask button (e.g. *Official Degree Programs*) returns a grounded answer with citations.

---

## 3. Deployment Evidence Artifacts

For your final submission bin and defense presentation, capture and save the following:
1. **Public Live App URL:** `https://tpolicynav-production.up.railway.app` (or your assigned Railway subdomain).
2. **Railway Dashboard Screenshot:** Showing the green active deployment status indicator.
3. **Live Query Verification Screenshot:** Showing the web app answering a student question with TPC citations and confidence score.
4. **GitHub Actions Badge / Run:** Showing green checkmark on the CI evaluation workflow.

