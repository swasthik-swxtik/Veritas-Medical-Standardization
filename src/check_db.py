import sqlite3

conn = sqlite3.connect("database/medical.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(lab_results)")
columns = cursor.fetchall()

for column in columns:
    print(column)

conn.close()