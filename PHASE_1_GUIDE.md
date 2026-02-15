# Phase 1 Implementation Guide

**Status**: ✅ COMPLETE  
**Date**: February 15, 2026  
**Phase**: 1 (Foundation - Weeks 1-3)

## Overview

Phase 1 implementation adds the **RBAC (Role-Based Access Control)** foundation and admin API to your HerCare backend. All changes are **backward compatible** - no existing code is broken.

## What Was Added

### 1. New Database Models (models.py)

Added 7 new database tables while preserving all existing models:

```
Role                    - User roles (super_admin, hospital_admin, doctor, patient)
UserRole               - Many-to-many: Users ↔ Roles
Organization           - Hospital/clinic information & verification
AuditLog               - Track all user actions (HIPAA-ready)
Appointment            - Doctor-patient appointments
File                   - Secure file uploads (S3-ready)
Notification           - Multi-channel notifications (email, SMS, push, in-app)
```

### 2. Authentication Enhancements (auth.py)

- ✅ JWT tokens now include roles array
- ✅ New: `create_token_with_roles()` - Create tokens with embedded roles
- ✅ New: `get_current_user_with_roles()` - Get user with roles attached
- ✅ New: `require_role()` & `require_permission()` - Route decorators
- ✅ New: `has_role()` & `has_permission()` - Helper functions

### 3. RBAC Middleware (rbac.py)

Complete role-based access control system:

- `get_user_roles()` - Get user's roles and permissions
- `@require_role()` - Decorator for role-based access
- `@require_permission()` - Decorator for permission-based access
- `has_role()` - Check if user has specific role
- `has_permission()` - Check if user has specific permission
- Helper functions for permission management

### 4. Audit Logging Service (audit.py)

`AuditService` class for comprehensive action logging:

- `log()` - Generic action logging
- `log_login()` - Login events
- `log_user_creation()` - Track new users
- `log_user_update()` - Track changes
- `log_user_deletion()` - Track deletions
- `log_role_assignment()` - Track role changes
- `log_access()` - Track resource access
- `get_user_audit_logs()` - Retrieve user's audit history
- `get_resource_audit_logs()` - Retrieve resource's audit history
- `get_all_audit_logs()` - Get all audit logs

### 5. Admin API Routes (routes_admin.py)

Complete admin management API with 15+ endpoints:

#### Dashboard
- `GET /admin/dashboard` - Admin overview

#### User Management
- `POST /admin/users` - Create user
- `GET /admin/users` - List users (with filters)
- `GET /admin/users/{user_id}` - Get user details
- `PUT /admin/users/{user_id}` - Update user
- `DELETE /admin/users/{user_id}` - Delete user (super admin only)

#### Role Management
- `POST /admin/users/{user_id}/roles` - Assign role
- `GET /admin/users/{user_id}/roles` - Get user's roles

#### Audit & Compliance
- `GET /admin/audit-logs` - Get all audit logs
- `GET /admin/audit-logs/user/{user_id}` - Get user's audit logs

#### Doctor Management
- `GET /admin/doctors/pending-approval` - List pending doctors
- `POST /admin/doctors/{doctor_id}/approve` - Approve doctor

#### Organization Management
- `GET /admin/organizations` - List organizations
- `POST /admin/organizations/{org_id}/verify` - Verify organization

### 6. Role Seed Script (seed_roles.py)

Initializes 4 default roles with complete permission sets:

```
super_admin      - Full system access
hospital_admin   - Manage doctors, patients, approve doctors
doctor           - Manage patients, consultations, prescriptions
patient          - Manage own health records, appointments
```

### 7. Enhanced Login Endpoint (main.py)

Updated `/login` endpoint now:

- ✅ Returns user's roles array
- ✅ Logs login attempts (success & failure)
- ✅ Embeds roles in JWT token
- ✅ Records IP address for security

### 8. Dependency Updates (requirements.txt)

Added key packages:

```
alembic              - Database migrations
pytest               - Testing framework
pytest-asyncio       - Async testing
httpx                - HTTP client testing
python-multipart     - Form data handling
email-validator      - Email validation
python-decouple      - Configuration management
```

## Quick Start

### Step 1: Install Dependencies

```bash
cd /Users/nilaychavhan/Downloads/her/hercare-backend
pip install -r requirements.txt
```

### Step 2: Setup Environment

Create `.env` file:

```bash
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/hercare
SECRET_KEY=your-super-secret-key-change-in-production
EOF
```

### Step 3: Initialize Database

```bash
# This creates all tables (including new ones)
python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Step 4: Seed Default Roles

```bash
python seed_roles.py
```

Output should show:
```
✓ Role 'super_admin' created
✓ Role 'hospital_admin' created
✓ Role 'doctor' created
✓ Role 'patient' created
✅ Role seeding completed successfully!
```

### Step 5: Verify Implementation

```bash
python verify_phase1.py
```

This checks all imports and shows available admin routes.

### Step 6: Run Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the Admin API

### 1. Create Super Admin User

```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Admin&email=admin@example.com&password=admin123&role=super_admin"
```

Response:
```json
{
  "message": "User registered",
  "id": "user-uuid",
  "name": "Admin",
  "role": "super_admin",
  "roles": ["super_admin"],
  "token": "eyJhbGc..."
}
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=admin@example.com&password=admin123"
```

### 3. Use Token for Admin Endpoints

```bash
# Get dashboard
curl -X GET "http://localhost:8000/admin/dashboard" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# List users
curl -X GET "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create new user
curl -X POST "http://localhost:8000/admin/users" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John",
    "email": "john@example.com",
    "password": "doctor123",
    "role": "doctor"
  }'
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    FastAPI App                      │
└─────────────────────────────────────────────────────┘
         │                           │
         ├─ /auth routes (legacy)   │
         ├─ /admin routes ← NEW     │
         └─ /api routes (Phase 2)   │
                                     │
┌────────────────────────────────────────────────────────┐
│                  Authentication Layer                  │
├────────────────────────────────────────────────────────┤
│  JWT Token → [user_id, name, roles=[...]]             │
│                                                        │
│  get_current_user_with_roles() ← Extracts token       │
│  require_role(*roles)          ← Route protection     │
│  require_permission(*perms)    ← Fine-grained access  │
└────────────────────────────────────────────────────────┘
         │
┌────────────────────────────────────────────────────────┐
│              Authorization (RBAC) Layer               │
├────────────────────────────────────────────────────────┤
│  User ──┬──→ UserRole ──→ Role ──→ Permissions        │
│         │                                              │
│         └──→ Direct Permissions                        │
└────────────────────────────────────────────────────────┘
         │
┌────────────────────────────────────────────────────────┐
│              Audit Logging Layer                      │
├────────────────────────────────────────────────────────┤
│  Every action → AuditLog                              │
│  Tracks: user, action, resource, timestamp, IP        │
└────────────────────────────────────────────────────────┘
```

## Permission Matrix

### Super Admin
```
user.create       ✓  user.delete       ✓
user.read         ✓  role.assign       ✓
user.update       ✓  system.settings   ✓
user.list         ✓  audit.read        ✓
```

### Hospital Admin
```
user.read         ✓  doctor.approve    ✓
user.update       ✓  patient.read      ✓
user.list         ✓  patient.list      ✓
doctor.read       ✓  audit.read        ✓
doctor.list       ✓
```

### Doctor
```
patient.read      ✓  report.read       ✓
patient.create    ✓  report.create     ✓
patient.list      ✓  profile.read      ✓
consultation.*    ✓  profile.update    ✓
prescription.*    ✓  appointment.read  ✓
```

### Patient
```
profile.read      ✓  medical.read      ✓
profile.update    ✓  prescription.read ✓
health.*          ✓  notification.read ✓
consultation.read ✓  appointment.*     ✓
```

## Database Schema

### New Tables

#### roles
```sql
id (UUID)
name (VARCHAR, UNIQUE) - super_admin, hospital_admin, doctor, patient
description (VARCHAR)
permissions (JSON) - {"user.create": true, ...}
created_at, updated_at (TIMESTAMP)
```

#### user_roles (Many-to-Many)
```sql
id (UUID)
user_id (FK → users.id)
role_id (FK → roles.id)
assigned_at (TIMESTAMP)
assigned_by (FK → users.id, nullable)
```

#### organizations
```sql
id (UUID)
name (VARCHAR)
type (VARCHAR) - hospital, clinic, individual
address, phone, email, website (VARCHAR, nullable)
license_number (VARCHAR, nullable)
is_verified (BOOLEAN) - Admin approval
created_at, updated_at (TIMESTAMP)
```

#### audit_logs
```sql
id (UUID)
user_id (FK → users.id, nullable)
action (VARCHAR) - create, update, delete, login, access
resource_type (VARCHAR) - user, patient, prescription, etc.
resource_id (UUID, nullable)
old_value, new_value (JSON, nullable)
ip_address, user_agent (VARCHAR, nullable)
status (VARCHAR) - success, failed
details (TEXT, nullable)
created_at (TIMESTAMP, indexed)
```

#### appointments
```sql
id (UUID)
doctor_id, patient_id (FK → users.id)
appointment_date (DATETIME, indexed)
duration_minutes (INTEGER) - default 30
status (VARCHAR) - scheduled, completed, cancelled, no_show
appointment_type (VARCHAR)
notes, cancellation_reason (TEXT, nullable)
created_at, updated_at (TIMESTAMP)
```

#### files
```sql
id (UUID)
user_id (FK → users.id)
file_name, file_type (VARCHAR)
file_size (INTEGER)
s3_key, s3_url (VARCHAR, nullable)
resource_type (VARCHAR) - medical_report, prescription, profile_photo
resource_id (UUID, nullable)
uploaded_by (FK → users.id, nullable)
is_public (BOOLEAN)
access_log (JSON, nullable)
created_at (TIMESTAMP), expires_at (DATETIME, nullable)
```

#### notifications
```sql
id (UUID)
user_id (FK → users.id, indexed)
title, message (VARCHAR, TEXT)
notification_type (VARCHAR) - info, warning, error, success
channel (VARCHAR) - in_app, email, sms, push
is_read (BOOLEAN), read_at (DATETIME, nullable)
action_url (VARCHAR, nullable)
metadata (JSON, nullable)
created_at (TIMESTAMP, indexed)
```

## File Structure

```
hercare-backend/
├── main.py                  ← Updated: includes admin routes, role-aware login
├── auth.py                  ← Updated: JWT with roles, decorators
├── models.py                ← Updated: 7 new models added
├── database.py              ← No changes (existing)
├── schemas.py               ← No changes (existing)
├── rbac.py                  ← NEW: Role-based access control
├── audit.py                 ← NEW: Audit logging service
├── routes_admin.py          ← NEW: Admin API routes
├── seed_roles.py            ← NEW: Initialize default roles
├── verify_phase1.py         ← NEW: Verification script
├── requirements.txt         ← Updated: new dependencies
├── .env                     ← Create this: DATABASE_URL, SECRET_KEY
└── [other existing files]   ← All unchanged
```

## Testing

Run the verification script:

```bash
python verify_phase1.py
```

Expected output:
```
============================================================
HerCare Phase 1 Implementation Verification
============================================================

🔍 Checking imports...
  ✓ Importing FastAPI...
  ✓ Importing SQLAlchemy...
  ✓ Importing auth module...
  ✓ Importing RBAC module...
  ✓ Importing audit module...
  ✓ Importing models...
  ✓ Importing admin routes...
  ✓ Importing main app...

🔍 Checking models...
  ✓ Model 'User' is defined
  [... all 18 models ...]

🔍 Checking auth functions...
  ✓ Password hashing/verification works
  ✓ Token creation works

🔍 Checking admin routes...
  ✓ Route: /admin/dashboard
  [... 15+ routes ...]

============================================================
Summary
============================================================
Imports: ✅ PASS
Models: ✅ PASS
Auth Functions: ✅ PASS
Admin Routes: ✅ PASS

============================================================
✅ All checks passed! Phase 1 implementation is ready.

Next steps:
1. Run: python seed_roles.py (to create default roles)
2. Set DATABASE_URL environment variable
3. Run: uvicorn main:app --reload
```

## Backward Compatibility

✅ **Zero Breaking Changes**

- All existing endpoints continue to work
- All existing models preserved unchanged
- New models are additions, not modifications
- Legacy functions kept for compatibility
- Old JWT tokens still work (roles array added but optional)

## Security Considerations

1. **Password Hashing**: All passwords use bcrypt (industry standard)
2. **JWT Tokens**: 24-hour expiration, includes roles array
3. **Audit Logging**: All actions tracked with IP and user agent
4. **IP Tracking**: Failed logins logged for security
5. **RBAC**: Role-based access control prevents unauthorized actions
6. **Super Admin**: Limited to actual admin functions

## Next Steps (Phase 2)

After Phase 1 is complete and tested:

1. **React Admin Dashboard** - Web UI for admin functions
2. **Appointment Scheduling** - API for booking appointments
3. **File Uploads** - S3 integration for medical files
4. **Notifications** - Email, SMS, push notifications
5. **Doctor Approval System** - Verification flow for doctors

## Troubleshooting

### "Role not found" error

The roles haven't been seeded. Run:
```bash
python seed_roles.py
```

### "Access denied" error when accessing admin endpoints

Your user doesn't have the required role. Make sure:
1. User was created with `role="super_admin"` or `role="hospital_admin"`
2. Role was properly assigned in database
3. Token includes roles array

### Import errors

Make sure you've installed requirements:
```bash
pip install -r requirements.txt
```

### Database errors

Check that:
1. DATABASE_URL is set in .env
2. Database server is running
3. Models can create tables: `python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"`

## Contact & Support

For issues or questions about Phase 1 implementation, refer to:
- IMPLEMENTATION_ROADMAP.md - Week-by-week implementation details
- ARCHITECTURE.md - System design documentation
- REFERENCE_CARD.md - Quick command reference

---

**Phase 1 Status**: ✅ COMPLETE  
**Ready for Testing**: YES  
**Ready for Phase 2**: YES (after testing)
