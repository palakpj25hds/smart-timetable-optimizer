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

    try:
        cursor.execute("ALTER TABLE classes ADD COLUMN student_count INTEGER")
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

    cursor.execute("DELETE FROM teachers")
    cursor.execute("DELETE FROM assignments")
    cursor.execute("DELETE FROM classes")
    cursor.execute("DELETE FROM classrooms")

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

    clean_classes = [
        ("FY DS", 60),
        ("SY DS", 55),
        ("TY DS", 50)
    ]
    for class_name, student_count in clean_classes:
        cursor.execute(
            "INSERT INTO classes (class_name, student_count) VALUES (?, ?)",
            (class_name, student_count)
        )

    clean_classrooms = [
        ("CR-02", 65, "Classroom"),
        ("CR-03", 60, "Classroom"),
        ("CR-04", 55, "Classroom")
    ]
    for room_name, capacity, room_type in clean_classrooms:
        cursor.execute(
            "INSERT INTO classrooms (room_name, capacity, room_type) VALUES (?, ?, ?)",
            (room_name, capacity, room_type)
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


ensure_database_ready()


@app.route("/")
def home():
    return render_template("index.html")


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
    cursor.execute("INSERT INTO teachers (teacher_name, email, department) VALUES (?, ?, ?)",
                   (teacher_name, email, department))
    conn.commit()
    conn.close()
    return "Teacher Saved Successfully!"


@app.route("/view_teachers")
def view_teachers():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    conn.close()
    return render_template("view_teachers.html", teachers=teachers)


@app.route("/delete-teacher/<int:teacher_id>")
def delete_teacher(teacher_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE teacher_id = ?", (teacher_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_teachers"))


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
    cursor.execute("INSERT INTO subjects (subject_name, department, periods) VALUES (?, ?, ?)",
                   (subject_name, department, periods))
    conn.commit()
    conn.close()
    return "Subject Saved Successfully!"


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
    cursor.execute("INSERT INTO classrooms (room_name, capacity, room_type) VALUES (?, ?, ?)",
                   (room_name, capacity, room_type))
    conn.commit()
    conn.close()
    return "Classroom Saved Successfully!"


@app.route("/class")
def class_page():
    return render_template("class.html")


@app.route("/save_class", methods=["POST"])
def save_class():
    class_name = request.form["class_name"]
    student_count = request.form.get("student_count", 0)
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (class_name, student_count) VALUES (?, ?)",
                   (class_name, student_count))
    conn.commit()
    conn.close()
    return "Class Saved Successfully!"


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
    return render_template("assignment.html", classes=classes, subjects=subjects,
                            teachers=teachers, classrooms=classrooms)


@app.route("/save_assignment", methods=["POST"])
def save_assignment():
    class_name = request.form["class_name"]
    subject_name = request.form["subject_name"]
    teacher_name = request.form["teacher_name"]
    room_name = request.form["room_name"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT student_count FROM classes WHERE class_name = ?", (class_name,))
    class_data = cursor.fetchone()
    class_strength = class_data[0] if class_data and class_data[0] else 0

    cursor.execute("SELECT capacity FROM classrooms WHERE room_name = ?", (room_name,))
    room_data = cursor.fetchone()
    room_capacity = room_data[0] if room_data and room_data[0] else 0

    warning = ""
    if class_strength and room_capacity and class_strength > room_capacity:
        warning = f"Warning: Class strength ({class_strength}) exceeds room capacity ({room_capacity})!"

    cursor.execute("""
    INSERT INTO assignments (class_name, subject_name, teacher_name, room_name)
    VALUES (?, ?, ?, ?)
    """, (class_name, subject_name, teacher_name, room_name))
    conn.commit()
    conn.close()

    if warning:
        return f"""
        <div style="max-width:400px; margin:50px auto; padding:20px; background-color:#f8d7da; 
        border:2px solid #dc3545; border-radius:10px; text-align:center; font-family:sans-serif;">
            <h2 style="color:#dc3545;">Assignment Saved (with warning)</h2>
            <p>{warning}</p>
            <a href="/assignment" style="color:#1e6fb0;">Back to Assignments</a>
        </div>
        """
    else:
        return """
        <div style="max-width:400px; margin:50px auto; padding:20px; background-color:#d4edda; 
        border:2px solid #28a745; border-radius:10px; text-align:center; font-family:sans-serif;">
            <h2 style="color:#28a745;">Success!</h2>
            <p>Assignment saved successfully.</p>
            <a href="/assignment" style="color:#1e6fb0;">Back to Assignments</a>
        </div>
        """


@app.route("/view_assignments")
def view_assignments():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()
    conn.close()
    return render_template("view_assignments.html", assignments=assignments)


@app.route("/delete-assignment/<int:assignment_id>")
def delete_assignment(assignment_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assignments WHERE assignment_id = ?", (assignment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_assignments"))


@app.route("/generate")
def generate():
    all_timetables = generate_timetable()
    search_class = request.args.get("class_name", "").strip().upper()

    if search_class:
        filtered_timetables = {}
        for class_name in all_timetables:
            if search_class in class_name.upper():
                filtered_timetables[class_name] = all_timetables[class_name]
        all_timetables = filtered_timetables

    current_date = datetime.now().strftime("%A, %d %B %Y")

    return render_template(
        "timetable.html",
        all_timetables=all_timetables,
        current_date=current_date
    )


@app.route("/admin-dashboard")
def admin_dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM classes")
    total_classes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM assignments")
    total_assignments = cursor.fetchone()[0]

    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT teacher_name FROM attendance WHERE date = ? AND status = 'absent'", (today,))
    absent_today = cursor.fetchall()

    conn.close()

    return render_template("admin_dashboard.html",
        total_teachers=total_teachers,
        total_classes=total_classes,
        total_assignments=total_assignments,
        absent_today=absent_today
    )


@app.route("/attendance-analytics")
def attendance_analytics():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT teacher_name, COUNT(*) as absent_count
            FROM attendance
            WHERE status = 'absent'
            GROUP BY teacher_name
            ORDER BY absent_count DESC
        """)
        teacher_absences = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'absent'")
        total_absences = cursor.fetchone()[0]

        conn.close()

        return render_template("attendance_analytics.html",
            teacher_absences=teacher_absences,
            total_absences=total_absences
        )
    except Exception as e:
        return f"ERROR: {str(e)}"


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
    cursor.execute("UPDATE teachers SET password = ? WHERE teacher_name = ?", (password, teacher_name))
    conn.commit()
    conn.close()
    return """
    <div style="max-width:400px; margin:50px auto; padding:20px; background-color:#d4edda; 
    border:2px solid #28a745; border-radius:10px; text-align:center; font-family:sans-serif;">
        <h2 style="color:#28a745;">Success!</h2>
        <p>Password has been set successfully.</p>
        <a href="/" style="color:#1e6fb0;">Go to Home</a>
    </div>
    """


@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        try:
            teacher_name = request.form["teacher_name"]
            password = request.form["password"]
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM teachers WHERE teacher_name = ? AND password = ?",
                           (teacher_name, password))
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

        teacher_name = session["teacher_name"]
        today_name = datetime.now().strftime("%A")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT class_name, subject_name, room_name
            FROM assignments
            WHERE teacher_name = ?
        """, (teacher_name,))
        today_classes = cursor.fetchall()
        conn.close()

        return render_template("teacher_dashboard.html",
            teacher_name=teacher_name,
            today_name=today_name,
            today_classes=today_classes
        )
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
        cursor.execute("INSERT INTO attendance (teacher_name, date, status) VALUES (?, ?, ?)",
                       (teacher_name, today, "absent"))
        conn.commit()
        conn.close()
        return f"""
        <div style="max-width:400px; margin:50px auto; padding:20px; background-color:#fff3cd; 
        border:2px solid #f0a500; border-radius:10px; text-align:center; font-family:sans-serif;">
            <h2 style="color:#f0a500;">Marked Absent</h2>
            <p><b>{teacher_name}</b> has been marked absent for today.</p>
            <p>Substitutes have been assigned automatically.</p>
            <a href="/generate" style="color:#1e6fb0;">View Updated Timetable</a>
        </div>
        """
    except Exception as e:
        return f"ERROR: {str(e)}"


@app.route("/teacher-logout")
def teacher_logout():
    session.pop("teacher_name", None)
    return redirect(url_for("teacher_login"))


if __name__ == "__main__":
    app.run(debug=True)