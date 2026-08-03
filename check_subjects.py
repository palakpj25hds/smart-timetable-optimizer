import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM subjects")

subjects = cursor.fetchall()

for subject in subjects:
    print(subject)

conn.close()