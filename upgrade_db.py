from database import engine
from sqlalchemy import text
from models import Base

def upgrade():
    print("Starting database upgrade...")
    with engine.connect() as conn:
        # Add permissions column if not exists
        try:
            conn.execute(text("ALTER TABLE doctor_patient_links ADD COLUMN permissions JSON DEFAULT '{}'"))
            conn.commit()
            print("Added permissions column to doctor_patient_links.")
        except Exception as e:
            print(f"Skipping permissions column add: {e}")

        # Add treatment_plan column if not exists (Phase 4)
        try:
            conn.execute(text("ALTER TABLE consultations ADD COLUMN treatment_plan TEXT"))
            conn.commit()
            print("Added treatment_plan column to consultations.")
        except Exception as e:
            print(f"Skipping treatment_plan column add: {e}")

        # Add Phase 5 columns
        try:
            conn.execute(text("ALTER TABLE consultations ADD COLUMN prescriptions JSON DEFAULT '[]'"))
            conn.execute(text("ALTER TABLE consultations ADD COLUMN billing_items JSON DEFAULT '[]'"))
            conn.execute(text("ALTER TABLE consultations ADD COLUMN total_amount FLOAT DEFAULT 0.0"))
            conn.execute(text("ALTER TABLE consultations ADD COLUMN payment_status VARCHAR DEFAULT 'paid'"))
            conn.commit()
            print("Added Phase 5 columns to consultations.")
        except Exception as e:
            print(f"Skipping Phase 5 columns add: {e}")

        # Add Phase 10: Share Code
        try:
            conn.execute(text("ALTER TABLE doctor_patient_links ADD COLUMN share_code VARCHAR UNIQUE"))
            conn.commit()
            print("Added share_code to doctor_patient_links.")
        except Exception as e:
            print(f"Skipping share_code column add: {e}")
    
    # Create new tables
    print("Creating new tables if they don't exist...")
    Base.metadata.create_all(bind=engine)
    print("Database upgrade complete.")

if __name__ == "__main__":
    upgrade()
