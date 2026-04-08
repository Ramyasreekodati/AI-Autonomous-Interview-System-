from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from database.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="candidate") # "candidate" or "admin"

    interviews = relationship("Interview", back_populates="user")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending") # "pending", "active", "completed"
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_score = Column(Float, default=0.0)
    
    # Detailed scores as per explainable scoring requirement
    score_breakdown = Column(JSON, default={
        "answer_quality": 0.0,
        "behavior": 0.0,
        "emotion": 0.0
    })
    reasoning_logs = Column(JSON, default=[])

    user = relationship("User", back_populates="interviews")
    responses = relationship("Response", back_populates="interview")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    category = Column(String) # "technical", "behavioral", etc.
    difficulty = Column(String) # "easy", "medium", "hard"
    expected_keywords = Column(JSON) # ["react", "hooks", "state"]
    ideal_answer = Column(String, nullable=True)

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_text = Column(String)
    score = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    interview = relationship("Interview", back_populates="responses")
