import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(subjects)")

for column in cursor.fetchall():
    print(column)

conn.close()