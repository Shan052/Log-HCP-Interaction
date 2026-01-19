from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas import InteractionExtract
from config import GROQ_API_KEY, LLM_MODEL
from tools import (
    edit_field,
    detect_sentiment,
    fetch_history,
    suggest_followup
)
from models import Interaction
import json
import re

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=LLM_MODEL,
    temperature=0
)

PROMPT = ChatPromptTemplate.from_template("""
You are an AI assistant for a medical CRM.

Extract structured JSON STRICTLY in this schema:
{schema}

Rules:
- Return ONLY JSON
- No explanation text

Text:
{message}
""")



def run_agent(message: str, db):
    msg = message.lower()

    edit_match = re.search(r"name is not .* name is (.*)", msg)
    if edit_match:
        return {
            "tool": "edit",
            "field": "hcp_name",
            "value": edit_match.group(1).strip()
        }
    # ---------- SENTIMENT EDIT ----------
    sentiment_only = re.search(
        r"(unhappy|not happy|angry|upset|Negative)",
        msg
    )

    name_or_meeting = re.search(
        r"(met|meeting|call|discussed)",
        msg
    )

    if sentiment_only and not name_or_meeting:
        new_sentiment = detect_sentiment(message)
        return {
            "tool": "edit",
            "field": "sentiment",
            "value": "Negative"
        }
    sentiment_only = re.search(
        r"(positive|happy|good|impress)",
        msg
    )

    if sentiment_only and not name_or_meeting:
        new_sentiment = detect_sentiment(message)
        return {
            "tool": "edit",
            "field": "sentiment",
            "value": "Positive"
        }



    # ---------- TOOL 4: HISTORY ----------
    if "previous" in msg or "history" in msg:
        name = message.split("of")[-1].strip()
        return {
            "tool": "history",
            "result": fetch_history(db, name)
        }

    # ---------- TOOL 5: FOLLOW-UP ----------
    if "next step" in msg or "follow up" in msg:
        last = db.query(Interaction).order_by(Interaction.id.desc()).first()
        sentiment = last.sentiment if last else "Neutral"
        return {
            "tool": "followup",
            "result": suggest_followup(sentiment)
        }

    # ---------- TOOL 1 + 3: EXTRACTION ----------
    schema = InteractionExtract.model_json_schema()

    prompt = PROMPT.format_messages(
        schema=json.dumps(schema, indent=2),
        message=message
    )

    try:
        response = llm.invoke(prompt).content

        # 🔐 SAFE JSON PARSE
        json_text = re.search(r"\{.*\}", response, re.DOTALL)
        if not json_text:
            raise ValueError("No JSON found in LLM response")

        data = json.loads(json_text.group())
        data["sentiment"] = detect_sentiment(message)

        return {
            "tool": "extract",
            "data": data
        }

    except Exception as e:
        print("AI ERROR:", e)
        return {
            "tool": "error",
            "message": "AI failed to extract structured data"
        }
