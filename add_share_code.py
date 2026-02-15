
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
conn.autocommit = True
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE doctor_patient_links ADD COLUMN share_code VARCHAR UNIQUE")
    print("Added share_code column.")
except Exception as e:
    print(f"Error: {e}")
conn.close()
