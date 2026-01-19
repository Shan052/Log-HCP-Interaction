# AI CRM HCP Interaction Logger

An AI-powered CRM application to log, analyze, and manage Healthcare Professional (HCP) interactions using Natural Language input.

This project demonstrates how unstructured interaction notes can be converted into structured CRM data using an AI Assistant, along with intelligent editing, sentiment analysis, history retrieval, and follow-up suggestions.

---

## 🚀 Features (5 AI Tools Implemented)

### 1️⃣ AI Form Auto-Filling (Information Extraction)
- User describes interaction in natural language
- AI extracts:
  - HCP Name
  - Interaction Type
  - Topics Discussed
  - Materials Shared
  - Sentiment
  - Summary
- Auto-fills the CRM form instantly

### 2️⃣ AI-Based Field Editing
- User can correct specific fields via chat
- Example:
  > “Name is not Mukesh, name is Dr. Sumit”
- AI updates only the targeted field without affecting others

### 3️⃣ Sentiment Detection
- Rule-based sentiment detection for accuracy
- Identifies:
  - Positive
  - Neutral
  - Negative
- Overrides unreliable LLM sentiment for critical keywords (e.g., unhappy, not satisfied)

### 4️⃣ Interaction History Retrieval
- Fetches previous interactions of an HCP
- Example:
  > “Show previous interactions of Dr. Mukesh”

### 5️⃣ AI Follow-Up Suggestions
- Suggests next steps based on last interaction sentiment
- Example:
  > “What should be the next step?”

---

## 🏗️ Project Structure

ai_crm_hcp/
│
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── agent.py # AI agent logic
│ ├── tools.py # AI tools (edit, sentiment, history, follow-up)
│ ├── db.py # Database connection
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ ├── config.py # Environment & API keys
│ └── requirements.txt
│
├── frontend/
│ └── react-app/
│ ├── src/
│ │ ├── App.js
│ │ ├── App.css
│ │ └── index.js
│ └── package.json
│
└── README.md


---

## 🛠️ Tech Stack

### Frontend
- React.js
- CSS (custom UI)
- Fetch API

### Backend
- FastAPI
- LangChain
- Groq LLM (LLaMA-based)
- SQLAlchemy
- MySQL

---

## 🧠 AI Architecture

- **LLM**: Groq (LLaMA model)
- **Prompt Engineering**: Structured JSON extraction
- **Hybrid Intelligence**:
  - LLM for extraction
  - Rule-based logic for sentiment & edits (more reliable)

---

## 🗄️ Database

- **Database**: MySQL
- **ORM**: SQLAlchemy
- Stores:
  - HCP interactions
  - Sentiment
  - Topics
  - Follow-up actions
  - Timestamps

---

## ▶️ How to Run the Project

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python -m uvicorn main:app --reload


Backend runs on:

http://127.0.0.1:8000

Frontend Setup
cd frontend/react-app
npm install
npm start


Frontend runs on:

http://localhost:3000

🔁 API Endpoints
POST /chat

Processes user message through AI agent

Request

{
  "message": "Met Dr. Mukesh today. He was unhappy with pricing."
}


Response

{
  "tool": "extract",
  "data": {
    "hcp_name": "Dr. Mukesh",
    "interaction_type": "Meeting",
    "sentiment": "Negative"
  }
}

POST /save

Saves interaction to database

🧪 Sample Test Inputs

Extraction

Met Dr. Mukesh today. We discussed Product X efficacy. He seemed positive.


Edit

Name is not Mukesh, name is Dr. Sumit


History

Show previous interactions of Dr. Mukesh


Follow-up

What should be the next step?

🎯 Assignment Coverage

✔ AI-powered data extraction
✔ Intelligent field editing
✔ Sentiment analysis
✔ History retrieval
✔ Follow-up recommendation
✔ Frontend + Backend integration
✔ Database persistence

👤 Author

Shan 
MCA Student
AI & Full-Stack Developer
