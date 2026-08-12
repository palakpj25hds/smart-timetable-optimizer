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
    CREATE TABLE IF NOT EXISTS attendance