import sqlite3

conn = sqlite3.connect("database/medical.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM lab_results")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()