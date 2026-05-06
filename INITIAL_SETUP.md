# Browser Game — Project Setup Guide

## Prerequisites — Downloads

| Tool | Where | Notes |
|---|---|---|
| **Laragon** | laragon.org/download | Download the full version (8.6.1+) |
| **Python 3.x** | python.org/downloads | ⚠️ Check **"Add Python to PATH"** during install |
| **VS Code** | code.visualstudio.com | Recommended editor |
| **Git** | git-scm.com/download/win | For version control |

---

## Project Structure

Keep everything in **one folder outside of Laragon's www**. This folder will become your single Git repository.

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
└── README.md
```

---

## Step 1 — Create the Folder Structure

Open a terminal (`Win + R` → `cmd`) and run:

```bash
mkdir C:\projects\browser-game
mkdir C:\projects\browser-game\frontend
mkdir C:\projects\browser-game\backend
cd C:\projects\browser-game
```

---

## Step 2 — Python / FastAPI Setup

```bash
cd C:\projects\browser-game\backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Your terminal should now show (venv) prefix
# Install dependencies
pip install fastapi uvicorn

# Save dependencies
pip freeze > requirements.txt
```

> ⚠️ Every time you come back to work on the project, activate the venv first:
> `venv\Scripts\activate`

---

## Step 3 — Base FastAPI App

Create `C:\projects\browser-game\backend\main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend is running"}
```

---

## Step 4 — Base PHP Frontend

Create `C:\projects\browser-game\frontend\index.php`:

```php
<?php
// Call the FastAPI health endpoint
$ch = curl_init("http://localhost:8000/api/health");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$error = curl_error($ch);
curl_close($ch);

$data = $response ? json_decode($response, true) : null;
$connected = $data && $data['status'] === 'ok';
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Browser Game</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Browser Game</h1>

  <div class="status <?= $connected ? 'ok' : 'fail' ?>">
    <?php if ($connected): ?>
      ✅ Backend connected — <?= htmlspecialchars($data['message']) ?>
    <?php else: ?>
      ❌ Backend not reachable — is FastAPI running on port 8000?
    <?php endif; ?>
  </div>
</body>
</html>
```

Create `C:\projects\browser-game\frontend\style.css`:

```css
body {
  font-family: Arial, sans-serif;
  background: #1a1a2e;
  color: #eee;
  text-align: center;
  padding: 40px;
}

.status {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 1.1rem;
}

.status.ok   { background: #1a472a; border: 1px solid #2ecc71; }
.status.fail { background: #4a1a1a; border: 1px solid #e74c3c; }
```

---

## Step 5 — Configure Laragon

By default Laragon serves from `C:\laragon\www`. Point it at your project instead:

1. Install and launch Laragon
2. Right-click the Laragon tray icon → **Preferences**
3. Under **General**, find **Document Root**
4. Change it to: `C:\projects\browser-game\frontend`
5. Click **Save** and then **Start All**

> After this, `http://localhost` serves your frontend folder directly.

---

## Step 6 — Git Setup

Create `C:\projects\browser-game\.gitignore`:

```
# Python
backend/venv/
backend/__pycache__/
*.pyc
*.pyo

# System
.DS_Store
Thumbs.db
```

Then initialise the repo and push to GitHub:

```bash
cd C:\projects\browser-game

git init
git add .
git commit -m "initial project setup"

# Create a new repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/browser-game.git
git branch -M main
git push -u origin main
```

---

## Step 7 — Running the Project

You need **two terminals** every time you work on this project.

**Terminal 1 — FastAPI backend:**
```bash
cd C:\projects\browser-game\backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

**Laragon — PHP frontend:**
- Click **Start All** in the Laragon tray

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
- [ ] `pip install fastapi uvicorn` done
- [ ] `requirements.txt` generated
- [ ] `http://localhost:8000/api/health` returns JSON
- [ ] `http://localhost` shows green status box
- [ ] `.gitignore` in place (venv excluded)
- [ ] Project pushed to GitHub

---

## Cloning on Another Machine

If you or someone else clones the repo fresh:

```bash
git clone https://github.com/YOUR_USERNAME/browser-game.git
cd browser-game/backend

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Then follow Steps 5 and 7 as normal.