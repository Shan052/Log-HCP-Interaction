from sqlalchemy import Column, Integer, String, Text
from db import Base

class Interaction(Base):
    __tablename__ = "interactions"

    # ======================
    # PRIMARY KEY
    # ======================
    id = Column(Integer, primary_key=True, index=True)

    # ======================
    # HCP DETAILS
    # ======================
    hcp_name = Column(String(100), nullable=False)
    interaction_type = Column(String(50), nullable=False)

    # ======================
    # DATE & TIME
    # ======================
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)

    # ======================
    # INTERACTION CONTENT
    # ======================
    topics_discussed = Column(Text, nullable=True)
    materials_shared = Column(Text, nullable=True)

    # ======================
    # ANALYSIS
    # ======================
    sentiment = Column(String(20), nullable=True)

    # ======================
    # SUMMARY
    # ======================
    summary = Column(Text, nullable=True)
