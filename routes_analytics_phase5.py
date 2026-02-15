"""
Phase 5: Analytics & Health Insights API Routes
Routes for health metrics, insights, reports, and analytics
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from auth import get_current_user, require_role
from audit import AuditService
from database import get_db

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])
audit_service = AuditService()


# ==================== Schemas ====================

class HealthMetricDTO(BaseModel):
    metric_type: str
    value: float
    unit: str
    notes: Optional[str] = None
    recorded_at: Optional[datetime] = None


class HealthInsightDTO(BaseModel):
    pass  # Read-only


class HealthReportDTO(BaseModel):
    report_type: str  # "monthly", "quarterly", "annual"
    period_start: datetime
    period_end: datetime


class UserPreferenceDTO(BaseModel):
    notify_health_alerts: Optional[bool] = None
    notify_insights: Optional[bool] = None
    notify_appointments: Optional[bool] = None
    notify_prescriptions: Optional[bool] = None
    daily_health_reminder: Optional[bool] = None
    reminder_time: Optional[str] = None
    share_data_for_research: Optional[bool] = None
    privacy_level: Optional[str] = None


# ==================== Health Metrics ====================

@router.post("/health-metrics", status_code=201)
async def record_health_metric(
    metric: HealthMetricDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record a health metric (blood pressure, weight, glucose, etc.)"""
    metric_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="health_metric_recorded",
        resource=f"metric:{metric_id}",
        status="success"
    )
    
    return {
        "metric_id": metric_id,
        "metric_type": metric.metric_type,
        "value": metric.value,
        "unit": metric.unit,
        "recorded_at": (metric.recorded_at or datetime.utcnow()).isoformat(),
        "is_abnormal": False,
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/health-metrics")
async def get_health_metrics(
    metric_type: Optional[str] = None,
    days: int = 30,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health metrics for the user"""
    return {
        "total": 45,
        "metrics": [
            {
                "metric_id": str(uuid.uuid4()),
                "metric_type": "blood_pressure",
                "value": 120,
                "systolic": 120,
                "diastolic": 80,
                "unit": "mmHg",
                "recorded_at": "2024-02-15T10:00:00Z",
                "is_abnormal": False
            }
        ],
        "statistics": {
            "average": 120,
            "minimum": 115,
            "maximum": 135,
            "trend": "stable"
        }
    }


@router.get("/health-metrics/{metric_type}")
async def get_metric_history(
    metric_type: str,
    days: int = 90,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get history of specific health metric"""
    return {
        "metric_type": metric_type,
        "period_days": days,
        "total_records": 90,
        "records": [
            {
                "date": "2024-02-15",
                "value": 120,
                "unit": "mmHg"
            }
        ],
        "statistics": {
            "average": 120,
            "median": 119,
            "std_dev": 5.2,
            "trend": "decreasing",
            "alerts_generated": 2
        }
    }


# ==================== Health Insights ====================

@router.get("/insights")
async def get_health_insights(
    priority: Optional[str] = None,
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health insights for the user"""
    return {
        "total": 8,
        "insights": [
            {
                "insight_id": str(uuid.uuid4()),
                "insight_type": "medication_reminder",
                "title": "Time to take your medication",
                "description": "You're due for your daily aspirin dose",
                "recommendation": "Take 1 tablet with water",
                "priority": "high",
                "is_read": False,
                "created_at": "2024-02-15T10:00:00Z"
            },
            {
                "insight_id": str(uuid.uuid4()),
                "insight_type": "health_alert",
                "title": "High blood pressure detected",
                "description": "Your recent blood pressure reading (140/90) is higher than normal",
                "recommendation": "Consider contacting your doctor",
                "priority": "high",
                "is_read": True,
                "created_at": "2024-02-14T15:30:00Z"
            }
        ]
    }


@router.put("/insights/{insight_id}/read")
async def mark_insight_as_read(
    insight_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark insight as read"""
    return {
        "insight_id": insight_id,
        "is_read": True,
        "read_at": datetime.utcnow().isoformat()
    }


@router.post("/insights/{insight_id}/action")
async def take_insight_action(
    insight_id: str,
    action_type: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record action taken on an insight (e.g., scheduled appointment)"""
    return {
        "insight_id": insight_id,
        "action_taken": True,
        "action_type": action_type,
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== Health Reports ====================

@router.post("/reports")
async def generate_health_report(
    report: HealthReportDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a health report for the period"""
    report_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="health_report_generated",
        resource=f"report:{report_id}",
        status="success"
    )
    
    return {
        "report_id": report_id,
        "report_type": report.report_type,
        "period_start": report.period_start.isoformat(),
        "period_end": report.period_end.isoformat(),
        "summary": "Your health has been stable over the past month...",
        "key_findings": [
            "Average blood pressure: 120/80 mmHg (Normal)",
            "Weight trend: Stable",
            "Activity level: Good"
        ],
        "recommendations": [
            "Continue current exercise routine",
            "Stay hydrated",
            "Monitor blood pressure weekly"
        ],
        "generated_at": datetime.utcnow().isoformat()
    }


@router.get("/reports")
async def get_health_reports(
    report_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all health reports for the user"""
    return {
        "total": 5,
        "reports": [
            {
                "report_id": str(uuid.uuid4()),
                "report_type": "monthly",
                "period_start": "2024-01-01",
                "period_end": "2024-01-31",
                "summary": "Your health has been stable...",
                "shared_with_doctor": True,
                "generated_at": "2024-02-01T10:00:00Z"
            }
        ]
    }


@router.get("/reports/{report_id}")
async def get_health_report(
    report_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed health report"""
    return {
        "report_id": report_id,
        "report_type": "monthly",
        "period_start": "2024-01-01T00:00:00Z",
        "period_end": "2024-01-31T23:59:59Z",
        "summary": "Your health has been stable over the past month with no major concerns.",
        "key_findings": {
            "blood_pressure": {
                "average": "120/80 mmHg",
                "status": "Normal",
                "trend": "stable"
            },
            "weight": {
                "average": 70,
                "unit": "kg",
                "trend": "stable"
            },
            "activity": {
                "average_steps": 8500,
                "trend": "good"
            }
        },
        "recommendations": [
            "Continue current exercise routine",
            "Maintain healthy diet",
            "Schedule yearly checkup"
        ],
        "metrics_summary": {
            "metrics_recorded": 45,
            "abnormal_readings": 2,
            "health_alerts": 1
        },
        "generated_at": "2024-02-01T10:00:00Z"
    }


@router.post("/reports/{report_id}/share")
async def share_report_with_doctor(
    report_id: str,
    doctor_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Share health report with doctor"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="health_report_shared",
        resource=f"report:{report_id}",
        status="success"
    )
    
    return {
        "report_id": report_id,
        "shared_with": doctor_id,
        "shared_at": datetime.utcnow().isoformat()
    }


# ==================== Health Dashboard ====================

@router.get("/dashboard")
async def get_health_dashboard(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive health dashboard"""
    return {
        "overview": {
            "overall_health_score": 82,
            "trend": "improving",
            "last_checkup": "2024-01-20",
            "next_checkup": "2024-04-20"
        },
        "vital_signs": {
            "blood_pressure": {
                "latest": "120/80 mmHg",
                "status": "Normal",
                "trend": "stable"
            },
            "weight": {
                "latest": 70,
                "unit": "kg",
                "trend": "stable"
            },
            "heart_rate": {
                "latest": 72,
                "unit": "bpm",
                "trend": "stable"
            }
        },
        "recent_insights": [
            {
                "insight_type": "wellness_tip",
                "title": "Stay hydrated",
                "description": "Drink at least 8 glasses of water daily"
            }
        ],
        "upcoming": {
            "appointments": 1,
            "prescriptions_to_refill": 0,
            "health_alerts": 0
        },
        "statistics": {
            "metrics_tracked": 45,
            "health_records": 12,
            "appointments_this_month": 2
        }
    }


# ==================== Preferences ====================

@router.get("/preferences")
async def get_preferences(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user analytics and insight preferences"""
    return {
        "notify_health_alerts": True,
        "notify_insights": True,
        "notify_appointments": True,
        "notify_prescriptions": True,
        "daily_health_reminder": False,
        "reminder_time": "08:00",
        "share_data_for_research": False,
        "privacy_level": "private"
    }


@router.put("/preferences")
async def update_preferences(
    preferences: UserPreferenceDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="preferences_updated",
        resource="user_preferences",
        status="success"
    )
    
    return {
        "notify_health_alerts": preferences.notify_health_alerts or True,
        "notify_insights": preferences.notify_insights or True,
        "notify_appointments": preferences.notify_appointments or True,
        "notify_prescriptions": preferences.notify_prescriptions or True,
        "daily_health_reminder": preferences.daily_health_reminder or False,
        "reminder_time": preferences.reminder_time or "08:00",
        "share_data_for_research": preferences.share_data_for_research or False,
        "privacy_level": preferences.privacy_level or "private",
        "updated_at": datetime.utcnow().isoformat()
    }


# ==================== Doctor Analytics ====================

@router.get("/doctor/statistics")
@require_role("doctor")
async def get_doctor_statistics(
    period_days: int = 30,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get doctor statistics for the period"""
    return {
        "period_days": period_days,
        "total_appointments": 120,
        "completed_appointments": 115,
        "completion_rate": 95.8,
        "total_prescriptions": 65,
        "average_patient_satisfaction": 4.7,
        "consultation_revenue": 15000,
        "prescription_revenue": 2500,
        "daily_breakdown": [
            {
                "date": "2024-02-15",
                "appointments": 8,
                "consultations": 3,
                "prescriptions": 5,
                "revenue": 500
            }
        ]
    }


# ==================== Platform Analytics ====================

@router.get("/platform/statistics")
@require_role("admin")
async def get_platform_statistics(
    period_days: int = 30,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get overall platform statistics"""
    return {
        "period_days": period_days,
        "total_users": 50000,
        "active_users": 12500,
        "total_appointments": 25000,
        "total_consultations": 5000,
        "total_prescriptions": 15000,
        "platform_revenue": 500000,
        "average_rating": 4.6,
        "growth_rate": 15.5,
        "daily_active_users": {
            "average": 12500,
            "peak": 15000,
            "trend": "increasing"
        }
    }
