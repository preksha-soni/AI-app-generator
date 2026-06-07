# 🤖 AI App Generator

> **Natural Language → Complete App Schema** using a 4-stage AI pipeline powered by Google Gemini

---

## 🌟 What It Does

Just describe your app in plain English, and this tool automatically generates a **complete technical blueprint** including:

- 🎨 **UI Schema** — Pages, components, and layouts
- 🔌 **REST API Schema** — Endpoints, methods, request/response formats
- 🗄️ **Database Schema** — Tables, fields, and relations
- 🔐 **Auth & Roles Schema** — User roles and permissions

---

## 🚀 Live Demo

👉 [Try it here](https://your-streamlit-url.streamlit.app) *(replace with your Streamlit URL after deploying)*

---

## 🧠 How It Works — 4-Stage Pipeline

```
User Prompt (plain English)
        │
        ▼
┌─────────────────────┐
│  Stage 1            │  Extract Intent
│  Intent Extraction  │  → app name, features, roles, entities
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 2            │  Design Architecture
│  System Architect   │  → pages, routes, auth flows, integrations
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 3            │  Generate Schemas
│  Schema Generator   │  → UI + API + DB + Auth schemas
└─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Stage 4            │  Validate & Auto-Repair
│  Validator          │  → cross-layer consistency check
└─────────────────────┘
        │
        ▼
  📦 Complete App Blueprint (JSON)
```

---

## ✨ Key Features

- **4-stage LLM pipeline** for structured, reliable output
- **Self-healing JSON repair** — automatically fixes malformed AI output
- **Cross-layer validation** — ensures UI, API, DB and Auth are consistent
- **Interactive Streamlit UI** with real-time progress tracking
- **One-click JSON download** of the complete schema
- **Example prompts** to get started instantly

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| AI Model | Google Gemini 1.5 Flash |
| Language | Python 3 |
| Output Format | JSON |

---

## 💻 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/preksha-soni/AI-app-generator.git
cd AI-app-generator
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Gemini API key**

Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Get a free API key at 👉 [aistudio.google.com](https://aistudio.google.com)

**4. Run the app**
```bash
streamlit run app.py
```

---

## 📌 Example Prompts

- *"Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments"*
- *"Create a todo app with user authentication and team collaboration"*
- *"Build an e-commerce store with product listings, cart, checkout and admin panel"*

---

## 👩‍💻 About

Built by **Preksha Soni** — B.Tech CSE (AI/ML) student at CSMU, Panvel.

This project demonstrates practical skills in:
- LLM API integration & prompt engineering
- Multi-stage AI pipeline design
- Streamlit web app development
- JSON validation and self-healing mechanisms

📧 prekshasoni13@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/prekshasoni) | [GitHub](https://github.com/preksha-soni)
