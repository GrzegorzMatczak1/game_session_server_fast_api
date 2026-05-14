# Browser Game — Project Setup Guide

## Necessary Downloads

| Tool | Where | Notes |
|---|---|---|
| **Laragon** | laragon.org/download | Download the full version (8.6.1+) |
| **Python 3.x** | python.org/downloads | ⚠️ Check **"Add Python to PATH"** during install |
| **VS Code** | code.visualstudio.com | Recommended editor |
| **Git** | git-scm.com/download/win | For version control |

---

## Clone The Repository

Clone all project files from a GitHub repo.

```bash
  git clone https://github.com/GrzegorzMatczak1/game_session_server_fast_api.git
```

---



## Python / FastAPI Setup

```bash
cd C:\projects\browser-game\backend # or whatever the project root is

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Your terminal should now show (venv) prefix
# Install dependencies
pip install fastapi uvicorn

# Save dependencies
pip install -r requirements.txt
```

> ⚠️ Every time you come back to work on the project, activate the venv first:
> `venv\Scripts\activate`

---

## Configure Laragon

By default Laragon serves from `C:\laragon\www`. Point it at your project instead:

1. Install and launch Laragon
2. Right-click the Laragon tray icon → **Preferences**
3. Under **General**, find **Document Root**
4. Change it to: `C:\projects\browser-game\frontend` (or whatever the project root is)
5. Click **Save** and then **Start All**

> After this, `http://localhost` serves your frontend folder directly.

---

## Project Structure

This should be the file structure after all the previous steps.

```
C:\projects\browser-game\
│
├── frontend\                  ← PHP + HTML + CSS
│   ├── index.php
│   ├── game.php
│   └── style.css
│
├── backend\                   ← Python FastAPI
│   ├── main.py
│   ├── requirements.txt
│   └── venv\                  ← created locally, never pushed to Git
│
├── .gitignore
└── PROJECT_SETUP.md
```

---
## Running the Project

You need **two terminals** every time you work on this project.

**Terminal 1 — FastAPI backend:**
```bash
cd C:\projects\browser-game\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Laragon — PHP frontend:**
- Click **Start All** or start **Apache** in the Laragon tray

---

## Step 8 — Testing

Test each piece in order:

### 1. FastAPI directly
Open your browser and visit:
```
http://localhost:8000/api/health
```
Expected response:
```json
{"status": "ok", "message": "Backend is running"}
```

### 2. FastAPI interactive docs
```
http://localhost:8000/docs
```
Swagger UI loads automatically — useful for testing endpoints manually.

### 3. PHP frontend
```
http://localhost
```
You should see a **green status box** confirming the backend is connected.
If the box is red, FastAPI is not running — go back to Terminal 1.

---

## Checklist

- [ ] Laragon installed and **Start All** clicked
- [ ] `venv` created and activated
- [ ] `pip install -r requirements.txt` done
- [ ] `http://localhost:8000/api/health` returns JSON
- [ ] `http://localhost` shows green status box
- [ ] `.gitignore` in place (venv excluded)
