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

    cursor.execute("DELETE FROM teachers")
    cursor.execute("DELETE FROM assignments")

    clean_teachers = [
        ("Varsha Shinde", "varsha@sies.edu", "Data Science"),
        ("Rashmi Prabha", "rashmi@sies.edu", "Data Science"),
        ("Tina Tommy", "tina@sies.edu", "Data Science"),
        ("Palak Jadhav", "palak@sies.edu", "Data Science"),
        ("Sana Chougule", "sana@sies.edu", "Data Science"),
        ("Anita Desai", "anita@sies.edu", "Data Science"),
        ("Ramesh Iyer", "ramesh@sies.edu", "Data Science"),
        ("Priya Nair", "priya@sies.edu", "Data Science"),
        ("Suresh Patil", "suresh@sies.edu", "Data Science"),
        ("Vishal Kumar", "vishal@sies.edu", "Data Science"),
        ("Nutan Sawant", "nutan@sies.edu", "Data Science")
    ]
    for name, email, dept in clean_teachers:
        cursor.execute(
            "INSERT INTO teachers (teacher_name, email, department) VALUES (?, ?, ?)",
            (name, email, dept)
        )

    assignments = [
        ("FY DS", "FDS", "Rashmi Prabha", "CR-02"),
        ("FY DS", "Python Programming", "Nutan Sawant", "CR-02"),
        ("FY DS", "Descriptive Statistics", "Varsha Shinde", "CR-02"),
        ("FY DS", "SIES Development", "Tina Tommy", "CR-02"),

        ("SY DS", "DSA", "Sana Chougule", "CR-03"),
        ("SY DS", "Statistical Inference", "Anita Desai", "CR-03"),
        ("SY DS", "CC - SIES Development", "Ramesh Iyer", "CR-03"),
        ("SY DS", "OE1 - Social Media Marketing", "Priya Nair", "CR-03"),

        ("TY DS", "Big Data Analytics", "Suresh Patil", "CR-04"),
        ("TY DS", "Deep Learning", "Vishal Kumar", "CR-04"),
        ("TY DS", "Natural Language Processing (NLP)", "Rashmi Prabha", "CR-04"),
        ("TY DS", "Research Methodology in Data Science", "Palak Jadhav", "CR-04"),
    ]
    for class_name, subject_name, teacher_name, room_name in assignments:
        cursor.execute("""
        INSERT INTO assignments (class_name, subject_name, teacher_name, room_name)
        VALUES (?, ?, ?, ?)
        """, (class_name, subject_name, teacher_name, room_name))

    conn.commit()
    conn.close()

    print("Database Created Successfully!")


create_database()