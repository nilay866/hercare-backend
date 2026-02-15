"""
Phase 3: Doctor API Routes
Routes for prescription management, health records, and doctor workflows
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from auth import get_current_user, require_role, require_permission
from audit import AuditService
from database import get_db

router = APIRouter(tags=["doctor"])
audit_service = AuditService()


# ==================== Schemas ====================

class SpecialtyDTO(BaseModel):
    specialty: str
    license_number: str
    issuing_country: str
    issue_date: datetime
    expiry_date: Optional[datetime] = None


class PrescriptionCreateDTO(BaseModel):
    patient_id: str
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int
    instructions: Optional[str] = None
    refills_allowed: int = 0
    notes: Optional[str] = None


class PrescriptionUpdateDTO(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class HealthRecordDTO(BaseModel):
    record_type: str
    title: str
    description: Optional[str] = None
    recorded_date: datetime
    file_url: Optional[str] = None
    metadata: Optional[dict] = None


class DoctorAvailabilityDTO(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    slot_duration_minutes: int = 30


class DoctorRatingDTO(BaseModel):
    rating: int
    review_text: Optional[str] = None
    anonymous: bool = False


# ==================== Doctor Profile Routes ====================

@router.get("/profile")
@require_role("doctor")
async def get_doctor_profile(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get doctor profile with specializations and ratings"""
    # Return doctor info with specializations and average rating
    return {
        "doctor_id": current_user.id,
        "name": current_user.full_name if hasattr(current_user, "full_name") else current_user.name,
        "email": current_user.email,
        "phone": current_user.phone if hasattr(current_user, "phone") else None,
        "hospital_id": current_user.hospital_id if hasattr(current_user, "hospital_id") else None,
        "specializations": [],  # Query from DB
        "average_rating": 4.5,
        "total_ratings": 42,
        "total_patients": 150,
        "years_experience": 10,
    }


@router.post("/specializations")
@require_role("doctor")
async def add_specialization(
    specialty: SpecialtyDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add doctor specialization and license"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="doctor_specialization_added",
        resource="doctor_specialization",
        status="success"
    )
    return {
        "specialty_id": str(uuid.uuid4()),
        "specialty": specialty.specialty,
        "verified": False,
        "message": "Specialization added. Pending admin verification."
    }


@router.get("/specializations")
@require_role("doctor")
async def get_specializations(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all doctor specializations"""
    return {
        "specializations": [
            {
                "specialty": "Cardiology",
                "license_number": "MD-12345",
                "verified": True,
                "issue_date": "2015-01-01",
                "expiry_date": "2025-01-01"
            }
        ]
    }


# ==================== Prescription Management ====================

@router.post("/prescriptions")
@require_role("doctor")
@require_permission("issue_prescription")
async def create_prescription(
    prescription: PrescriptionCreateDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Issue prescription to patient"""
    prescription_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="prescription_issued",
        resource=f"prescription:{prescription_id}",
        status="success"
    )
    
    return {
        "prescription_id": prescription_id,
        "patient_id": prescription.patient_id,
        "medication_name": prescription.medication_name,
        "dosage": prescription.dosage,
        "frequency": prescription.frequency,
        "duration_days": prescription.duration_days,
        "status": "active",
        "start_date": datetime.utcnow().isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=prescription.duration_days)).isoformat(),
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/prescriptions")
@require_role("doctor")
async def get_my_prescriptions(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all prescriptions issued by doctor"""
    return {
        "total": 45,
        "prescriptions": [
            {
                "prescription_id": str(uuid.uuid4()),
                "patient_id": "pat-123",
                "patient_name": "John Doe",
                "medication_name": "Aspirin",
                "dosage": "500mg",
                "frequency": "Twice daily",
                "status": "active",
                "start_date": "2024-01-15",
                "end_date": "2024-02-15"
            }
        ]
    }


@router.get("/prescriptions/{prescription_id}")
@require_role("doctor")
async def get_prescription(
    prescription_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prescription details"""
    return {
        "prescription_id": prescription_id,
        "patient_id": "pat-123",
        "patient_name": "John Doe",
        "medication_name": "Aspirin",
        "dosage": "500mg",
        "frequency": "Twice daily",
        "duration_days": 30,
        "instructions": "Take with food",
        "status": "active",
        "refills_allowed": 3,
        "refills_used": 1,
        "notes": "Monitor for side effects",
        "start_date": "2024-01-15",
        "end_date": "2024-02-15",
        "created_at": "2024-01-15T10:00:00Z"
    }


@router.put("/prescriptions/{prescription_id}")
@require_role("doctor")
@require_permission("modify_prescription")
async def update_prescription(
    prescription_id: str,
    prescription_update: PrescriptionUpdateDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update prescription status or notes"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="prescription_updated",
        resource=f"prescription:{prescription_id}",
        status="success"
    )
    
    return {
        "prescription_id": prescription_id,
        "status": prescription_update.status or "active",
        "updated_at": datetime.utcnow().isoformat()
    }


@router.post("/prescriptions/{prescription_id}/refill")
@require_role("doctor")
async def approve_refill(
    prescription_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve prescription refill"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="prescription_refill_approved",
        resource=f"prescription:{prescription_id}",
        status="success"
    )
    
    return {
        "prescription_id": prescription_id,
        "refills_used": 2,
        "refills_remaining": 1,
        "message": "Refill approved"
    }


# ==================== Health Records ====================

@router.post("/health-records")
@require_role("doctor")
@require_permission("create_health_record")
async def create_health_record(
    patient_id: str,
    record: HealthRecordDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create health record for patient"""
    record_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="health_record_created",
        resource=f"health_record:{record_id}",
        status="success"
    )
    
    return {
        "record_id": record_id,
        "patient_id": patient_id,
        "record_type": record.record_type,
        "title": record.title,
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/patients/{patient_id}/health-records")
@require_role("doctor")
async def get_patient_health_records(
    patient_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all health records for a patient"""
    return {
        "patient_id": patient_id,
        "total": 12,
        "records": [
            {
                "record_id": str(uuid.uuid4()),
                "record_type": "lab_result",
                "title": "Blood Test Results",
                "recorded_date": "2024-01-10",
                "created_by": "Dr. Smith"
            }
        ]
    }


# ==================== Doctor Availability ====================

@router.post("/availability")
@require_role("doctor")
async def set_availability(
    availability: DoctorAvailabilityDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set doctor availability slots"""
    availability_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="availability_set",
        resource=f"availability:{availability_id}",
        status="success"
    )
    
    return {
        "availability_id": availability_id,
        "day_of_week": availability.day_of_week,
        "start_time": availability.start_time,
        "end_time": availability.end_time,
        "slot_duration_minutes": availability.slot_duration_minutes
    }


@router.get("/availability")
@require_role("doctor")
async def get_availability(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get doctor availability schedule"""
    return {
        "doctor_id": current_user.id,
        "availability": [
            {
                "day": "Monday",
                "start_time": "09:00",
                "end_time": "17:00",
                "slot_duration_minutes": 30
            },
            {
                "day": "Wednesday",
                "start_time": "14:00",
                "end_time": "18:00",
                "slot_duration_minutes": 30
            }
        ]
    }


# ==================== Doctor Dashboard ====================

@router.get("/dashboard")
@require_role("doctor")
async def get_doctor_dashboard(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get doctor dashboard with key metrics"""
    return {
        "today": {
            "appointments_count": 8,
            "prescriptions_issued": 5,
            "new_patients": 2
        },
        "this_week": {
            "appointments_count": 35,
            "prescriptions_issued": 18,
            "new_patients": 7
        },
        "this_month": {
            "appointments_count": 120,
            "prescriptions_issued": 65,
            "new_patients": 25
        },
        "statistics": {
            "total_patients": 350,
            "average_rating": 4.7,
            "total_reviews": 145,
            "appointment_completion_rate": 92.5
        },
        "pending_tasks": {
            "prescription_refills": 3,
            "appointment_requests": 5,
            "health_record_reviews": 2
        }
    }


# ==================== Doctor Ratings ====================

@router.get("/ratings")
@require_role("doctor")
async def get_ratings(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all ratings and reviews"""
    return {
        "average_rating": 4.7,
        "total_ratings": 145,
        "rating_distribution": {
            "5_stars": 95,
            "4_stars": 35,
            "3_stars": 10,
            "2_stars": 4,
            "1_star": 1
        },
        "recent_reviews": [
            {
                "rating": 5,
                "review_text": "Excellent doctor, very professional",
                "patient_name": "Anonymous",
                "created_at": "2024-01-15"
            }
        ]
    }


@router.get("/appointments/pending")
@require_role("doctor")
async def get_pending_appointments(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending appointment requests"""
    return {
        "pending_count": 5,
        "appointments": [
            {
                "appointment_id": str(uuid.uuid4()),
                "patient_id": "pat-123",
                "patient_name": "John Doe",
                "appointment_type": "consultation",
                "requested_date": "2024-01-20T10:00:00Z",
                "reason": "Follow-up checkup",
                "status": "pending"
            }
        ]
    }


@router.post("/appointments/{appointment_id}/accept")
@require_role("doctor")
async def accept_appointment(
    appointment_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept pending appointment request"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="appointment_accepted",
        resource=f"appointment:{appointment_id}",
        status="success"
    )
    
    return {
        "appointment_id": appointment_id,
        "status": "confirmed",
        "message": "Appointment accepted"
    }


@router.post("/appointments/{appointment_id}/reject")
@require_role("doctor")
async def reject_appointment(
    appointment_id: str,
    reason: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject appointment request"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="appointment_rejected",
        resource=f"appointment:{appointment_id}",
        status="success"
    )
    
    return {
        "appointment_id": appointment_id,
        "status": "rejected",
        "reason": reason,
        "message": "Appointment rejected"
    }
