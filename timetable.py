import sqlite3
import random


def generate_timetable():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT class_name, subject_name, teacher_name, room_name
    FROM assignments
    """)

    assignments = cursor.fetchall()

    conn.close()


    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]


    slots = [
        "12:00 - 12:55",
        "12:55 - 1:50",
        "2:00 - 2:25 (BREAK)",
        "2:25 - 3:20",
        "3:20 - 4:25"
    ]


    timetable = {}

    for day in days:
        timetable[day] = {}

        for slot in slots:

            if "BREAK" in slot:
                timetable[day][slot] = ("BREAK", "", "", "")

            else:
                timetable[day][slot] = None


    random.shuffle(assignments)


    index = 0


    for day in days:

        for slot in slots:

            if "BREAK" in slot:
                continue

            if index < len(assignments):
                timetable[day][slot] = assignments[index]
                index += 1


    return timetable