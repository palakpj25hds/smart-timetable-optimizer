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

    grouped = {}
    for a in all_assignments:
        grouped.setdefault(a[0], []).append(list(a))

    occupied_teachers = {}
    occupied_rooms = {}

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

    for day in days:
        day_order = {}
        for class_name in grouped:
            shuffled = grouped[class_name][:]
            random.shuffle(shuffled)
            day_order[class_name] = shuffled

        pointers = {class_name: 0 for class_name in grouped}

        for slot in slots:
            if "BREAK" in slot:
                continue

            occupied_teachers.setdefault((day, slot), set())
            occupied_rooms.setdefault((day, slot), set())

            for class_name in grouped:
                assignments = day_order[class_name]
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
                    room_name = entry[3]

                    if day == today_name and teacher_name in absent_teachers:
                        available_subs = [
                            t for t in all_teachers
                            if t not in absent_teachers
                            and t not in occupied_teachers[(day, slot)]
                        ]
                        if available_subs and room_name not in occupied_rooms[(day, slot)]:
                            substitute = random.choice(available_subs)
                            entry[2] = substitute + " (Substitute)"
                            occupied_teachers[(day, slot)].add(substitute)
                            occupied_rooms[(day, slot)].add(room_name)
                            all_timetables[class_name][day][slot] = tuple(entry)
                            assigned = True
                            break
                        else:
                            continue

                    if teacher_name in occupied_teachers[(day, slot)]:
                        continue
                    if room_name in occupied_rooms[(day, slot)]:
                        continue

                    occupied_teachers[(day, slot)].add(teacher_name)
                    occupied_rooms[(day, slot)].add(room_name)
                    all_timetables[class_name][day][slot] = tuple(entry)
                    assigned = True
                    break

                if not assigned:
                    all_timetables[class_name][day][slot] = ("No Slot Available", "", "", "")

    def sort_key(class_name):
        if class_name.startswith("FY"):
            return 0
        elif class_name.startswith("SY"):
            return 1
        elif class_name.startswith("TY"):
            return 2
        else:
            return 3

    sorted_timetables = dict(sorted(all_timetables.items(), key=lambda x: sort_key(x[0])))

    return sorted_timetables