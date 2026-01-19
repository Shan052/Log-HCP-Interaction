from pydantic import BaseModel, Field
from typing import Optional

# ======================
# CHAT REQUEST
# ======================
class ChatRequest(BaseModel):
    message: str = Field(..., example="Met Dr. Sumit today, discussed product X")

# ======================
# AI EXTRACTED DATA
# ======================
class InteractionExtract(BaseModel):
    hcp_name: str
    interaction_type: str
    date: str
    time: str
    topics_discussed: Optional[str] = ""
    materials_shared: Optional[str] = ""
    sentiment: Optional[str] = "Neutral"
    summary: str

# ======================
# SAVE TO DATABASE
# ======================
class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    date: str
    time: str
    topics_discussed: Optional[str] = ""
    materials_shared: Optional[str] = ""
    sentiment: Optional[str] = "Neutral"
    summary: str

# ======================
# GENERIC RESPONSE
# ======================
class StatusResponse(BaseModel):
    status: str
