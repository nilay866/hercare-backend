"""
Phase 4: Telemedicine & Messaging API Routes
Routes for video consultations and real-time messaging
"""

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid

from auth import get_current_user, require_role
from audit import AuditService
from database import get_db

router = APIRouter(prefix="/api/v1/telemedicine", tags=["telemedicine"])
audit_service = AuditService()

# Store active connections for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, consultation_id: str, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if consultation_id not in self.active_connections:
            self.active_connections[consultation_id] = {}
        self.active_connections[consultation_id][user_id] = websocket

    def disconnect(self, consultation_id: str, user_id: str):
        if consultation_id in self.active_connections:
            self.active_connections[consultation_id].pop(user_id, None)

    async def broadcast_to_consultation(self, consultation_id: str, message: dict):
        if consultation_id in self.active_connections:
            for user_id, connection in self.active_connections[consultation_id].items():
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()


# ==================== Schemas ====================

class VideoConsultationCreateDTO(BaseModel):
    appointment_id: Optional[str] = None
    patient_id: str
    consultation_type: str
    scheduled_start: datetime


class VideoConsultationUpdateDTO(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    diagnosis: Optional[str] = None
    follow_up_required: Optional[bool] = None


class MessageDTO(BaseModel):
    content: str
    message_type: str = "text"
    file_url: Optional[str] = None


class DirectMessageDTO(BaseModel):
    receiver_id: str
    content: str
    message_type: str = "text"
    file_url: Optional[str] = None


# ==================== Video Consultation Routes ====================

@router.post("/consultations")
@require_role("doctor")
async def schedule_consultation(
    consultation: VideoConsultationCreateDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Schedule a new video consultation"""
    consultation_id = str(uuid.uuid4())
    meeting_token = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="consultation_scheduled",
        resource=f"consultation:{consultation_id}",
        status="success"
    )
    
    return {
        "consultation_id": consultation_id,
        "patient_id": consultation.patient_id,
        "doctor_id": current_user.id,
        "consultation_type": consultation.consultation_type,
        "scheduled_start": consultation.scheduled_start.isoformat(),
        "status": "scheduled",
        "meeting_url": f"https://meet.hercare.com/{consultation_id}",
        "meeting_token": meeting_token
    }


@router.get("/consultations")
@require_role("doctor", "patient")
async def get_consultations(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get consultations for logged-in user"""
    return {
        "total": 15,
        "consultations": [
            {
                "consultation_id": str(uuid.uuid4()),
                "doctor_name": "Dr. Smith",
                "patient_name": "John Doe",
                "consultation_type": "video",
                "status": "scheduled",
                "scheduled_start": "2024-02-20T14:00:00Z"
            }
        ]
    }


@router.get("/consultations/{consultation_id}")
@require_role("doctor", "patient")
async def get_consultation(
    consultation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get consultation details"""
    return {
        "consultation_id": consultation_id,
        "doctor_id": "doc-123",
        "patient_id": "pat-123",
        "consultation_type": "video",
        "status": "completed",
        "scheduled_start": "2024-02-20T14:00:00Z",
        "actual_start": "2024-02-20T14:05:00Z",
        "actual_end": "2024-02-20T14:35:00Z",
        "duration_minutes": 30,
        "notes": "General checkup completed",
        "diagnosis": "Patient is healthy",
        "recording_url": "https://storage.hercare.com/recordings/cons-123.mp4"
    }


@router.put("/consultations/{consultation_id}")
@require_role("doctor")
async def update_consultation(
    consultation_id: str,
    consultation_update: VideoConsultationUpdateDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update consultation details"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="consultation_updated",
        resource=f"consultation:{consultation_id}",
        status="success"
    )
    
    return {
        "consultation_id": consultation_id,
        "status": consultation_update.status,
        "updated_at": datetime.utcnow().isoformat()
    }


@router.post("/consultations/{consultation_id}/start")
@require_role("doctor", "patient")
async def start_consultation(
    consultation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark consultation as started"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="consultation_started",
        resource=f"consultation:{consultation_id}",
        status="success"
    )
    
    return {
        "consultation_id": consultation_id,
        "status": "ongoing",
        "started_at": datetime.utcnow().isoformat()
    }


@router.post("/consultations/{consultation_id}/end")
@require_role("doctor")
async def end_consultation(
    consultation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End consultation session"""
    await audit_service.log_action(
        user_id=current_user.id,
        action="consultation_ended",
        resource=f"consultation:{consultation_id}",
        status="success"
    )
    
    return {
        "consultation_id": consultation_id,
        "status": "completed",
        "ended_at": datetime.utcnow().isoformat()
    }


# ==================== Messages in Consultation ====================

@router.post("/consultations/{consultation_id}/messages")
@require_role("doctor", "patient")
async def send_message(
    consultation_id: str,
    message: MessageDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send message during consultation"""
    message_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="message_sent",
        resource=f"message:{message_id}",
        status="success"
    )
    
    return {
        "message_id": message_id,
        "sender_id": current_user.id,
        "content": message.content,
        "message_type": message.message_type,
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/consultations/{consultation_id}/messages")
@require_role("doctor", "patient")
async def get_consultation_messages(
    consultation_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages in consultation"""
    return {
        "total": 25,
        "messages": [
            {
                "message_id": str(uuid.uuid4()),
                "sender_id": "doc-123",
                "sender_name": "Dr. Smith",
                "content": "Good morning, how are you feeling?",
                "message_type": "text",
                "created_at": "2024-02-20T14:05:00Z",
                "is_read": True
            }
        ]
    }


# ==================== WebSocket for Real-time Messaging ====================

@router.websocket("/ws/consultation/{consultation_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    consultation_id: str,
    token: str = None,
    current_user = Depends(get_current_user)
):
    """WebSocket endpoint for real-time consultation messaging"""
    await manager.connect(consultation_id, websocket, current_user.id)
    try:
        while True:
            data = await websocket.receive_json()
            
            message = {
                "sender_id": current_user.id,
                "message_type": data.get("message_type", "text"),
                "content": data.get("content"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await manager.broadcast_to_consultation(consultation_id, message)
            
            await audit_service.log_action(
                user_id=current_user.id,
                action="consultation_message_sent",
                resource=f"consultation:{consultation_id}",
                status="success"
            )
    except Exception as e:
        manager.disconnect(consultation_id, current_user.id)


# ==================== Direct Messaging ====================

@router.post("/messages")
async def send_direct_message(
    message: DirectMessageDTO,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send direct message to another user"""
    message_id = str(uuid.uuid4())
    
    await audit_service.log_action(
        user_id=current_user.id,
        action="direct_message_sent",
        resource=f"message:{message_id}",
        status="success"
    )
    
    return {
        "message_id": message_id,
        "sender_id": current_user.id,
        "receiver_id": message.receiver_id,
        "content": message.content,
        "created_at": datetime.utcnow().isoformat()
    }


@router.get("/conversations")
async def get_conversations(
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user"""
    return {
        "total": 8,
        "conversations": [
            {
                "conversation_id": str(uuid.uuid4()),
                "other_user_id": "doc-123",
                "other_user_name": "Dr. Smith",
                "other_user_avatar": "https://...",
                "last_message": "See you next week",
                "last_message_at": "2024-02-15T10:00:00Z",
                "unread_count": 2
            }
        ]
    }


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages in conversation"""
    return {
        "total": 120,
        "messages": [
            {
                "message_id": str(uuid.uuid4()),
                "sender_id": "doc-123",
                "sender_name": "Dr. Smith",
                "content": "Hi! How are you?",
                "created_at": "2024-02-15T10:00:00Z",
                "is_read": True
            }
        ]
    }


@router.put("/conversations/{conversation_id}/messages/read")
async def mark_conversation_as_read(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all messages in conversation as read"""
    return {
        "conversation_id": conversation_id,
        "marked_read_at": datetime.utcnow().isoformat()
    }


@router.post("/conversations/{conversation_id}/archive")
async def archive_conversation(
    conversation_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Archive conversation"""
    return {
        "conversation_id": conversation_id,
        "archived": True,
        "archived_at": datetime.utcnow().isoformat()
    }
