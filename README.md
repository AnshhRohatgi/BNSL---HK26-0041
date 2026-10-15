# GreenPulse AI - Campus Resource Waste Intelligence Platform

Chakravyuh 1.0 · Domain 2: Sustainable Development · SD-02. A prototype that analyses electricity,
water and paper consumption records. **Hour 1 status:** React dashboard + FastAPI backend serving a
bundled **synthetic** CSV (summary KPIs, per-resource totals, INR costs, data preview).
Upload, validation, anomaly detection, charts, savings and exports come in later hours.

> Sample data is illustrative, not real campus data. Note: the TRD v1.0 describes a single Streamlit app;
> this repo uses the React + FastAPI architecture instead.

## Structure
```
greenpulse-ai/
├── backend/   FastAPI + Pandas (app/, data/, scripts/, requirements.txt, .env.example)
├── frontend/  React + Vite + Tailwind (src/, public/, package.json, .env.example)
├── README.md
└── .gitignore
```

## Run the backend (terminal 1)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_sample_data.py                # optional: regenerates the 270-row CSV
uvicorn app.main:app --reload --port 8000
```
Check: http://localhost:8000/health and http://localhost:8000/api/sample-data (docs: /docs)

## Run the frontend (terminal 2)
```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```
Open http://localhost:5173

## Configuration (no secrets in git)
- `frontend/.env.local` → `VITE_API_BASE_URL` (backend URL)
- `backend/.env.example` → `CORS_ORIGINS` (comma-separated allowed origins). Set it as an environment
  variable (the backend reads the process environment; it does not load `.env` files).

## Git: first commit and push
Create an empty GitHub repo, then from the project root:
```bash
git init -b main
git add .
git status        # confirm no .env files, node_modules or .venv are listed
git commit -m "Hour 1: React + FastAPI skeleton, synthetic sample data, dashboard"
git remote add origin https://github.com/<your-username>/greenpulse-ai.git
git push -u origin main
```

## Deploy (later)
- **Backend (Render):** Web Service, root dir `backend`, build `pip install -r requirements.txt`,
  start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, env `CORS_ORIGINS=<your Vercel URL>`.
- **Frontend (Vercel):** root dir `frontend`, framework Vite, env `VITE_API_BASE_URL=<your Render URL>`.
