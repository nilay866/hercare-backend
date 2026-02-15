"""
Phase 3: Doctor Features & Prescription Management
Database models for doctor workflows, prescriptions, and health records
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Models extend the existing models.py - add these to the database

class PrescriptionStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
    expired = "expired"


class DoctorSpecialty(str, enum.Enum):
    general_practice = "general_practice"
    cardiology = "cardiology"
    dermatology = "dermatology"
    neurology = "neurology"
    orthopedics = "orthopedics"
    pediatrics = "pediatrics"
    gynecology = "gynecology"
    psychiatry = "psychiatry"
    oncology = "oncology"
    surgery = "surgery"


class DoctorSpecializationModel:
    """Doctor specializations and certifications"""
    __tablename__ = "doctor_specializations"

    id = Column(String(36), primary_key=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    specialty = Column(SQLEnum(DoctorSpecialty), nullable=False)
    license_number = Column(String(100), unique=True, nullable=False)
    issuing_country = Column(String(100), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    verified = Column(Boolean, default=False)
    verification_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("User", back_populates="specializations")
    prescriptions = relationship("Prescription", back_populates="prescribed_by_doctor")


class Prescription:
    """Patient prescriptions issued by doctors"""
    __tablename__ = "prescriptions"

    id = Column(String(36), primary_key=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    patient_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    medication_name = Column(String(255), nullable=False)
    dosage = Column(String(100), nullable=False)  # e.g., "500mg"
    frequency = Column(String(100), nullable=False)  # e.g., "3 times daily"
    duration_days = Column(Integer, nullable=False)
    instructions = Column(Text, nullable=True)
    status = Column(SQLEnum(PrescriptionStatus), default=PrescriptionStatus.active)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    refills_allowed = Column(Integer, default=0)
    refills_used = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])


class HealthRecord:
    """Patient health records and medical history"""
    __tablename__ = "health_records"

    id = Column(String(36), primary_key=True)
    patient_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    record_type = Column(String(100), nullable=False)  # e.g., "lab_result", "diagnosis", "imaging"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=True)
    recorded_date = Column(DateTime, nullable=False)
    file_url = Column(String(500), nullable=True)
    metadata = Column(JSON, nullable=True)
    visibility = Column(String(50), default="private")  # private, shared_with_providers, public
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])


class DoctorAvailability:
    """Doctor availability slots for appointments"""
    __tablename__ = "doctor_availability"

    id = Column(String(36), primary_key=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(String(5), nullable=False)  # "09:00"
    end_time = Column(String(5), nullable=False)  # "17:00"
    slot_duration_minutes = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("User", back_populates="availability")


class DoctorRating:
    """Patient ratings and reviews for doctors"""
    __tablename__ = "doctor_ratings"

    id = Column(String(36), primary_key=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    patient_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    appointment_id = Column(String(36), ForeignKey("appointments"), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text, nullable=True)
    anonymous = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
