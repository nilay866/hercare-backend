"""
Phase 4: Telemedicine & Real-time Messaging
Database models for video consultations and patient-provider messaging
"""

from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


class ConsultationType(str, enum.Enum):
    video = "video"
    audio = "audio"
    text = "text"


class MessageType(str, enum.Enum):
    text = "text"
    image = "image"
    file = "file"
    prescription = "prescription"


class VideoConsultation:
    """Video/audio consultation sessions between doctor and patient"""
    __tablename__ = "video_consultations"

    id = Column(String(36), primary_key=True)
    appointment_id = Column(String(36), ForeignKey("appointments"), nullable=True)
    doctor_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    patient_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    consultation_type = Column(SQLEnum(ConsultationType), default=ConsultationType.video)
    status = Column(String(50), default="scheduled")  # scheduled, ongoing, completed, cancelled
    scheduled_start = Column(DateTime, nullable=False)
    actual_start = Column(DateTime, nullable=True)
    actual_end = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    meeting_url = Column(String(500), nullable=True)
    meeting_token = Column(String(500), nullable=True)
    recording_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    doctor = relationship("User", foreign_keys=[doctor_id])
    patient = relationship("User", foreign_keys=[patient_id])
    messages = relationship("Message", back_populates="consultation")


class Message:
    """Messages between doctor and patient during consultations"""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True)
    consultation_id = Column(String(36), ForeignKey("video_consultations"), nullable=False)
    sender_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    receiver_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    message_type = Column(SQLEnum(MessageType), default=MessageType.text)
    content = Column(Text, nullable=True)
    file_url = Column(String(500), nullable=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    consultation = relationship("VideoConsultation", back_populates="messages")


class DirectMessage:
    """Direct messages between users outside of consultations"""
    __tablename__ = "direct_messages"

    id = Column(String(36), primary_key=True)
    sender_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    receiver_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    content = Column(Text, nullable=True)
    message_type = Column(SQLEnum(MessageType), default=MessageType.text)
    file_url = Column(String(500), nullable=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])


class Conversation:
    """Tracks conversation between two users"""
    __tablename__ = "conversations"

    id = Column(String(36), primary_key=True)
    user1_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    user2_id = Column(String(36), ForeignKey("user.id"), nullable=False)
    last_message_id = Column(String(36), nullable=True)
    last_message_at = Column(DateTime, nullable=True)
    user1_unread_count = Column(Integer, default=0)
    user2_unread_count = Column(Integer, default=0)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
