
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
conn.autocommit = True
cur = conn.cursor()
try:
    cur.execute("ALTER TABLE users ADD COLUMN phone VARCHAR")
    print("Added phone column.")
except Exception as e:
    print(f"Error: {e}")
conn.close()
