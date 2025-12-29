import sys
import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add server directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_db
from models import Base, User, ResumeAnalysis
from auth import get_current_user

# --- Database Setup (Isolated) ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Mock User Helper
class SimpleUser:
    def __init__(self, id, email):
        self.id = id
        self.email = email

# Reset dependency overrides and set DB override
# app.dependency_overrides = {}
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Helper mock result that satisfies ResumeAnalysisResponse schema
VALID_MOCK_RESPONSE = {
    "overall_score": 85,
    "strengths": ["Python"],
    "weaknesses": ["None"],
    "ats_issues": [],
    "role_alignment_feedback": "Good",
    "optimized_bullets": ["Bullet"],
    "missing_skills": [],
    "final_suggestions": "Hire",
    "optimized_resume_content": "Resume Content"
}

def test_usage_limit_boundary_conditions():
    """Test 49 (OK) vs 50 (Blocked) for a single user."""
    
    # 1. Create a User with 49 entries
    user_id = 100
    db = TestingSessionLocal()
    user_49_db = User(id=user_id, email="user49@example.com", hashed_password="pw")
    db.add(user_49_db)
    
    # Add 49 records
    for i in range(49):
        db.add(ResumeAnalysis(user_id=user_id, original_text="x", analysis_json={}))
    db.commit()
    db.close()

    # Override Auth to return our SimpleUser
    app.dependency_overrides[get_current_user] = lambda: SimpleUser(id=user_id, email="user49@example.com")
    
    # Mock services
    with patch("main.analyze_resume_with_ai") as mock_ai, \
         patch("main.parse_resume") as mock_parser:
        mock_ai.return_value = VALID_MOCK_RESPONSE
        mock_parser.return_value = "text"

        # Try 50th Upload (Should Succeed)
        files = {"resume_file": ("resume.pdf", b"content", "application/pdf")}
        data = {"target_role": "Dev"}
        response = client.post("/api/analyze-resume", files=files, data=data)
        assert response.status_code == 200, f"49th upload failed: {response.text}"
        
        # Now DB should have 50.
        # Try 51st Upload (Should Fail)
        response = client.post("/api/analyze-resume", files=files, data=data)
        assert response.status_code == 403, "51st upload should be blocked"
        assert "usage limit exceeded" in response.json()['detail'].lower()

def test_usage_limit_isolation():
    """Test that User A being full doesn't block User B."""
    
    db = TestingSessionLocal()
    # User A: Full (50)
    user_full_db = User(id=200, email="full@example.com", hashed_password="pw")
    db.add(user_full_db)
    for _ in range(50):
        db.add(ResumeAnalysis(user_id=200, original_text="x", analysis_json={}))
        
    # User B: New (0)
    user_new_db = User(id=201, email="new@example.com", hashed_password="pw")
    db.add(user_new_db)
    db.commit()
    db.close()
    
    # 1. Verify User A is blocked
    app.dependency_overrides[get_current_user] = lambda: SimpleUser(id=200, email="full@example.com")
    files = {"resume_file": ("resume.pdf", b"content", "application/pdf")}
    data = {"target_role": "Dev"}
    
    response = client.post("/api/analyze-resume", files=files, data=data)
    assert response.status_code == 403
    
    # 2. Verify User B is OK
    app.dependency_overrides[get_current_user] = lambda: SimpleUser(id=201, email="new@example.com")
    
    with patch("main.analyze_resume_with_ai") as mock_ai, \
         patch("main.parse_resume") as mock_parser:
        mock_ai.return_value = VALID_MOCK_RESPONSE
        mock_parser.return_value = "text"
        
        response = client.post("/api/analyze-resume", files=files, data=data)
        assert response.status_code == 200
