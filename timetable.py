import sqlite3
import random
from datetime import datetime

def generate_timetable():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT class_name, subject_name, teacher_name, room_name FROM assignments")
    all_assignments = cursor.fetchall()

    today_date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT teacher_name FROM attendance WHERE date = ? AND status = 'absent'", (today_date,))
    absent_teachers = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT teacher_name FROM teachers")
    all_teachers = [row[0] for row in cursor.fetchall()]

    conn.close()

    today_name = datetime.now().strftime("%A")

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    slots = [
        "12:00 - 12:55",
        "12:55 - 1:50",
        "2:00 - 2:25 (BREAK)",
        "2:25 - 3:20",
        "3:20 - 4:25"
    ]

    # Group assignments by class_name (FY, SY, TY, etc.)
    grouped = {}
    for a in all_assignments:
        grouped.setdefault(a[0], []).append(list(a))

    for class_name in grouped:
        random.shuffle(grouped[class_name])

    # Rotating pointer for each class, so we cycle through its assignments
    pointers = {class_name: 0 for class_name in grouped}

    # Track which teacher is already busy on a given (day, slot)
    occupied = {}  # key: (day, slot) -> set of teacher_names

    # Build empty timetable structure for every class
    all_timetables = {}
    for class_name in grouped:
        timetable = {}
        for day in days:
            timetable[day] = {}
            for slot in slots:
                if "BREAK" in slot:
                    timetable[day][slot] = ("BREAK", "", "", "")
                else:
                    timetable[day][slot] = None
        all_timetables[class_name] = timetable

    # Fill slots day by day, so conflict-checking works across all classes together
    for day in days:
        for slot in slots:
            if "BREAK" in slot:
                continue

            occupied.setdefault((day, slot), set())

            for class_name, assignments in grouped.items():
                if not assignments:
                    continue

                total = len(assignments)
                tries = 0
                assigned = False

                while tries < total:
                    idx = pointers[class_name] % total
                    entry = list(assignments[idx])
                    pointers[class_name] += 1
                    tries += 1

                    teacher_name = entry[2]

                    # Handle today's absentees -> find substitute
                    if day == today_name and teacher_name in absent_teachers:
                        available_subs = [
                            t for t in all_teachers
                            if t not in absent_teachers
                            and t not in occupied[(day, slot)]
                        ]
                        if available_subs:
                            substitute = random.choice(available_subs)
                            entry[2] = substitute + " (Substitute)"
                            occupied[(day, slot)].add(substitute)
                            all_timetables[class_name][day][slot] = tuple(entry)
                            assigned = True
                            break
                        else:
                            continue  # no substitute free, try next assignment

                    # Normal case: check if this teacher is already busy this slot
                    if teacher_name in occupied[(day, slot)]:
                        continue  # conflict, try next assignment in the list

                    occupied[(day, slot)].add(teacher_name)
                    all_timetables[class_name][day][slot] = tuple(entry)
                    assigned = True
                    break

                if not assigned:
                    all_timetables[class_name][day][slot] = ("No Teacher Available", "", "", "")

    return all_timetables