from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class CandidateSession(Base):
    __tablename__ = "candidate_sessions"

    id = Column(String, primary_key=True, index=True)
    candidate_name = Column(String, index=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="started") # started, completed, failed
    overall_score = Column(Float, nullable=True)
    recommendation = Column(String, nullable=True) # HIRE, REJECT, PENDING
    final_report_url = Column(String, nullable=True)

    # Relationships
    answers = relationship("CandidateAnswer", back_populates="session")
    alerts = relationship("AlertLog", back_populates="session")

class CandidateAnswer(Base):
    __tablename__ = "candidate_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("candidate_sessions.id"))
    question_id = Column(Integer)
    answer_text = Column(String)
    relevance_score = Column(Float)
    detailed_feedback = Column(JSON) # Detailed AI feedback

    session = relationship("CandidateSession", back_populates="answers")

class AlertLog(Base):
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("candidate_sessions.id"))
    type = Column(String) # Focus, Emotion, Movement, Other
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    severity = Column(String) # Low, Medium, High

    session = relationship("CandidateSession", back_populates="alerts")
