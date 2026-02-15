
from database import engine
from models import Base
import models # Ensure all models are registered

print("Syncing database schema for RBAC...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ RBAC tables created successfully.")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
