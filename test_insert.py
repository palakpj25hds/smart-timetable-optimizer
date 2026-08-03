import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO subjects
(class_name, subject_name, department, periods)
VALUES (?, ?, ?, ?)
""", ("FY DS", "TEST", "Data Science", 1))

conn.commit()
conn.close()

print("Inserted successfully!")