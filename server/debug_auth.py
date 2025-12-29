from passlib.context import CryptContext
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_hashing():
    password = "testpassword123"
    try:
        logger.info(f"Hashing password: {password}")
        hashed = pwd_context.hash(password)
        logger.info(f"Hashed: {hashed}")
        
        logger.info("Verifying password...")
        is_valid = pwd_context.verify(password, hashed)
        logger.info(f"Verification result: {is_valid}")
        
        if is_valid:
            print("SUCCESS: Hashing and verification working correctly.")
        else:
            print("FAILURE: Verification returned False.")
            
    except Exception as e:
        logger.error("An error occurred during hashing/verification")
        print(f"ERROR: {e}")
        # Check if bcrypt is installed
        try:
            import bcrypt
            print("Target 'bcrypt' library is importable.")
        except ImportError:
            print("Target 'bcrypt' library is NOT importable.")

if __name__ == "__main__":
    test_hashing()
