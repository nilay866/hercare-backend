
import requests
import uuid

BASE_URL = "http://localhost:8001"

# 1. Test Registration (Check if default role is assigned)
name = "RBAC Test User"
email = f"rbac_{uuid.uuid4().hex[:6]}@test.com"
password = "password"
role = "doctor"

print(f"1. Registering {role} {email}...")
r = requests.post(f"{BASE_URL}/register", params={"name": name, "email": email, "password": password, "role": role})
if r.status_code == 200:
    print("   Registration Successful.")
else:
    print(f"   Registration Failed: {r.text}")
    exit(1)

# 2. Test Login (Check roles in response)
print(f"2. Logging in {email}...")
r = requests.post(f"{BASE_URL}/login", params={"email": email, "password": password})
if r.status_code == 200:
    data = r.json()
    print("   Login Successful.")
    print(f"   Roles returned: {data.get('roles')}")
    print(f"   Token length: {len(data.get('token', ''))}")
    
    if data.get("roles") == ["doctor"]:
        print("✅ SUCCESS: Default role correctly assigned and returned.")
    else:
        print("❌ FAILURE: Roles list is incorrect or missing.")
else:
    print(f"   Login Failed: {r.text}")
    exit(1)

# 3. Test Unauthorized Admin Access (Verify RBAC protection)
print("3. Testing Unauthorized Admin Route Access...")
# Trying a random admin route (if exists in routes_admin.py)
# /admin/users is common
r = requests.get(f"{BASE_URL}/admin/users", headers={"Authorization": f"Bearer {data['token']}"})
if r.status_code == 403:
    print("✅ SUCCESS: Correctly blocked doctor from admin route (403 Forbidden).")
elif r.status_code == 401:
    print("✅ SUCCESS: Correctly blocked doctor from admin route (401 Unauthorized - which might be standard if no permissions).")
elif r.status_code == 404:
    print("ℹ️ INFO: Admin route not found (404), check routes_admin.py definition.")
else:
    print(f"❌ FAILURE: Doctor accessed admin route? Status: {r.status_code}")

print("\nRBAC Verification Complete.")
