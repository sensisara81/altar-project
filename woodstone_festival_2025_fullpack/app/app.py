from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "euystacio-secret"

DB_NAME = "euystacio.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS pulses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            body TEXT,
            author TEXT
        )''')
        conn.commit()

def create_user(username, password, role="user"):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      (username, generate_password_hash(password), role))
            conn.commit()
        except sqlite3.IntegrityError:
            pass

# --- INIT DB ---
if not os.path.exists(DB_NAME):
    init_db()
    create_user("woodstone", "threefold-zes", role="admin")
    print("✅ Admin user created: username='woodstone', password='threefold-zes'")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connect")
def connect():
    return render_template("connect.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT password, role FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row and check_password_hash(row[0], password):
            session["user"] = username
            session["role"] = row[1]
            return redirect(url_for("index"))
    return "❌ Login failed"

@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect(url_for("connect"))
    title = request.form["title"]
    body = request.form["body"]
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO pulses (title, body, author) VALUES (?, ?, ?)", 
                  (title, body, session["user"]))
        conn.commit()
    return "✅ Pulse submitted! <a href='/'>Back</a>"

if __name__ == "__main__":
    app.run(debug=True)
