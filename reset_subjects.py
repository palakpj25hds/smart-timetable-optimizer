import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS subjects")


cursor.execute("""
CREATE TABLE subjects(
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    subject_name TEXT NOT NULL,
    department TEXT,
    periods INTEGER
)
""")


conn.commit()
conn.close()

print("Subjects table recreated successfully!")