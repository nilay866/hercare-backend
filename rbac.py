# ════════════════════════════════════
# RBAC (Role-Based Access Control)
# ════════════════════════════════════

from functools import wraps
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, UserRole, Role
import uuid

# ────── RBAC Dependency: Extract roles from JWT ──────
def get_user_roles(user_id: str, db: Session = Depends(get_db)):
    """Get all roles assigned to a user"""
    user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id_uuid).all()
    
    roles = []
    permissions = {}
    
    for user_role in user_roles:
        role = db.query(Role).filter(Role.id == user_role.role_id).first()
        if role:
            roles.append(role.name)
            permissions.update(role.permissions)
    
    return {
        "roles": roles,
        "permissions": permissions,
        "has_role": lambda r: r in roles,
        "has_permission": lambda p: permissions.get(p, False)
    }

# ────── Decorator: Require specific role ──────
def require_role(*required_roles):
    """Decorator to check if user has required role(s)"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, db: Session = None, **kwargs):
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            user_roles = db.query(UserRole).filter(UserRole.user_id == current_user.id).all()
            user_role_names = [db.query(Role).filter(Role.id == ur.role_id).first().name for ur in user_roles]
            
            if not any(role in user_role_names for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {', '.join(required_roles)}"
                )
            
            return await func(*args, current_user=current_user, db=db, **kwargs)
        return wrapper
    return decorator

# ────── Decorator: Require specific permission ──────
def require_permission(*required_permissions):
    """Decorator to check if user has required permission(s)"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, db: Session = None, **kwargs):
            if current_user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            user_roles = db.query(UserRole).filter(UserRole.user_id == current_user.id).all()
            permissions = {}
            
            for user_role in user_roles:
                role = db.query(Role).filter(Role.id == user_role.role_id).first()
                if role:
                    permissions.update(role.permissions)
            
            if not any(permissions.get(perm, False) for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required permissions: {', '.join(required_permissions)}"
                )
            
            return await func(*args, current_user=current_user, db=db, **kwargs)
        return wrapper
    return decorator

# ────── Helper: Check role ──────
def has_role(user_id: str, required_role: str, db: Session):
    """Check if user has a specific role"""
    user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id_uuid).all()
    
    for user_role in user_roles:
        role = db.query(Role).filter(Role.id == user_role.role_id).first()
        if role and role.name == required_role:
            return True
    
    return False

# ────── Helper: Check permission ──────
def has_permission(user_id: str, required_permission: str, db: Session):
    """Check if user has a specific permission"""
    user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id_uuid).all()
    
    for user_role in user_roles:
        role = db.query(Role).filter(Role.id == user_role.role_id).first()
        if role and role.permissions.get(required_permission, False):
            return True
    
    return False

# ────── Helper: Get all user roles ──────
def get_user_role_names(user_id: str, db: Session) -> list:
    """Get list of role names for a user"""
    user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id_uuid).all()
    
    roles = []
    for user_role in user_roles:
        role = db.query(Role).filter(Role.id == user_role.role_id).first()
        if role:
            roles.append(role.name)
    
    return roles

# ────── Helper: Get all user permissions ──────
def get_user_permissions(user_id: str, db: Session) -> dict:
    """Get all permissions for a user"""
    user_id_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id_uuid).all()
    
    permissions = {}
    for user_role in user_roles:
        role = db.query(Role).filter(Role.id == user_role.role_id).first()
        if role:
            permissions.update(role.permissions)
    
    return permissions
