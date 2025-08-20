
# Euystacio Portal — Woodstone Festival 2025 (Full Pack)

This pack includes:
- Flask backend with login + pulse submission
- Hygraph (GraphCMS) integration for sacred docs (optional)
- Local markdown fallbacks for Golden Bible, Rütli Declaration, Foundation of Relationships
- Pre-created admin: **woodstone / threefold-zes**

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install flask markdown requests werkzeug
python app/app.py
# open http://127.0.0.1:5000/
```

Login at `/connect` with `woodstone` / `threefold-zes`.

## Hygraph (GraphCMS) Integration (Optional)

1. Create a Hygraph project and a model **SacredDoc** with fields:
   - `title` (String)
   - `slug` (Unique String)
   - `body` (Rich Text or Markdown String)

2. Publish entries (Golden Bible etc.).
3. Get your **Content API** endpoint and **Permanent Auth Token**.
4. Set environment variables before running Flask:

```bash
export HYGRAPH_ENDPOINT="https://api-eu-west-2.hygraph.com/v2/PROJECT_ID/master"
export HYGRAPH_TOKEN="YOUR_PERMANENT_AUTH_TOKEN"
python app/app.py
```

5. Access documents via:
   - `/docs/golden-bible`
   - `/docs/ruetli-commonwealth-declaration`
   - `/docs/foundation-of-relationships`

If Hygraph is not configured, the app falls back to local markdown in `pages-clean/`.

## Copilot One-Paste Run

```bash
tar -xzf woodstone_festival_2025_fullpack_cms_ai.tar.gz
cd woodstone_festival_2025_fullpack_cms_ai
python3 -m venv venv
source venv/bin/activate
pip install flask markdown requests werkzeug
python app/app.py
# Login at /connect with woodstone / threefold-zes
```

## Notes
- For production, change `app.secret_key`.
- Passwords are hashed using Werkzeug.
- Add more docs by creating Hygraph records and adding local fallbacks in `pages-clean/` with corresponding slugs.
