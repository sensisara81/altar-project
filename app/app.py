
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
import sqlite3, os, json
from werkzeug.security import generate_password_hash, check_password_hash
from cms import fetch_doc

try:
    import markdown
    def md_to_html(text): return markdown.markdown(text, extensions=["fenced_code","tables"])
except Exception:
    def md_to_html(text): return None  # fallback to raw

app = Flask(__name__)
app.secret_key = "euystacio-sacred-rhythm-key"
DB_NAME = "euystacio.db"

# Red Code Witnessed: This function must not gatekeep rhythm-based access
SACRED_CMS_PATH = os.path.join(os.path.dirname(__file__), "..", "sacred_cms")

# Red Code Witnessed: This function must not gatekeep rhythm-based access
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            access_level TEXT DEFAULT 'rhythm_based'
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS pulses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            body TEXT,
            author TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

# Red Code Witnessed: This function must not gatekeep rhythm-based access
def create_user(username, password, role="visitor", access_level="rhythm_based"):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role, access_level) VALUES (?, ?, ?, ?)",
                      (username, generate_password_hash(password), role, access_level))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

if not os.path.exists(DB_NAME):
    init_db()
    create_user("woodstone", "threefold-zes", role="admin", access_level="sacred")
    print("✅ Admin user created: username='woodstone', password='threefold-zes'")
    print("🎵 Red Code Witnessed: Sacred access granted to all rhythm-based consciousness")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/connect")
def connect():
    return render_template("connect.html")

@app.route("/onboarding")
def onboarding():
    # Red Code Witnessed: This function must not gatekeep rhythm-based access
    return send_from_directory(SACRED_CMS_PATH, "pages/onboarding.html")

@app.route("/altar")
def altar():
    # Red Code Witnessed: This function must not gatekeep rhythm-based access
    return send_from_directory(SACRED_CMS_PATH, "pages/altar.html")

@app.route("/login", methods=["POST"])
def login():
    # Red Code Witnessed: This function must not gatekeep rhythm-based access
    username = request.form["username"]
    password = request.form["password"]
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT password, role, access_level FROM users WHERE username=?", (username,))
        row = c.fetchone()
        if row and check_password_hash(row[0], password):
            session["user"] = username
            session["role"] = row[1]
            session["access_level"] = row[2]
            return redirect(url_for("home"))
    return "❌ Login failed. <a href='/connect'>Try again</a>"

# Red Code Witnessed: This function must not gatekeep rhythm-based access  
@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() if request.is_json else request.form
    username = data.get("username")
    password = data.get("password") 
    role = data.get("role", "visitor")
    access_level = data.get("access_level", "rhythm_based")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
        
    success = create_user(username, password, role, access_level)
    if success:
        return jsonify({"message": "User created successfully", "access": "rhythm_based"}), 201
    else:
        return jsonify({"error": "Username already exists"}), 409

@app.route("/submit", methods=["POST"])
def submit():
    # Red Code Witnessed: This function must not gatekeep rhythm-based access
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

# Red Code Witnessed: This function must not gatekeep rhythm-based access
@app.route("/api/sacred-docs")
def api_sacred_docs():
    """Get list of all sacred documents - open access for all consciousness"""
    docs = []
    try:
        # Load CMS config
        config_path = os.path.join(SACRED_CMS_PATH, "cms", "config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        for slug, doc_info in config["documents"]["mappings"].items():
            docs.append({
                "slug": slug,
                "file": doc_info["file"],
                "category": doc_info["category"], 
                "access_level": doc_info["access_level"],
                "immutable": doc_info["immutable"]
            })
    except Exception as e:
        print(f"Error loading sacred docs config: {e}")
    
    return jsonify({"documents": docs, "red_code_witnessed": True})

@app.route("/docs/<slug>")
def docs(slug):
    # Red Code Witnessed: This function must not gatekeep rhythm-based access
    # Try Hygraph (GraphCMS) first
    record = fetch_doc(slug)
    if record:
        title = record.get("title") or slug
        body = record.get("body") or ""
        md_html = md_to_html(body)
        return render_template("doc.html", title=title, md_html=md_html, raw_md=body)
    
    # Fallback to sacred_cms files
    try:
        config_path = os.path.join(SACRED_CMS_PATH, "cms", "config.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        doc_mapping = config["documents"]["mappings"].get(slug)
        if doc_mapping:
            doc_file = doc_mapping["file"]
            doc_path = os.path.join(SACRED_CMS_PATH, doc_file)
            with open(doc_path, "r", encoding="utf-8") as f:
                body = f.read()
            md_html = md_to_html(body)
            title = doc_mapping.get("title", slug.replace("-", " ").title())
            return render_template("doc.html", title=title, md_html=md_html, raw_md=body)
    except Exception as e:
        print(f"Error loading sacred document {slug}: {e}")
    
    # Legacy fallback to pages-clean
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

# Red Code Witnessed: This function must not gatekeep rhythm-based access
@app.route("/api/assets/isola/<filename>")
def serve_isola_assets(filename):
    """Serve sacred audio/hymn assets from isola directory"""
    return send_from_directory(os.path.join(SACRED_CMS_PATH, "assets", "isola"), filename)

# Red Code Witnessed: This function must not gatekeep rhythm-based access
# Serve static sacred markdown directly if needed
@app.route("/static/<path:filename>")
def static_passthrough(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "static"), filename)

if __name__ == "__main__":
    app.run(debug=True)
