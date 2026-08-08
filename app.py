from flask import Flask, render_template, request
import sqlite3
from timetable import generate_timetable

app = Flask(__name__)


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

    print("Classes:", classes)
    print("Subjects:", subjects)
    print("Teachers:", teachers)
    print("Classrooms:", classrooms)

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


# ---------------- MIGRATION (temporary) ----------------

@app.route("/run-migration")
def run_migration():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE teachers ADD COLUMN password TEXT")
        conn.commit()
        result = "Password column added successfully!"
    except sqlite3.OperationalError as e:
        result = f"Already exists or error: {e}"

    conn.close()
    return result


    # ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)