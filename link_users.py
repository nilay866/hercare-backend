from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, DoctorPatientLink
import sys

def link_users(doctor_email, patient_email):
    db = SessionLocal()
    try:
        doctor = db.query(User).filter(User.email == doctor_email).first()
        patient = db.query(User).filter(User.email == patient_email).first()

        if not doctor:
            print(f"Error: Doctor with email '{doctor_email}' not found.")
            return
        if not patient:
            print(f"Error: Patient with email '{patient_email}' not found.")
            return

        # Check roles (optional but good practice)
        if doctor.role != 'doctor':
            print(f"Warning: User '{doctor_email}' has role '{doctor.role}', not 'doctor'. Proceeding anyway...")
        
        # Check if link already exists
        existing = db.query(DoctorPatientLink).filter(
            DoctorPatientLink.doctor_id == doctor.id,
            DoctorPatientLink.patient_id == patient.id
        ).first()

        if existing:
            print(f"Link already exists between {doctor.name} and {patient.name}.")
            return

        # Create link
        new_link = DoctorPatientLink(doctor_id=doctor.id, patient_id=patient.id)
        db.add(new_link)
        db.commit()
        print(f"Successfully linked Doctor '{doctor.name}' ({doctor_email}) with Patient '{patient.name}' ({patient_email}).")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python link_users.py <doctor_email> <patient_email>")
    else:
        link_users(sys.argv[1], sys.argv[2])
