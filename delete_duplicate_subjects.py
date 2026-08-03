import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Keep only the first occurrence of each subject
cursor.execute("""
DELETE FROM subjects
WHERE subject_id NOT IN (
    SELECT MIN(subject_id)
    FROM subjects
    GROUP BY subject_name
)
""")

conn.commit()
conn.close()

print("Duplicate subjects deleted successfully!")