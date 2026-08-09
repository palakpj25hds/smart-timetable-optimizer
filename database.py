import sqlite3


def create_database():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers(
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT NOT NULL,
        email TEXT,
        department TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects(
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL,
        subject_name TEXT NOT NULL,
        department TEXT,
        periods INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classrooms(
        classroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name TEXT NOT NULL,
        capacity INTEGER,
        room_type TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes(
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments(
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL,
        subject_name TEXT NOT NULL,
        teacher_name TEXT NOT NULL,
        room_name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

    print("Database Created Successfully!")


create_database()