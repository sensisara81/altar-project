
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = "supersecretkey"
DB_NAME = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    schema = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('tutor','visitor','admin')) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        body TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        author_id INTEGER,
        FOREIGN KEY(author_id) REFERENCES users(id)
    );
    '''
    conn = get_db_connection()
    conn.executescript(schema)
    conn.commit()
    conn.close()

def create_user(username,password,role="visitor"):
    conn = get_db_connection()
    conn.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",(username,password,role))
    conn.commit()
    conn.close()

# --- INIT DB AND CREATE FIRST ADMIN ---
if not os.path.exists(DB_NAME):
    init_db()
    create_user("woodstone", "threefold-zes", role="admin")
    print("✅ Admin user created: username='woodstone', password='threefold-zes'")

@app.route("/")
def index():
    return "Euystacio Portal is live. Login at /login"
