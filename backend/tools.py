from models import Interaction
from sqlalchemy.orm import Session

# ------------------------------
# TOOL 2: EDIT FIELD
# ------------------------------
def edit_field(db: Session, field: str, value: str):
    interaction = db.query(Interaction).order_by(Interaction.id.desc()).first()
    if not interaction:
        return "No interaction found"

    if not hasattr(interaction, field):
        return f"Invalid field {field}"

    setattr(interaction, field, value)
    db.commit()
    return f"{field} updated to {value}"


# ------------------------------
# TOOL 3: SENTIMENT ANALYSIS
# ------------------------------
def detect_sentiment(text: str) -> str:
    text = text.lower()

    negative_words = [
        "unhappy", "not happy", "angry", "upset",
        "disappointed", "pricing issue", "pricing concern",
        "negative", "bad", "poor"
    ]

    positive_words = [
        "happy", "positive", "satisfied",
        "interested", "excited", "good"
    ]

    for word in negative_words:
        if word in text:
            return "Negative"

    for word in positive_words:
        if word in text:
            return "Positive"

    return "Neutral"


# ------------------------------
# TOOL 4: FETCH HCP HISTORY
# ------------------------------
def fetch_history(db: Session, hcp_name: str):
    records = db.query(Interaction).filter(
        Interaction.hcp_name == hcp_name
    ).all()

    if not records:
        return f"No history found for {hcp_name}"

    return [
        {
            "date": r.date,
            "interaction_type": r.interaction_type,
            "sentiment": r.sentiment,
            "summary": r.summary
        }
        for r in records
    ]


# ------------------------------
# TOOL 5: FOLLOW-UP SUGGESTION
# ------------------------------
def suggest_followup(sentiment: str):
    if sentiment == "Positive":
        return "Schedule follow-up meeting and share clinical data."
    if sentiment == "Neutral":
        return "Send product brochure and check back in a week."
    if sentiment == "Negative":
        return "No follow-up required. Revisit strategy later."
    return "No suggestion available."
