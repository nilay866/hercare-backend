#!/usr/bin/env python3
"""
Quick verification script for Phase 1 implementation
Checks if all imports work and database models are properly defined
"""

import sys
import os

def check_imports():
    """Check if all modules can be imported"""
    print("🔍 Checking imports...")
    
    try:
        print("  ✓ Importing FastAPI...")
        from fastapi import FastAPI
        
        print("  ✓ Importing SQLAlchemy...")
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        print("  ✓ Importing auth module...")
        from auth import (
            create_token_with_roles,
            verify_password,
            hash_password,
            get_current_user_with_roles,
            require_role,
            require_permission,
            get_client_ip
        )
        
        print("  ✓ Importing RBAC module...")
        from rbac import (
            get_user_roles,
            require_role as rbac_require_role,
            has_role,
            has_permission
        )
        
        print("  ✓ Importing audit module...")
        from audit import AuditService
        
        print("  ✓ Importing models...")
        from models import (
            User, HealthLog, PregnancyProfile, DoctorProfile,
            DoctorPatientLink, MedicalReport, Medication, DietPlan,
            EmergencyRequest, Consultation, MedicalHistory,
            # New models
            Role, UserRole, Organization, AuditLog, Appointment, File, Notification
        )
        
        print("  ✓ Importing admin routes...")
        from routes_admin import router as admin_router
        
        print("  ✓ Importing main app...")
        from main import app
        
        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_models():
    """Check if all models are properly defined"""
    print("\n🔍 Checking models...")
    
    try:
        from models import Base
        from sqlalchemy import inspect
        
        # Check existing models
        existing_models = [
            'User', 'HealthLog', 'PregnancyProfile', 'DoctorProfile',
            'DoctorPatientLink', 'MedicalReport', 'Medication', 'DietPlan',
            'EmergencyRequest', 'Consultation', 'MedicalHistory'
        ]
        
        # Check new models
        new_models = ['Role', 'UserRole', 'Organization', 'AuditLog', 'Appointment', 'File', 'Notification']
        
        all_models = existing_models + new_models
        
        for model_name in all_models:
            try:
                exec(f"from models import {model_name}")
                print(f"  ✓ Model '{model_name}' is defined")
            except Exception as e:
                print(f"  ❌ Model '{model_name}' not found: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Model check error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_auth_functions():
    """Check if auth functions are properly defined"""
    print("\n🔍 Checking auth functions...")
    
    try:
        from auth import (
            hash_password,
            verify_password,
            create_token_with_roles,
            get_current_user_with_roles,
            require_role,
            require_permission
        )
        
        # Test password hashing
        test_password = "test123"
        hashed = hash_password(test_password)
        if verify_password(test_password, hashed):
            print("  ✓ Password hashing/verification works")
        else:
            print("  ❌ Password verification failed")
            return False
        
        # Test token creation
        token = create_token_with_roles("test-user-id", "Test User", ["patient", "doctor"])
        if token and len(token) > 0:
            print("  ✓ Token creation works")
        else:
            print("  ❌ Token creation failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Auth function check error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_admin_routes():
    """Check if admin routes are properly defined"""
    print("\n🔍 Checking admin routes...")
    
    try:
        from routes_admin import router
        
        routes = []
        for route in router.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
                print(f"  ✓ Route: {route.path}")
        
        if len(routes) > 0:
            print(f"\n  Total admin routes: {len(routes)}")
            return True
        else:
            print("  ❌ No admin routes found")
            return False
        
    except Exception as e:
        print(f"  ❌ Admin routes check error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("HerCare Phase 1 Implementation Verification")
    print("=" * 60)
    
    checks = [
        ("Imports", check_imports),
        ("Models", check_models),
        ("Auth Functions", check_auth_functions),
        ("Admin Routes", check_admin_routes),
    ]
    
    results = {}
    for check_name, check_func in checks:
        results[check_name] = check_func()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All checks passed! Phase 1 implementation is ready.")
        print("\nNext steps:")
        print("1. Run: python seed_roles.py (to create default roles)")
        print("2. Set DATABASE_URL environment variable")
        print("3. Run: uvicorn main:app --reload")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
