from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime
from timetable import generate_timetable

app = Flask(__name__)
app.secret_key = "smart_timetable_secret_key"


def ensure_database_ready():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE teachers ADD COLUMN password TEXT")
    except sqlite3.OperationalError:
        pass

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


ensure_database_ready()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- TEACHER ----------------

@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


@app.route("/save_teacher", methods=["POST"])
def save_teacher():
    teacher_name = request.form["teacher_name"]
    email = request.form["email"]
    department = request.form["department"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO teachers (teacher_name, email, department)
    VALUES (?, ?, ?)
    """, (teacher_name, email, department))
    conn.commit()
    conn.close()

    return "Teacher Saved Successfully!"


@app.route("/reset-teachers-clean")
def reset_teachers_clean():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teachers")

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
        ("Vishal Kumar", "vishal@sies.edu", "Data Science")
    ]

    for name, email, dept in clean_teachers:
        cursor.execute(
            "INSERT INTO teachers (teacher_name, email, department) VALUES (?, ?, ?)",
            (name, email, dept)
        )

    conn.commit()
    conn.close()

    return "Teachers table reset with clean unique names!"


@app.route("/view_teachers")
def view_teachers():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()

    return render_template("view_teachers.html", teachers=teachers)


# ---------------- SUBJECT ----------------

@app.route("/subject")
def subject():
    return render_template("subject.html")


@app.route("/save_subject", methods=["POST"])
def save_subject():
    subject_name = request.form["subject_name"]
    department = request.form["department"]
    periods = request.form["periods"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO subjects (subject_name, department, periods)
    VALUES (?, ?, ?)
    """, (subject_name, department, periods))
    conn.commit()
    conn.close()

    return "Subject Saved Successfully!"


# ---------------- CLASSROOM ----------------

@app.route("/classroom")
def classroom():
    return render_template("classroom.html")


@app.route("/save_classroom", methods=["POST"])
def save_classroom():
    room_name = request.form["room_name"]
    capacity = request.form["capacity"]
    room_type = request.form["room_type"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO classrooms (room_name, capacity, room_type)
    VALUES (?, ?, ?)
    """, (room_name, capacity, room_type))
    conn.commit()
    conn.close()

    return "Classroom Saved Successfully!"


# ---------------- CLASS ----------------

@app.route("/class")
def class_page():
    return render_template("class.html")


@app.route("/save_class", methods=["POST"])
def save_class():
    class_name = request.form["class_name"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO classes (class_name)
    VALUES (?)
    """, (class_name,))
    conn.commit()
    conn.close()

    return "Class Saved Successfully!"


# ---------------- ASSIGNMENT ----------------

@app.route("/assignment")
def assignment():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT class_name FROM classes")
    classes = cursor.fetchall()

    cursor.execute("SELECT subject_name FROM subjects")
    subjects = cursor.fetchall()

    cursor.execute("SELECT teacher_name FROM teachers")
    teachers = cursor.fetchall()

    cursor.execute("SELECT room_name FROM classrooms")
    classrooms = cursor.fetchall()

    conn.close()

    return render_template(
        "assignment.html",
        classes=classes,
        subjects=subjects,
        teachers=teachers,
        classrooms=classrooms
    )


@app.route("/save_assignment", methods=["POST"])
def save_assignment():
    class_name = request.form["class_name"]
    subject_name = request.form["subject_name"]
    teacher_name = request.form["teacher_name"]
    room_name = request.form["room_name"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO assignments
    (class_name, subject_name, teacher_name, room_name)
    VALUES (?, ?, ?, ?)
    """, (class_name, subject_name, teacher_name, room_name))
    conn.commit()
    conn.close()

    return "Assignment Saved Successfully!"


@app.route("/bulk-add-assignments-v3")
def bulk_add_assignments_v3():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assignments")

    assignments = [
        ("FY DS", "DSA", "Varsha Shinde", "CR-02"),
        ("FY DS", "DBMS", "Rashmi Prabha", "CR-02"),
        ("FY DS", "ML", "Tina Tommy", "CR-02"),
        ("FY DS", "AEC1 - English", "Palak Jadhav", "CR-02"),

        ("SY DS", "DSA", "Sana Chougule", "CR-03"),
        ("SY DS", "Statistical Inference", "Anita Desai", "CR-03"),
        ("SY DS", "CC - SIES Development", "Ramesh Iyer", "CR-03"),
        ("SY DS", "OE1 - Social Media Marketing", "Priya Nair", "CR-03"),

        ("TY DS", "DBMS", "Suresh Patil", "CR-04"),
        ("TY DS", "ML", "Vishal Kumar", "CR-04"),
        ("TY DS", "OE2 - Brand Management", "Varsha Shinde", "CR-04"),
        ("TY DS", "AEC2 - Hindi", "Rashmi Prabha", "CR-04"),
    ]

    for class_name, subject_name, teacher_name, room_name in assignments:
        cursor.execute("""
        INSERT INTO assignments (class_name, subject_name, teacher_name, room_name)
        VALUES (?, ?, ?, ?)
        """, (class_name, subject_name, teacher_name, room_name))

    conn.commit()
    conn.close()

    return f"Added {len(assignments)} assignments — FY, SY, TY each in their own room!"


@app.route("/update-fy-ty-subjects")
def update_fy_ty_subjects():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teachers WHERE teacher_name = ?", ("Nutan Sawant",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO teachers (teacher_name, email, department) VALUES (?, ?, ?)",
            ("Nutan Sawant", "nutan@sies.edu", "Data Science")
        )

    cursor.execute("DELETE FROM assignments WHERE class_name = 'FY DS'")
    cursor.execute("DELETE FROM assignments WHERE class_name = 'TY DS'")

    new_assignments = [
        ("FY DS", "FDS", "Rashmi Prabha", "CR-02"),
        ("FY DS", "Python Programming", "Nutan Sawant", "CR-02"),
        ("FY DS", "Descriptive Statistics", "Varsha Shinde", "CR-02"),
        ("FY DS", "SIES Development", "Tina Tommy", "CR-02"),

        ("TY DS", "Big Data Analytics", "Suresh Patil", "CR-04"),
        ("TY DS", "Deep Learning", "Vishal Kumar", "CR-04"),
        ("TY DS", "Natural Language Processing (NLP)", "Rashmi Prabha", "CR-04"),
    ]

    for class_name, subject_name, teacher_name, room_name in new_assignments:
        cursor.execute("""
        INSERT INTO assignments (class_name, subject_name, teacher_name, room_name)
        VALUES (?, ?, ?, ?)
        """, (class_name, subject_name, teacher_name, room_name))

    conn.commit()
    conn.close()

    return f"Updated! FY and TY subjects changed, SY untouched. Added {len(new_assignments)} assignments."


@app.route("/view_assignments")
def view_assignments():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()
    conn.close()

    return render_template("view_assignments.html", assignments=assignments)


# ---------------- GENERATE ----------------

@app.route("/generate")
def generate():
    all_timetables = generate_timetable()
    return render_template(
        "timetable.html",
        all_timetables=all_timetables
    )


# ---------------- SET PASSWORD ----------------

@app.route("/set-password-page")
def set_password_page():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_name FROM teachers")
    teachers = cursor.fetchall()
    conn.close()

    return render_template("set_password.html", teachers=teachers)


@app.route("/save_password", methods=["POST"])
def save_password():
    teacher_name = request.form["teacher_name"]
    password = request.form["password"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE teachers SET password = ? WHERE teacher_name = ?",
        (password, teacher_name)
    )
    conn.commit()
    conn.close()

    return "Password Set Successfully!"


# ---------------- TEACHER LOGIN ----------------

@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        try:
            teacher_name = request.form["teacher_name"]
            password = request.form["password"]

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM teachers WHERE teacher_name = ? AND password = ?",
                (teacher_name, password)
            )
            teacher = cursor.fetchone()
            conn.close()

            if teacher:
                session["teacher_name"] = teacher_name
                return redirect(url_for("teacher_dashboard"))
            else:
                return "Invalid name or password. <a href='/teacher-login'>Try again</a>"
        except Exception as e:
            return f"ERROR: {str(e)}"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_name FROM teachers")
    teachers = cursor.fetchall()
    conn.close()

    return render_template("teacher_login.html", teachers=teachers)


@app.route("/teacher-dashboard")
def teacher_dashboard():
    try:
        if "teacher_name" not in session:
            return redirect(url_for("teacher_login"))

        return render_template("teacher_dashboard.html", teacher_name=session["teacher_name"])
    except Exception as e:
        return f"ERROR: {str(e)}"


@app.route("/mark-absent-today", methods=["POST"])
def mark_absent_today():
    try:
        if "teacher_name" not in session:
            return redirect(url_for("teacher_login"))

        teacher_name = session["teacher_name"]
        today = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (teacher_name, date, status) VALUES (?, ?, ?)",
            (teacher_name, today, "absent")
        )
        conn.commit()
        conn.close()

        return f"{teacher_name} marked absent for today. Substitutes assigned automatically. <a href='/generate'>View Timetable</a>"
    except Exception as e:
        return f"ERROR: {str(e)}"


@app.route("/teacher-logout")
def teacher_logout():
    session.pop("teacher_name", None)
    return redirect(url_for("teacher_login"))


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)