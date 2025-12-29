from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import auth
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    db = SessionLocal()
    try:
        # Ensure tables exist
        models.Base.metadata.create_all(bind=engine)
        
        email = "admin@example.com"
        password = "password123"
        
        # Check if exists
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            logger.info(f"User {email} already exists. Deleting...")
            db.delete(existing_user)
            db.commit()
            
        logger.info(f"Creating test user: {email} / {password}")
        hashed_password = auth.get_password_hash(password)
        user = models.User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User created successfully. ID: {user.id}")
        
        # Verify immediately
        logger.info("Performing immediate verification...")
        if auth.verify_password(password, user.hashed_password):
            logger.info("SUCCESS: Password verified against DB record.")
        else:
            logger.error("FAILURE: Immediate verification failed.")
            
    except Exception as e:
        logger.error(f"Error creating test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
