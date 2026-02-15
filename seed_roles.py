#!/usr/bin/env python3
"""
Seed script to create initial roles and permissions
Run once after database setup: python seed_roles.py
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Role

# ────── Define Role Permissions ──────
SUPER_ADMIN_PERMISSIONS = {
    # User management
    "user.create": True,
    "user.read": True,
    "user.update": True,
    "user.delete": True,
    "user.list": True,
    
    # Role management
    "role.create": True,
    "role.read": True,
    "role.update": True,
    "role.delete": True,
    "role.assign": True,
    
    # Organization management
    "organization.create": True,
    "organization.read": True,
    "organization.update": True,
    "organization.delete": True,
    "organization.verify": True,
    
    # Doctor approval
    "doctor.approve": True,
    "doctor.reject": True,
    "doctor.suspend": True,
    
    # Audit logs
    "audit.read": True,
    "audit.delete": True,
    
    # System settings
    "system.settings": True,
}

HOSPITAL_ADMIN_PERMISSIONS = {
    # User management (limited)
    "user.read": True,
    "user.update": True,
    "user.list": True,
    
    # Doctor management
    "doctor.approve": True,
    "doctor.read": True,
    "doctor.list": True,
    "doctor.suspend": True,
    
    # Patient management
    "patient.read": True,
    "patient.list": True,
    
    # Audit logs
    "audit.read": True,
    
    # Organization
    "organization.read": True,
    "organization.update": True,
}

DOCTOR_PERMISSIONS = {
    # Patient management
    "patient.read": True,
    "patient.create": True,
    "patient.list": True,
    
    # Consultations
    "consultation.create": True,
    "consultation.read": True,
    "consultation.update": True,
    
    # Prescriptions
    "prescription.create": True,
    "prescription.read": True,
    "prescription.update": True,
    
    # Appointments
    "appointment.read": True,
    "appointment.update": True,
    
    # Medical reports
    "report.read": True,
    "report.create": True,
    
    # Profile
    "profile.read": True,
    "profile.update": True,
}

PATIENT_PERMISSIONS = {
    # Own profile
    "profile.read": True,
    "profile.update": True,
    
    # Health logs
    "health.create": True,
    "health.read": True,
    "health.update": True,
    
    # Consultations
    "consultation.read": True,
    
    # Appointments
    "appointment.create": True,
    "appointment.read": True,
    "appointment.cancel": True,
    
    # Medical info
    "medical.read": True,
    
    # Prescriptions
    "prescription.read": True,
    
    # Notifications
    "notification.read": True,
}

# ────── Define Roles ──────
ROLES = [
    {
        "name": "super_admin",
        "description": "System administrator with full access",
        "permissions": SUPER_ADMIN_PERMISSIONS
    },
    {
        "name": "hospital_admin",
        "description": "Hospital administrator - manages doctors and patients",
        "permissions": HOSPITAL_ADMIN_PERMISSIONS
    },
    {
        "name": "doctor",
        "description": "Doctor - can consult patients",
        "permissions": DOCTOR_PERMISSIONS
    },
    {
        "name": "patient",
        "description": "Patient - can manage own health records",
        "permissions": PATIENT_PERMISSIONS
    }
]


def seed_roles():
    """Create default roles if they don't exist"""
    db = SessionLocal()
    
    try:
        for role_data in ROLES:
            # Check if role already exists
            existing = db.query(Role).filter(Role.name == role_data["name"]).first()
            
            if existing:
                print(f"✓ Role '{role_data['name']}' already exists")
                continue
            
            # Create new role
            role = Role(
                id=uuid.uuid4(),
                name=role_data["name"],
                description=role_data["description"],
                permissions=role_data["permissions"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(role)
            print(f"✓ Created role '{role_data['name']}'")
        
        db.commit()
        print("\n✅ Role seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding roles: {str(e)}")
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()
