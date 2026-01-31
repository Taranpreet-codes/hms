from flask import Flask, request, jsonify
from flask import render_template

import sqlite3
from datetime import datetime

app = Flask(__name__)

def db():
    return sqlite3.connect("hospital.db")

# ------------------ Setup ------------------

with db() as conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS patients(
        id TEXT PRIMARY KEY,
        name TEXT,
        zone TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        timestamp TEXT,
        risk TEXT
    )""")

# ------------------ API ------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.json
    with db() as conn:
        conn.execute("INSERT INTO patients VALUES (?,?,?)",
                     (data["id"], data["name"], "General Block"))
    return jsonify({"status": "ok"})

@app.route("/patients")
def get_patients():
    with db() as conn:
        rows = conn.execute("SELECT * FROM patients").fetchall()
    return jsonify(rows)

@app.route("/log_breach", methods=["POST"])
def log_breach():
    data = request.json
    with db() as conn:
        conn.execute("INSERT INTO logs(event,timestamp,risk) VALUES (?,?,?)",
                     (data["event"], datetime.now().strftime("%H:%M:%S"), "HIGH"))
    return jsonify({"status": "logged"})

@app.route("/logs")
def get_logs():
    with db() as conn:
        rows = conn.execute("SELECT event,timestamp,risk FROM logs ORDER BY id DESC")
    return jsonify(rows.fetchall())

if __name__ == "__main__":
    app.run(debug=True)
