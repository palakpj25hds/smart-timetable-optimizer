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
        "2:00 - 2:25",
        "2:25 - 3:20",
        "3:20 - 4:25"
    ]

    # SY DS ka Exact SIES Schedule Grid
    sy_fixed_grid = {
        "Monday": {"12:00 - 12:55": "EC(AEC)", "12:55 - 1:50": "DSA", "2:25 - 3:20": "FML", "3:20 - 4:25": "DSA"},
        "Tuesday": {"12:00 - 12:55": "DBMS", "12:55 - 1:50": "FML", "2:25 - 3:20": "SI", "3:20 - 4:25": "CC"},
        "Wednesday": {"12:00 - 12:55": "OE (PD/Adv/SMM)", "12:55 - 1:50": "EC(AEC)", "2:25 - 3:20": "DBMS (PRAC)", "3:20 - 4:25": "DBMS (PRAC)"},
        "Thursday": {"12:00 - 12:55": "OE (PD/Adv/SMM)", "12:55 - 1:50": "DSA", "2:25 - 3:20": "DSA (PRAC)", "3:20 - 4:25": "DSA (PRAC)"},
        "Friday": {"12:00 - 12:55": "FML (PRAC)", "12:55 - 1:50": "FML (PRAC)", "2:25 - 3:20": "SI", "3:20 - 4:25": "BLANK"},
        "Saturday": {"12:00 - 12:55": "SI (PRAC)", "12:55 - 1:50": "SI (PRAC)", "2:25 - 3:20": "SI", "3:20 - 4:25": "FML"}
    }

    grouped = {}
    for a in all_assignments:
        grouped.setdefault(a[0], []).append(list(a))

    # Single global tracker across ALL classes to avoid teacher collisions
    occupied = {}
    all_timetables = {}

    # Sort classes so SY is processed first to reserve its fixed timetable slots
    class_order = sorted(grouped.keys(), key=lambda c: 0 if "SY" in c.upper() else 1)

    for class_name in class_order:
        assignments = grouped[class_name]
        timetable = {day: {slot: ("BREAK", "", "", "") if "2:00 - 2:25" in slot else None for slot in slots} for day in days}
        subject_map = {entry[1].strip().upper(): entry for entry in assignments}

        # --- 1. SY DS TIMETABLE (SIES EXACT GRID) ---
        if "SY" in class_name.upper():
            for day in days:
                for slot in slots:
                    if "2:00 - 2:25" in slot:
                        continue

                    target = sy_fixed_grid.get(day, {}).get(slot, "BLANK")
                    if target == "BLANK":
                        timetable[day][slot] = ("BLANK / Free", "", "", "")
                        continue

                    matched_entry = None
                    for subj_key, entry_val in subject_map.items():
                        if target.upper() in subj_key or subj_key in target.upper():
                            matched_entry = list(entry_val)
                            break

                    if matched_entry:
                        teacher_name = matched_entry[2]
                        occupied.setdefault((day, slot), set())

                        # Substitute handling if absent
                        if day == today_name and teacher_name in absent_teachers:
                            free_subs = [t for t in all_teachers if t not in absent_teachers and t not in occupied[(day, slot)]]
                            if free_subs:
                                sub = random.choice(free_subs)
                                matched_entry[2] = sub + " (Substitute)"
                                occupied[(day, slot)].add(sub)
                            else:
                                matched_entry[2] = teacher_name + " (Absent)"
                        else:
                            occupied[(day, slot)].add(teacher_name)

                        timetable[day][slot] = tuple(matched_entry)
                    else:
                        # Fallback mapping if subject entry is not saved in DB yet
                        timetable[day][slot] = (class_name, target, "Priya Nair", "CR-03")
                        occupied.setdefault((day, slot), set()).add("Priya Nair")

        # --- 2. FY DS & TY DS TIMETABLE (DYNAMIC WITH CLASH PREVENTION) ---
        else:
            assign_pool = list(assignments)
            random.shuffle(assign_pool)
            pool_idx = 0

            for day in days:
                for slot in slots:
                    if "2:00 - 2:25" in slot:
                        continue

                    occupied.setdefault((day, slot), set())
                    assigned = False
                    attempts = 0
                    total_assigns = len(assign_pool)

                    while attempts < total_assigns:
                        entry = list(assign_pool[pool_idx % total_assigns])
                        teacher_name = entry[2]
                        pool_idx += 1
                        attempts += 1

                        # Skip this teacher if they are ALREADY teaching in SY or another class at this slot
                        if teacher_name in occupied[(day, slot)]:
                            continue

                        # Handle today's absentees
                        if day == today_name and teacher_name in absent_teachers:
                            free_subs = [t for t in all_teachers if t not in absent_teachers and t not in occupied[(day, slot)]]
                            if free_subs:
                                sub = random.choice(free_subs)
                                entry[2] = sub + " (Substitute)"
                                occupied[(day, slot)].add(sub)
                                timetable[day][slot] = tuple(entry)
                                assigned = True
                                break
                            else:
                                continue

                        # Normal Assignment
                        occupied[(day, slot)].add(teacher_name)
                        timetable[day][slot] = tuple(entry)
                        assigned = True
                        break

                    if not assigned:
                        timetable[day][slot] = ("Free / No Teacher", "", "", "")

        all_timetables[class_name] = timetable

    return all_timetables
