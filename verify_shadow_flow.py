
import requests
import uuid

BASE_URL = "http://localhost:8001"

# 1. Login as Doctor (Assume one exists, or create one)
# I'll try to login with known doctor credentials or signup a temp one.
# Use random doctor
doctor_email = f"doc_{uuid.uuid4().hex[:6]}@test.com"
doctor_pass = "password"

print(f"1. Creating Doctor {doctor_email}...")
# Register User
r = requests.post(f"{BASE_URL}/register", params={"name": "Dr Test", "email": doctor_email, "password": doctor_pass, "role": "doctor"})
if r.status_code != 200 and "already registered" not in r.text:
    print(f"Failed to register doctor: {r.text}")
    # Try login if exists
r = requests.post(f"{BASE_URL}/login", params={"email": doctor_email, "password": doctor_pass})
if r.status_code != 200:
    print(f"Failed to login doctor: {r.text}")
    exit(1)
doctor_token = r.json()["token"]
print("   Doctor Logged In.")

# 2. Create Shadow Patient
print("2. Creating Shadow Patient...")
r = requests.post(f"{BASE_URL}/register-patient", headers={"Authorization": f"Bearer {doctor_token}"}, 
                  params={"name": "Shadow Patient", "age": 30}) # email intentionally omitted
if r.status_code != 200:
    print(f"Failed to create shadow patient: {r.text}")
    exit(1)
data = r.json()
shadow_id = data["patient_id"]
share_code = data["share_code"]
print(f"   Shadow Patient Created. ID: {shadow_id}, Code: {share_code}")

# 3. Add a Health Log to Shadow Patient (to verify migration)
# Doctor cannot add health log directly via API usually, but let's assume Doctor adds a Consultation
print("3. Adding Consultation to Shadow Patient...")
r = requests.post(f"{BASE_URL}/consultation", headers={"Authorization": f"Bearer {doctor_token}"},
                  json={"patient_id": shadow_id, "diagnosis": "Shadow Flu", "medication": "Rest", "visit_date": "2026-02-15"})
if r.status_code != 200:
    print(f"Failed to add consultation: {r.text}")
    # Proceed anyway

# 4. Create Real Patient
patient_email = f"pat_{uuid.uuid4().hex[:6]}@test.com"
print(f"4. Creating Real Patient {patient_email}...")
r = requests.post(f"{BASE_URL}/register", params={"name": "Real Patient", "email": patient_email, "password": "password", "role": "patient"})
token_patient = r.json()["token"]
real_patient_id = r.json()["id"]
print(f"   Real Patient Created. ID: {real_patient_id}")

# 5. Link Records
print(f"5. Linking Records using Code {share_code}...")
r = requests.post(f"{BASE_URL}/patients/link", headers={"Authorization": f"Bearer {token_patient}"}, params={"share_code": share_code})
if r.status_code == 200:
    print("   Link Successful!")
else:
    print(f"   Link Failed: {r.text}")
    exit(1)

# 6. Verify Migration
print("6. Verifying Consultation Migration...")
# Patient fetches their consultations
r = requests.get(f"{BASE_URL}/consultations/{real_patient_id}", headers={"Authorization": f"Bearer {token_patient}"})
consultations = r.json()
found = False
for c in consultations:
    if c["diagnosis"] == "Shadow Flu":
        found = True
        print("   Found 'Shadow Flu' in Real Patient's consultations!")
        break

if found:
    print("\n✅ VERIFICATION PASSED: Shadow Record Linked Successfully.")
else:
    print("\n❌ VERIFICATION FAILED: Consultation not found.")

