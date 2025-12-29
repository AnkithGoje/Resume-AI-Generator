import sys
import os

# Add server directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app, get_db
from models import Base, ResumeAnalysis
import auth
import pytest
import uuid

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

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_full_system_flow():
    print("\n--- Starting Comprehensive System Test (TestClient) ---\n")
    
    # 1. Signup
    print("1. Testing User Registration...")
    unique_email = f"test_{uuid.uuid4()}@example.com"
    password = "testpassword123"
    
    response = client.post("/api/auth/signup", json={"email": unique_email, "password": password})
    if response.status_code == 200:
        print("   SUCCESS: Signup successful")
    else:
        print(f"   FAILURE: {response.text}")
        return

    # 2. Login
    print("\n2. Testing User Login...")
    response = client.post("/api/auth/token", data={"username": unique_email, "password": password})
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"   SUCCESS: Login successful. Token received.")
    else:
        print(f"   FAILURE: Login failed. {response.text}")
        return

    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Get User Me
    print("\n3. Testing Protected Endpoint (/users/me)...")
    response = client.get("/api/users/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print(f"   SUCCESS: User data retrieved. usage_count: {user_data['usage_count']}")
    else:
        print(f"   FAILURE: {response.text}")
        return

    # 4. Test Usage Limit (Boundary Condition)
    print("\n4. Testing Usage Limit Enforcement (50 limit)...")
    
    # Inject 50 analyses into the IN-MEMORY database
    db = TestingSessionLocal()
    user_id = user_data["id"]
    
    print(f"   ...Injecting 50 dummy analysis records for user_id {user_id}...")
    try:
        for i in range(50):
            dummy_analysis = ResumeAnalysis(
                user_id=user_id,
                original_text=f"Dummy resume text {i}",
                analysis_json={"score": 0, "status": "dummy"}
            )
            db.add(dummy_analysis)
        db.commit()
        print("   ...Injection complete.")
        
        # Now try to hit the analyze endpoint
        print("   ...Attempting analysis request (Should Fail with 403)...")
        
        # Create a dummy PDF file in memory
        files = {'resume_file': ('test.pdf', b'%PDF-1.4 empty pdf', 'application/pdf')}
        data = {
            'target_role': 'Software Engineer',
            'job_description': 'Test JD',
            'experience_level': 'Entry'
        }
        
        response = client.post("/api/analyze-resume", headers=headers, files=files, data=data)
        
        if response.status_code == 403:
            print("   SUCCESS: Request rejected with 403 Forbidden as expected.")
            print(f"   Message: {response.json().get('detail')}")
        else:
            print(f"   FAILURE: Expected 403, got {response.status_code}")
            print(f"   Response: {response.text}")

    except Exception as e:
        print(f"   ERROR during DB injection: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_full_system_flow()
