import sqlite3

conn = sqlite3.connect("database/medical.db")

cursor = conn.cursor()

# Lab Results Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS lab_results (
    document_id TEXT,
    test_name TEXT,
    result TEXT,
    unit TEXT,
    validation_status TEXT
)
""")

# Discharge Summary Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS discharge_summaries (
    document_id TEXT,
    patient_name TEXT,
    age TEXT,
    gender TEXT,
    diagnosis TEXT,
    admission_date TEXT,
    discharge_date TEXT,
    hospital_name TEXT,
    doctor_name TEXT
)
""")

conn.commit()

conn.close()

print("Database tables created successfully!")