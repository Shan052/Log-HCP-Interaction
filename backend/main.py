from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import get_db
from models import Interaction
from schemas import (
    ChatRequest,
    InteractionCreate,
    StatusResponse
)
from agent import run_agent

# ======================
# FASTAPI APP
# ======================pytho
app = FastAPI(title="AI CRM HCP Assistant")

# ======================
# CORS (React ke liye)
# ======================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# HEALTH CHECK
# ======================
@app.get("/")
def health():
    return {"status": "AI CRM Backend Running"}

# ======================
# CHAT → AI EXTRACTION
# ======================
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    return run_agent(req.message, db)


# ======================
# SAVE INTERACTION
# ======================
@app.post("/save", response_model=StatusResponse)
def save_interaction(
    data: InteractionCreate,
    db: Session = Depends(get_db)
):
    """
    Save validated interaction to MySQL
    """
    interaction = Interaction(**data.dict())
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return {"status": "saved successfully"}

# ======================
# FETCH HCP HISTORY (OPTIONAL API)
# ======================
@app.get("/history/{hcp_name}")
def get_history(hcp_name: str, db: Session = Depends(get_db)):
    records = db.query(Interaction).filter(
        Interaction.hcp_name == hcp_name
    ).all()

    if not records:
        raise HTTPException(
            status_code=404,
            detail="No interactions found"
        )

    return records
