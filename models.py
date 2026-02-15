from sqlalchemy import Column, String, Integer, Text, Date, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime, date, timedelta
from database import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    password_hash = Column(String, nullable=True)
    age = Column(Integer)
    role = Column(String)  # "patient" or "doctor"
    phone = Column(String, nullable=True)

    health_logs = relationship("HealthLog", back_populates="user")
    pregnancy_profile = relationship("PregnancyProfile", back_populates="user", uselist=False)

class PregnancyProfile(Base):
    __tablename__ = "pregnancy_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    last_period_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    pregnancy_type = Column(String, nullable=False, default="continue")  # "continue" or "abort"
    blood_group = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    existing_conditions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="pregnancy_profile")

class DoctorProfile(Base):
    __tablename__ = "doctor_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    specialization = Column(String, nullable=True)
    hospital = Column(String, nullable=True)
    experience_years = Column(Integer, nullable=True)
    available = Column(Boolean, default=True)
    invite_code = Column(String, unique=True, nullable=True)

    user = relationship("User")

class DoctorPatientLink(Base):
    __tablename__ = "doctor_patient_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    permissions = Column(JSON, nullable=True, default={})
    share_code = Column(String, unique=True, nullable=True) # For linking shadow records
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicalReport(Base):
    __tablename__ = "medical_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    report_type = Column(String, nullable=False)  # "blood_test", "ultrasound", "prescription", "other"
    notes = Column(Text, nullable=True)
    file_data = Column(Text, nullable=True)  # base64 encoded file
    file_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Medication(Base):
    __tablename__ = "medications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    prescribed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=True)  # "1x daily", "2x daily", "3x daily"
    times = Column(JSON, nullable=True)  # ["08:00", "14:00", "20:00"]
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    meal_type = Column(String, nullable=False)  # "breakfast", "lunch", "snack", "dinner"
    food_items = Column(Text, nullable=False)
    calories = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    day_of_week = Column(String, nullable=True)  # "monday", "tuesday", etc.
    created_at = Column(DateTime, default=datetime.utcnow)

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    status = Column(String, default="pending")  # "pending", "accepted", "resolved"
    accepted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    consultation_type = Column(String, nullable=True)  # "online", "visit"
    created_at = Column(DateTime, default=datetime.utcnow)

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    log_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    log_date = Column(Date, nullable=False, default=date.today, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    pain_level = Column(Integer, nullable=True)
    bleeding_level = Column(String, nullable=True)
    mood = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="health_logs")

class MedicalHistory(Base):
    __tablename__ = "medical_histories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    surgeries = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    consulting_summary = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    visit_date = Column(Date, nullable=False, default=date.today)
    symptoms = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True) 
    # Phase 5: Structured Rx & Billing
    prescriptions = Column(JSON, nullable=True) # [{"name": "Panadol", "dosage": "500mg", "timing": "Morning", "duration": "5 days"}]
    billing_items = Column(JSON, nullable=True) # [{"service": "Consultation", "cost": 50.0}]
    total_amount = Column(Float, default=0.0)
    payment_status = Column(String, default="pending") # pending, paid
    
    prescription_text = Column(Text, nullable=True) # Keep for backward compat
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ════════════════════════════════════
#     NEW RBAC & ADMIN MODELS
# ════════════════════════════════════

class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False, index=True)  # "super_admin", "hospital_admin", "doctor", "patient"
    description = Column(String, nullable=True)
    permissions = Column(JSON, nullable=False, default={})  # {"user.create": True, "user.delete": True}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False, index=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    role = relationship("Role")
    assigner = relationship("User", foreign_keys=[assigned_by])

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(String, default="hospital")  # "hospital", "clinic", "individual"
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String, nullable=False)  # "create", "update", "delete", "login", "access"
    resource_type = Column(String, nullable=False)  # "user", "patient", "prescription", etc.
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    status = Column(String, default="success")  # "success", "failed"
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    appointment_date = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, default=30)
    status = Column(String, default="scheduled")  # "scheduled", "completed", "cancelled", "no_show"
    appointment_type = Column(String, default="consultation")  # "consultation", "followup", "checkup"
    notes = Column(Text, nullable=True)
    cancellation_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # "pdf", "image", "document", etc.
    file_size = Column(Integer, nullable=False)
    s3_key = Column(String, nullable=True)  # Path in S3
    s3_url = Column(String, nullable=True)  # Public URL from S3
    resource_type = Column(String, nullable=False)  # "medical_report", "prescription", "profile_photo"
    resource_id = Column(UUID(as_uuid=True), nullable=True)  # FK to related resource
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    is_public = Column(Boolean, default=False)
    access_log = Column(JSON, nullable=True)  # Track who accessed this file
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=True)

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, default="info")  # "info", "warning", "error", "success"
    channel = Column(String, default="in_app")  # "in_app", "email", "sms", "push"
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    action_url = Column(String, nullable=True)
    extra_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

