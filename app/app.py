
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash
from cms import fetch_doc

try:
    import markdown
    def md_to_html(text): return markdown.markdown(text, extensions=["fenced_code","tables"])
except Exception:
    def md_to_html(text): return None  # fallback to raw

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

if not os.path.exists(DB_NAME):
    init_db()
    create_user("woodstone", "threefold-zes", role="admin")
    print("✅ Admin user created: username='woodstone', password='threefold-zes'")

@app.route("/")
def home():
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
            return redirect(url_for("home"))
    return "❌ Login failed. <a href='/connect'>Try again</a>"

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

@app.route("/docs/<slug>")
def docs(slug):
    # Try Hygraph (GraphCMS) first
    record = fetch_doc(slug)
    if record:
        title = record.get("title") or slug
        body = record.get("body") or ""
        md_html = md_to_html(body)
        return render_template("doc.html", title=title, md_html=md_html, raw_md=body)
    # Fallback to local file (pages-clean)
    mapping = {
        "golden-bible": "golden_bible.md",
        "ruetli-commonwealth-declaration": "ruetli_commonwealth_declaration.md",
        "foundation-of-relationships": "foundation_of_relationships.md",
    }
    filename = mapping.get(slug)
    if filename:
        try:
            with open(os.path.join(os.path.dirname(__file__), "..", "pages-clean", filename), "r", encoding="utf-8") as f:
                body = f.read()
            md_html = md_to_html(body)
            title = slug.replace("-", " ").title()
            return render_template("doc.html", title=title, md_html=md_html, raw_md=body)
        except FileNotFoundError:
            return "Document not found", 404
    return "Unknown document", 404

# Serve static sacred markdown directly if needed
@app.route("/static/<path:filename>")
def static_passthrough(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "static"), filename)

if __name__ == "__main__":
    app.run(debug=True)
