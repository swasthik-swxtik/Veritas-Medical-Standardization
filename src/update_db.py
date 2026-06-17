import sqlite3

conn = sqlite3.connect("database/medical.db")

cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE lab_results
    ADD COLUMN validation_status TEXT
    """)

    print("validation_status column added!")

except Exception as e:
    print("Column already exists:", e)

conn.commit()
conn.close()