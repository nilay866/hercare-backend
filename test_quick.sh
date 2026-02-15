#!/bin/bash

# HerCare Platform - Quick Testing Commands
# Usage: source test_quick.sh or bash test_quick.sh

echo "🧪 HerCare Testing Quick Reference"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8000/api/v1"
EMAIL="testuser@example.com"
PASSWORD="Test@123456"

echo -e "${BLUE}Backend Health Check:${NC}"
echo "curl http://localhost:8000/health"
echo ""

echo -e "${BLUE}Phase 1 - Authentication:${NC}"
echo ""
echo "1. Register:"
echo "curl -X POST $BASE_URL/auth/register \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"first_name\":\"Test\",\"last_name\":\"User\"}'"
echo ""

echo "2. Login:"
echo "curl -X POST $BASE_URL/auth/login \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}'"
echo ""

echo "3. Get Profile (requires token - copy from login response):"
echo "curl -X GET $BASE_URL/users/profile \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN_HERE'"
echo ""

echo -e "${BLUE}Phase 2 - Appointments:${NC}"
echo ""
echo "4. Create Appointment:"
echo "curl -X POST $BASE_URL/appointments \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"doctor_id\":\"uuid\",\"scheduled_at\":\"2025-03-01T10:00:00Z\",\"reason\":\"Checkup\"}'"
echo ""

echo "5. List Appointments:"
echo "curl -X GET $BASE_URL/appointments \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo -e "${BLUE}Phase 3 - Doctor Features:${NC}"
echo ""
echo "6. Get Doctor Profile:"
echo "curl -X GET $BASE_URL/doctors/profile \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo "7. Get Prescriptions:"
echo "curl -X GET $BASE_URL/doctors/prescriptions \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo -e "${BLUE}Phase 4 - Telemedicine:${NC}"
echo ""
echo "8. Schedule Consultation:"
echo "curl -X POST $BASE_URL/telemedicine/consultations \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"doctor_id\":\"uuid\",\"title\":\"Video Call\",\"scheduled_at\":\"2025-03-01T14:00:00Z\",\"consultation_type\":\"video\"}'"
echo ""

echo "9. Get Consultations:"
echo "curl -X GET $BASE_URL/telemedicine/consultations \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo -e "${BLUE}Phase 5 - Analytics:${NC}"
echo ""
echo "10. Record Health Metric:"
echo "curl -X POST $BASE_URL/analytics/health-metrics \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"metric_type\":\"blood_pressure\",\"value\":120,\"systolic_value\":120,\"diastolic_value\":80,\"unit\":\"mmHg\"}'"
echo ""

echo "11. Get Health Metrics:"
echo "curl -X GET $BASE_URL/analytics/health-metrics \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo "12. Get Health Dashboard:"
echo "curl -X GET $BASE_URL/analytics/dashboard \\"
echo "  -H 'Authorization: Bearer YOUR_TOKEN'"
echo ""

echo -e "${YELLOW}Quick Testing Steps:${NC}"
echo ""
echo "1. Start backend: cd hercare-backend && python main.py"
echo "2. Run Python test: python quick_test.py"
echo "3. Or use curl commands above"
echo "4. For Flutter: cd hercare_app && flutter run"
echo ""

echo -e "${GREEN}✅ Testing guide complete!${NC}"
echo "For more details, see TESTING_GUIDE.md"
