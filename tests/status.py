import sqlite3

conn = sqlite3.connect("database/medical.db")
cursor = conn.cursor()

cursor.execute("""
SELECT validation_status, COUNT(*)
FROM lab_results
GROUP BY validation_status
""")

for row in cursor.fetchall():
    print(row)

conn.close()