from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, HealthLog
import sys

def get_logs(email):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User '{email}' not found.")
            return

        print(f"\nHealth Logs for {user.name} ({user.email})")
        print("=" * 60)
        
        logs = user.health_logs
        if not logs:
            print("No logs found.")
        else:
            for log in logs:
                print(f"Date: {log.log_date} | Type: {log.log_type}")
                print(f"Title: {log.title}")
                print(f"Mood: {log.mood} | Pain: {log.pain_level}")
                print(f"Bleeding: {log.bleeding_level}")
                if log.notes:
                    print(f"Notes: {log.notes}")
                if log.description:
                    print(f"Desc: {log.description}")
                print("-" * 60)
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = "nilay@gmail.com"
    get_logs(email)
