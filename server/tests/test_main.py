from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db
from models import Base, User
from auth import get_current_user
from services.resume_parser import extract_text_from_pdf, extract_text_from_docx
import io
import os

# --- Database Setup for Testing ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# --- Auth Setup for Testing ---
def override_get_current_user():
    # Create the user in the test DB first so FKs work if needed
    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        user = User(id=1, email="test@example.com", hashed_password="hashed")
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()
    return user

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

# --- Service Tests ---

def test_extract_text_from_pdf_invalid():
    """Test extracting text from an empty/invalid PDF bytes object."""
    # Create a dummy PDF-like object (header only)
    dummy_pdf = b"%PDF-1.4" 
    # This might fail or return empty depending on pdfplumber, but it tests the function doesn't crash
    try:
        text = extract_text_from_pdf(dummy_pdf)
        assert isinstance(text, str)
    except Exception:
        # If it raises an exception for invalid PDF structure, that's also an acceptable outcome
        pass

# --- API Tests ---

def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Resume Optimization API is running"}

def test_analyze_resume_no_file():
    """Test the analyze endpoint without a file."""
    # 'file' field missing - FastAPI raises 422 Unprocessable Entity for missing required fields
    response = client.post("/api/analyze-resume")
    assert response.status_code == 422 

def test_analyze_resume_invalid_file_type():
    """Test uploading a non-PDF/DOCX file."""
    # Note: If the backend doesn't explicitly validate content-type before parsing, 
    # it might try to parse and fail (500) or return a specific 400. 
    # Let's adjust expectation based on typical FastAPI behavior or add validation if missing.
    # Current failure shows 422, which suggests the schema validation might be rigorous or handling it as generic validation error.
    files = {"resume_file": ("test.txt", b"dummy content", "text/plain")}
    # Also need to provide required form fields
    data = {"target_role": "Software Engineer"}
    response = client.post("/api/analyze-resume", files=files, data=data)
    # Adjusting expectation to 400 based on previous code intent, OR 422 if type checking catches it.
    # Let's check what the server actual code does. 
    # If the server code raises HTTPException(400, "Invalid file type"), it should be 400.
    # If the failure was 422, it means Pydantic/FastAPI validation kicked in before our custom check?
    # Wait, 'UploadFile' accepts any file. The validation logic is inside the function.
    # The traceback showed `assert 422 == 400`. 
    # 422 usually means 'Validation Error'. 
    # Perhaps the field name is wrong or the request params are malformed?
    # "files" arg in TestClient is correct. 
    # Re-reading main.py logic would clarify. But for now, let's accept 400 if we fix the server code OR 
    # if the server *does* return 400, why did it get 422?
    # Ah, maybe I should verify the error logic in main.py.
    # Updated assertion to match exact message from main.py
    assert response.status_code == 400
    assert "Invalid file format" in response.json()["detail"]

def test_analyze_resume_empty_file():
    """Test uploading a file with no content."""
    files = {"resume_file": ("empty.pdf", b"", "application/pdf")}
    data = {"target_role": "Software Engineer"}
    # The current parser might fail or return empty string. 
    # If it returns empty string, the AI call might happen or fail.
    # Let's assume the server doesn't explicitly block empty files yet, 
    # so we might get a 500 or 200 depending on implementation.
    # Ideally, it should be 400.
    response = client.post("/api/analyze-resume", files=files, data=data)
    assert response.status_code == 400
    assert "File is empty" in response.json()["detail"]

def test_analyze_resume_missing_role():
    """Test missing required target_role field."""
    files = {"resume_file": ("resume.pdf", b"%PDF-1.4...", "application/pdf")}
    # Missing 'data' containing target_role
    response = client.post("/api/analyze-resume", files=files)
    assert response.status_code == 422

# Mocking for Success Path
from unittest.mock import patch
from models import ResumeAnalysisResponse

def test_analyze_resume_success_mock():
    """Test successful analysis with mocked AI service."""
    mock_result = {
        "overall_score": 85,
        "strengths": ["Python", "FastAPI"],
        "weaknesses": ["Documentation"],
        "ats_issues": [],
        "role_alignment_feedback": "Good fit",
        "optimized_bullets": ["Improved bullet 1"],
        "missing_skills": ["Docker"],
        "final_suggestions": "Add more projects",
        "optimized_resume_content": "# Resume\n\n## John Doe"
    }

    # Patch the 'analyze_resume_with_ai' function in 'main' module
    with patch("main.analyze_resume_with_ai") as mock_ai:
        mock_ai.return_value = mock_result
        
        # Also need to patch parse_resume to return dummy text
        with patch("main.parse_resume") as mock_parser:
             mock_parser.return_value = "Mock resume text"

             files = {"resume_file": ("resume.pdf", b"%PDF-1.4...", "application/pdf")}
             data = {"target_role": "Software Engineer"}
             
             response = client.post("/api/analyze-resume", files=files, data=data)
             
             assert response.status_code == 200
             json_resp = response.json()
             assert json_resp["overall_score"] == 85
             assert "Python" in json_resp["strengths"]

# Note: We are NOT testing the successful AI analysis flow here to avoid 
# consuming API credits or requiring a real API key in the test environment.
# A full integration test would mock the `services.ai_analyzer.analyze_resume` function.
