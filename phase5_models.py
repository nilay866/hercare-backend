"""
Phase 5: Analytics & Health Insights
Database models for health analytics, statistics, and AI insights
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class InsightType(str, enum.Enum):
    medication_reminder = "medication_reminder"
    health_alert = "health_alert"
    preventive_care = "preventive_care"
    appointment_reminder = "appointment_reminder"
    lab_follow_up = "lab_follow_up"
    wellness_tip = "wellness_tip"


class HealthMetric:
    """Daily/periodic health metrics tracked by user"""
    __tablename__ = "health_metrics"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    metric_type = Column(String(100), nullable=False)  # "blood_pressure", "weight", "glucose", etc.
    value = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)  # "mmHg", "kg", "mg/dL", etc.
    recorded_at = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    is_abnormal = Column(Boolean, default=False)
    alert_generated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_metrics")


class HealthInsight:
    """AI-generated health insights and recommendations"""
    __tablename__ = "health_insights"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    insight_type = Column(SQLEnum(InsightType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    data = Column(JSON, nullable=True)  # Additional data for insight
    is_read = Column(Boolean, default=False)
    action_taken = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="health_insights")


class HealthReport:
    """Generated health reports and summaries"""
    __tablename__ = "health_reports"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    report_type = Column(String(100), nullable=False)  # "monthly", "quarterly", "annual"
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    summary = Column(Text, nullable=True)
    key_findings = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    metrics_summary = Column(JSON, nullable=True)
    shared_with_doctor = Column(Boolean, default=False)
    shared_at = Column(DateTime, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_reports")


class DoctorAnalytics:
    """Analytics data for doctors"""
    __tablename__ = "doctor_analytics"

    id = Column(String(36), primary_key=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    appointments_count = Column(Integer, default=0)
    consultations_count = Column(Integer, default=0)
    prescriptions_issued = Column(Integer, default=0)
    patient_satisfaction = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("User", back_populates="analytics")


class PlatformAnalytics:
    """Overall platform analytics"""
    __tablename__ = "platform_analytics"

    id = Column(String(36), primary_key=True)
    date = Column(DateTime, nullable=False)
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_appointments = Column(Integer, default=0)
    total_consultations = Column(Integer, default=0)
    total_prescriptions = Column(Integer, default=0)
    platform_revenue = Column(Float, default=0.0)
    average_rating = Column(Float, default=0.0)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserPreference:
    """User preferences for notifications and insights"""
    __tablename__ = "user_preferences"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, unique=True)
    notify_health_alerts = Column(Boolean, default=True)
    notify_insights = Column(Boolean, default=True)
    notify_appointments = Column(Boolean, default=True)
    notify_prescriptions = Column(Boolean, default=True)
    daily_health_reminder = Column(Boolean, default=False)
    reminder_time = Column(String(5), default="08:00")  # "HH:MM"
    share_data_for_research = Column(Boolean, default=False)
    privacy_level = Column(String(50), default="private")  # private, doctors_only, full
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="preferences")
