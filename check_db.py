from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
import sys

print("Script starting...")

def get_users():
    print("Connecting to DB...")
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"\nTotal Users: {len(users)}")
        print("-" * 50)
        print(f"{'Name':<20} | {'Email':<30} | {'Role':<10} | {'Logs':<5}")
        print("-" * 75)
        for user in users:
            name = user.name or "N/A"
            email = user.email or "N/A"
            role = user.role or "N/A"
            log_count = len(user.health_logs)
            print(f"{name:<20} | {email:<30} | {role:<10} | {log_count:<5}")
        print("-" * 75)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    get_users()
