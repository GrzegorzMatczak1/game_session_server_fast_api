
# Browser Game — Project Setup Guide

## Prerequisites — Downloads

| Tool | Where | Notes |
|---|---|---|
| **Node.js** | nodejs.org | Required for the React/Vite frontend (Version 18+ recommended) |
| **Python 3.x** | python.org/downloads | Check **"Add Python to PATH"** during install |
| **VS Code** | code.visualstudio.com | Recommended editor |
| **Git** | git-scm.com/download/win | For version control |

---

## Project Structure

The repository is structured as a monorepo containing both the frontend and backend codebases.


```

browser-game/
│
├── frontend/                  ← React + TypeScript + Vite
│   ├── src/
│   ├── package.json
│   └── ...
│
├── backend/                   ← Python FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── venv/                  ← Created locally, ignored by Git
│
├── .gitignore
└── README.md

```

---

## First Time Setup (Cloning the Project)

If you have just cloned the repository, follow these steps to install dependencies for both the backend and frontend.

### 1. Backend Setup (FastAPI)

Open your terminal and run the following commands:

```bash
# Navigate to the backend directory
cd browser-game/backend

# Create a local Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all backend dependencies
pip install -r requirements.txt

```

> Every time you open a new terminal to work on the backend, you must activate the virtual environment first: `venv\Scripts\activate` (or source equivalent).

### 2. Frontend Setup (React / TypeScript)

Open a second terminal window or navigate out of the backend directory, then run:

```bash
# Navigate to the frontend directory
cd browser-game/frontend

# Install all Node modules and dependencies
npm install

```

---

## Running the Project

You will need **two separate terminals** running simultaneously to develop locally.

### Terminal 1 — FastAPI Backend

```bash
cd browser-game/backend
# Activate venv if you haven't already
venv\Scripts\activate
# Start the live-reloading API server
uvicorn main:app --reload --port 8000

```

### Terminal 2 — React Frontend

```bash
cd browser-game/frontend
# Start the Vite development server
npm run dev
```

---

## Local Verification & Testing

Once both servers are running, verify that everything is communicating properly:

### 1. FastAPI Direct Health Check

Visit `http://localhost:8000/api/health` in your browser. You should see:

```json
{"status": "ok", "message": "Backend is running"}

```

### 2. FastAPI Interactive API Docs

Visit `http://localhost:8000/docs` to open the interactive Swagger UI. This allows you to test endpoints manually as they are built.

### 3. React Frontend UI

Open the URL printed in Terminal 2 (typically `http://localhost:5173`).

* If the backend is running properly, the application will display a **green success status**.
* If it displays a red failure message, double-check that Terminal 1 is still actively running on port 8000.