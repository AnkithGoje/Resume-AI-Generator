from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from services.resume_parser import parse_resume
from services.ai_analyzer import analyze_resume_with_ai
from models import ResumeAnalysisResponse
import models
import auth
from database import engine, get_db
import json

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Optimization API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Routes ---

@app.post("/api/auth/signup", response_model=models.Token)
def signup(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = auth.create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/token", response_model=models.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=models.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    usage_count = db.query(models.ResumeAnalysis).filter(models.ResumeAnalysis.user_id == current_user.id).count()
    return {
        "id": current_user.id,
        "email": current_user.email,
        "usage_count": usage_count
    }

# --- Protected Analysis Route ---

@app.post("/api/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    target_role: str = Form(...),
    job_description: str = Form(None),
    experience_level: str = Form(None),
    resume_file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Check Usage Limit
    usage_count = db.query(models.ResumeAnalysis).filter(models.ResumeAnalysis.user_id == current_user.id).count()
    if usage_count >= 50:
        raise HTTPException(
            status_code=403, 
            detail="Usage limit exceeded. You have reached the maximum of 50 resume analyses."
        )

    if not resume_file.filename.endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload PDF or DOCX.")

    contents = await resume_file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="File is empty.")

    try:
        # 2. Process Resume
        resume_text = parse_resume(contents, resume_file.filename)
        
        analysis_result = analyze_resume_with_ai(
            text=resume_text, 
            target_role=target_role, 
            job_description=job_description, 
            experience_level=experience_level
        )

        # 3. Store Result (Text Only - Efficient Storage)
        db_analysis = models.ResumeAnalysis(
            user_id=current_user.id,
            original_text=resume_text,
            analysis_json=json.loads(json.dumps(analysis_result)), # Ensure it's JSON serialization compatible
        )
        db.add(db_analysis)
        db.commit()
        
        return analysis_result
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Resume Optimization API is running"}
