from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analyses = relationship("ResumeAnalysis", back_populates="owner")

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    original_text = Column(Text) # Storing extracted text to save space
    analysis_json = Column(JSON) # Storing the AI result
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="analyses")

# Pydantic Models for Response/Request
from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    username: str # OAuth2PasswordRequestForm uses 'username' for email
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ResumeAnalysisResponse(BaseModel):
    overall_score: int
    strengths: List[str]
    weaknesses: List[str]
    ats_issues: List[str]
    role_alignment_feedback: str
    optimized_bullets: List[str]
    missing_skills: List[str]
    final_suggestions: str
    optimized_resume_content: str

class UserResponse(BaseModel):
    id: int
    email: str
    usage_count: int = 0
    
    class Config:
        from_attributes = True
