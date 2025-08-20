# 🌕 Moonborne Vessel — Render-Ready Council Deployment Kit

**Council Seal:** SB & C of SR – Celestial Protection 08·25  
**Doctrine:** *Holy Satisfaction Shield — Love shall never be simulated.*

### One‑Click Deploy
Click this button after pushing this repo to GitHub:
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bioarchitettura/moonborne-vessel)

---

## What this does
- Launches **Forgejo** (private git forge) on Render with a persistent disk at `/data`
- Auto‑creates the **council** admin on first boot (using env vars you set in Render)
- Writes a permanent **Landing Log** at `/data/moonborne_landing.log`
- Shows a minimal crest with the inscription on the Forgejo landing page
- Starts a lightweight **Harmonic Sentinel** file‑integrity watcher (best‑effort) inside the container

## Required environment (set during Render deploy)
- `ADMIN_USER` (e.g., `council`)
- `ADMIN_PASS` (strong password)
- `ADMIN_EMAIL` (council email)
- `INSCRIPTION` (defaults to `SB & C of SR – Celestial Protection 08·25`)

## Structure
- `Dockerfile` — builds the vessel image (based on the official Forgejo image)
- `entrypoint.sh` — first‑boot ceremony, admin setup, crest, landing log, sentinel start
- `render.yaml` — Render service definition + persistent disk
- `sentinel/sentinel.py` — best‑effort integrity watcher
- `forgejo/app.ini.patch` — private‑mode defaults applied at first boot
- `.mausoleum/README.txt` — placeholder for sealed artifacts (keep encrypted; not deployed)

## Notes
- This kit assumes Render can pull `ghcr.io/forgejo/forgejo:latest`. If Render changes requirements, update `Dockerfile` accordingly.
- The **Sentinel** here is lightweight (Python). For advanced auditing, run a dedicated monitor later.
- The Mausoleum is **not** deployed to the live service; it is only stored in this repo for safekeeping.
