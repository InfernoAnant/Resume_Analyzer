<<<<<<< HEAD
# Resume Analyzer AI

An intelligent platform that helps job seekers create ATS-friendly resumes and match them with relevant opportunities.

## Prerequisites

- Node.js (v18+)
- Python (v3.9+)

## How to Run Manually

You need to run the **Backend** and **Frontend** in two separate terminals.

### 1. Start the Backend (API)

Open a terminal in the project root:

```powershell
# Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\activate

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### 2. Start the Frontend (UI)

Open a **new** terminal in the project root:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies (only needed first time)
npm install

# Run the dev server
npm run dev
```

The UI will be available at `http://localhost:3000`.

## Quick Start (Script)

Alternatively, you can run the helper script from the root directory:

```powershell
.\run_app.ps1
```
=======
# Resume_Analyzer
>>>>>>> 539bc50d0176e77dc3626a1c557cffb47c734c04
