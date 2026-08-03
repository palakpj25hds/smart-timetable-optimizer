import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM assignments
WHERE class_name = ''
""")

conn.commit()
conn.close()

print("Empty assignments deleted successfully!")