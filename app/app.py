from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    return sqlite3.connect("hospital.db")

def update_doctor_status():
    now = datetime.now().strftime("%H:%M")
    with get_db() as conn:
        doctors = conn.execute(
            "SELECT id, shift_start, shift_end FROM doctors"
        ).fetchall()

        for doc_id, start, end in doctors:
            # Emergency doctor always active
            if doc_id == "DOC020":
                conn.execute(
                    "UPDATE doctors SET status='Available' WHERE id=?",
                    (doc_id,)
                )
                continue

            if start <= now <= end:
                conn.execute(
                    "UPDATE doctors SET status='Available' WHERE id=?",
                    (doc_id,)
                )
            else:
                conn.execute(
                    "UPDATE doctors SET status='Off Duty' WHERE id=?",
                    (doc_id,)
                )
        conn.commit()

def mark_busy_doctors():
    now = datetime.now().strftime("%H:%M")
    with get_db() as conn:
        rows = conn.execute(
            "SELECT doctor FROM appointments WHERE time=?",
            (now,)
        ).fetchall()

        for (doctor_name,) in rows:
            conn.execute(
                "UPDATE doctors SET status='Busy' WHERE name=?",
                (doctor_name,)
            )
        conn.commit()

# ---------- DB Setup & Initial Data ----------

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS patients(
            id TEXT PRIMARY KEY,
            name TEXT,
            zone TEXT,
            ward TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            timestamp TEXT,
            risk TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS appointments(
            patient TEXT,
            doctor TEXT,
            time TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS doctors(
            id TEXT PRIMARY KEY,
            name TEXT,
            specialization TEXT,
            shift_start TEXT,
            shift_end TEXT,
            phone TEXT,
            room TEXT,
            experience INTEGER,
            status TEXT
        )""")
        
        doctors_list = [
            ("DOC001","Dr. Anil Sharma","Cardiologist","09:00","14:00","9876543210","Room 101",12,"Available"),
            ("DOC002","Dr. Neha Verma","Dermatologist","10:00","16:00","9876501234","Room 102",8,"Available"),
            ("DOC003","Dr. Raj Malhotra","Neurologist","14:00","20:00","9988776655","Room 201",15,"Available"),
            ("DOC004","Dr. Priya Singh","Pediatrician","08:00","13:00","9123456780","Room 103",6,"Available"),
            ("DOC005","Dr. Karan Mehta","Orthopedic","15:00","21:00","9012345678","Room 202",10,"Available"),
            ("DOC006","Dr. Sana Khan","Gynecologist","09:00","14:00","9090909090","Room 104",9,"Available"),
            ("DOC007","Dr. Amit Patel","General Physician","08:00","18:00","8888777766","Room 105",14,"Available"),
            ("DOC008","Dr. Rohit Gupta","ENT Specialist","10:00","15:00","9871112222","Room 106",7,"Available"),
            ("DOC009","Dr. Pooja Joshi","Psychiatrist","12:00","18:00","9812345670","Room 203",11,"Available"),
            ("DOC010","Dr. Arjun Rao","Urologist","09:00","14:00","9823456712","Room 204",13,"Available"),
            ("DOC011","Dr. Kavita Nair","Oncologist","10:00","16:00","9834567890","Room 301",16,"Available"),
            ("DOC012","Dr. Suresh Iyer","Nephrologist","14:00","20:00","9845678901","Room 302",18,"Available"),
            ("DOC013","Dr. Mehul Jain","Gastroenterologist","08:00","13:00","9856789012","Room 205",9,"Available"),
            ("DOC014","Dr. Rina Kapoor","Ophthalmologist","09:00","15:00","9867890123","Room 107",10,"Available"),
            ("DOC015","Dr. Vikram Chauhan","Pulmonologist","12:00","18:00","9878901234","Room 303",14,"Available"),
            ("DOC016","Dr. Nisha Agarwal","Endocrinologist","10:00","16:00","9889012345","Room 206",12,"Available"),
            ("DOC017","Dr. Harpreet Kaur","Radiologist","08:00","14:00","9890123456","Room 401",11,"Available"),
            ("DOC018","Dr. Sanjay Bansal","Surgeon","14:00","22:00","9901234567","Operation Theatre",20,"Available"),
            ("DOC019","Dr. Ayesha Mir","Anesthesiologist","09:00","17:00","9912345678","OT Wing",13,"Available"),
            ("DOC020","Dr. Rakesh Yadav","Emergency Physician","00:00","23:59","9923456789","Emergency Ward",17,"Available")
        ]
    
        
        patients_list = [
        ("P001","Aman Kumar","Block A","ICU"),
        ("P002","Riya Sharma","Block B","GENERAL"),
        ("P003","Mohit Verma","Block C","GENERAL"),
        ("P004","Neha Singh","Block A","ICU"),
        ("P005","Arjun Patel","Block B","GENERAL"),
        ("P006","Simran Kaur","Block C","ICU"),
        ("P007","Rahul Mehta","Block A","GENERAL"),
        ("P008","Pooja Joshi","Block B","GENERAL"),
        ("P009","Karan Malhotra","Block C","ICU"),
        ("P010","Anjali Gupta","Block A","GENERAL"),

        ("P011","Rohit Khanna","Block B","GENERAL"),
        ("P012","Nisha Arora","Block C","ICU"),
        ("P013","Sahil Jain","Block A","GENERAL"),
        ("P014","Kavya Bansal","Block B","GENERAL"),
        ("P015","Vikas Yadav","Block C","ICU"),
        ("P016","Isha Malhotra","Block A","GENERAL"),
        ("P017","Harsh Verma","Block B","GENERAL"),
        ("P018","Meenal Gupta","Block C","ICU"),
        ("P019","Aditya Rana","Block A","GENERAL"),
        ("P020","Sneha Kapoor","Block B","GENERAL"),

        ("P021","Manish Sethi","Block C","ICU"),
        ("P022","Tanya Chawla","Block A","GENERAL"),
        ("P023","Rajat Aggarwal","Block B","GENERAL"),
        ("P024","Pallavi Mishra","Block C","ICU"),
        ("P025","Deepak Joshi","Block A","GENERAL"),
        ("P026","Shreya Nair","Block B","GENERAL"),
        ("P027","Amit Saxena","Block C","ICU"),
        ("P028","Rashmi Thakur","Block A","GENERAL"),
        ("P029","Varun Chopra","Block B","GENERAL"),
        ("P030","Kriti Mehta","Block C","ICU"),

        ("P031","Suresh Rao","Block A","GENERAL"),
        ("P032","Anita Iyer","Block B","ICU"),
        ("P033","Pranav Kulkarni","Block C","GENERAL"),
        ("P034","Pinky Sharma","Block A","GENERAL"),
        ("P035","Naveen Joshi","Block B","ICU"),
        ("P036","Bhavya Jain","Block C","GENERAL"),
        ("P037","Rakesh Pandey","Block A","GENERAL"),
        ("P038","Sonali Deshpande","Block B","ICU"),
        ("P039","Yash Kapoor","Block C","GENERAL"),
        ("P040","Komal Arora","Block A","GENERAL"),

        ("P041","Dinesh Rawat","Block B","ICU"),
        ("P042","Preeti Malhotra","Block C","GENERAL"),
        ("P043","Akhil Bhatia","Block A","GENERAL"),
        ("P044","Neetu Verma","Block B","ICU"),
        ("P045","Rohan Choudhary","Block C","GENERAL"),
        ("P046","Poonam Saxena","Block A","GENERAL"),
        ("P047","Tarun Mishra","Block B","GENERAL"),
        ("P048","Sunita Rani","Block C","ICU"),
        ("P049","Kunal Sood","Block A","GENERAL"),
        ("P050","Rekha Chauhan","Block B","GENERAL")
        ]

        c.executemany("INSERT OR REPLACE INTO doctors VALUES (?,?,?,?,?,?,?,?,?)", doctors_list)

        c.executemany(
                    "INSERT OR REPLACE INTO patients VALUES (?,?,?,?)",
                    patients_list
                )
        conn.commit()
        

# Run Initialization
init_db()


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/doctors")
def get_doctors(): # Renamed to avoid clashing with the 'doctors' list variable
    update_doctor_status()
    mark_busy_doctors()
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM doctors").fetchall()
    return jsonify(rows)

@app.route("/patients")
def get_patients():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM patients").fetchall()
    return jsonify(rows)

@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.json
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO patients VALUES (?,?,?,?)",
            (data["id"], data["name"], "General Block", data["ward"])
        )
        conn.commit()
    return jsonify({"status": "saved"})

@app.route("/logs")
def get_logs():
    with get_db() as conn:
        # Added .fetchall() - critical for returning data
        rows = conn.execute("SELECT event, timestamp, risk FROM logs ORDER BY id DESC").fetchall()
    return jsonify(rows)

# --- Security & Audit Logging ---

@app.route("/log_breach", methods=["POST"])
def log_breach():
    data = request.json
    with get_db() as conn:
        conn.execute(
            "INSERT INTO logs(event,timestamp,risk) VALUES (?,?,?)",
            (data["event"], datetime.now().strftime("%H:%M:%S"), "HIGH")
        )
        conn.commit()
    return jsonify({"status": "logged"})
@app.route("/emergency_stats")
def emergency_stats():
    with get_db() as conn:
        icu = conn.execute("SELECT COUNT(*) FROM patients WHERE ward='ICU'").fetchone()[0]
        general = conn.execute("SELECT COUNT(*) FROM patients WHERE ward='GENERAL'").fetchone()[0]

    return jsonify({
        "icu": icu,
        "general": general,
        "total": icu + general
    })

@app.route("/log_emergency", methods=["POST"])
def log_emergency():
    with get_db() as conn:
        conn.execute(
            "INSERT INTO logs(event, timestamp, risk) VALUES (?, ?, ?)",
            ("EMERGENCY PROTOCOL ACTIVATED", datetime.now().strftime("%H:%M:%S"), "CRITICAL")
        )
        conn.commit()
    return jsonify({"status":"logged"})
@app.route("/patients/general")
def get_general_patients():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM patients WHERE ward='GENERAL'"
        ).fetchall()
    return jsonify(rows)
@app.route("/patients/icu")
def get_icu_patients():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM patients WHERE ward='ICU'"
        ).fetchall()
    return jsonify(rows)

# ==============================
# 🧑‍⚕️ Appointments
# ==============================
@app.route("/add_appointment", methods=["POST"])
def add_appointment():
    data = request.json
    with get_db() as conn:
        conn.execute(
            "INSERT INTO appointments VALUES (?,?,?)",
            (data["patient"], data["doctor"], data["time"])
        )
        conn.commit()
    return jsonify({"status":"ok"})

@app.route("/appointments")
def get_appointments():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM appointments ORDER BY time").fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)