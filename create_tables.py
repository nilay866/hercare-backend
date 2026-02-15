
from models import Base, User, HealthLog, PregnancyProfile, DoctorProfile, DoctorPatientLink, MedicalReport, Medication, DietPlan, EmergencyRequest, Consultation, MedicalHistory
from database import engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")
