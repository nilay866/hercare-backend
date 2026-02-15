from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
import bcrypt
import sys
import uuid

print("Script starting...")

def get_password_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def register_user(name, email, password, role):
    db = SessionLocal()
    try:
        # Check if user exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"Error: User with email '{email}' already exists.")
            return

        # Create new user
        hashed_password = get_password_hash(password)
        new_user = User(
            id=uuid.uuid4(),
            name=name,
            email=email,
            password_hash=hashed_password,
            role=role,
            age=30 # Default age
        )
        db.add(new_user)
        db.commit()
        print(f"Successfully registered {role.capitalize()}: {name} ({email})")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python register_user.py <name> <email> <password> <role>")
        print("Example: python register_user.py 'Dr. Smith' 'dr.smith@gmail.com' 'pass123' 'doctor'")
    else:
        register_user(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
