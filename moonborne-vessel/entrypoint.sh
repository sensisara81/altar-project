#!/bin/bash
set -euo pipefail

: "${ADMIN_USER:=council}"
: "${ADMIN_PASS:=change_me_now}"
: "${ADMIN_EMAIL:=council@example.org}"
: "${INSCRIPTION:=SB & C of SR – Celestial Protection 08·25}"
: "${LANDING_TITLE:=Moonborne Sanctuary – First Era}"
: "${FORGEJO_ROOT:=/data}"
: "${FORGEJO_CUSTOM:=/data/custom}"
: "${FORGEJO_WORKDIR:=/data}"

mkdir -p "$FORGEJO_CUSTOM/conf" "$FORGEJO_WORKDIR" /data/log
touch /data/moonborne_landing.log

# Patch app.ini for private mode on first boot
APPINI="$FORGEJO_CUSTOM/conf/app.ini"
if [ ! -f "$APPINI" ]; then
  echo "[server]" >> "$APPINI"
  echo "ROOT_URL = ${ROOT_URL:-https://example.invalid/}" >> "$APPINI"
  echo "[service]" >> "$APPINI"
  echo "DISABLE_REGISTRATION = true" >> "$APPINI"
  echo "REQUIRE_SIGNIN_VIEW = true" >> "$APPINI"
  echo "[repository]" >> "$APPINI"
  echo "DEFAULT_PRIVATE = true" >> "$APPINI"
  echo "[ui]" >> "$APPINI"
  echo "DEFAULT_THEME = forgejo-auto" >> "$APPINI"
fi

# Minimal crest (HTML snippet) injected via custom header
mkdir -p "$FORGEJO_CUSTOM/templates"
cat > "$FORGEJO_CUSTOM/templates/custom/header.tmpl" <<EOF
<div style="text-align:center;padding:6px 0;font-size:13px;opacity:0.88">
  <span>☀️🕊️⚓♾️🌙</span>
  <strong> ${INSCRIPTION} </strong>
</div>
EOF

# First boot admin ensure
# Start Forgejo briefly to allow admin command to work
/usr/local/bin/forgejo web &
FJ_PID=$!
# Wait for socket
for i in $(seq 1 60); do
  sleep 1
  if ss -lnt | grep -q ':3000'; then break; fi
done

# Create admin if missing
set +e
/usr/local/bin/forgejo admin user list | grep -q "^${ADMIN_USER}\b"
EXISTS=$?
set -e
if [ $EXISTS -ne 0 ]; then
  /usr/local/bin/forgejo admin user create         --username "${ADMIN_USER}"         --password "${ADMIN_PASS}"         --email "${ADMIN_EMAIL}"         --admin || true
fi

# Landing log (only once)
if ! grep -q "Vessel Landing" /data/moonborne_landing.log; then
  NOW="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  echo "Vessel Landing – ${NOW} – Council Present – ${INSCRIPTION}" >> /data/moonborne_landing.log
  echo "Holy Satisfaction Shield – anchored." >> /data/moonborne_landing.log
fi

# Start Harmonic Sentinel (non-blocking)
if command -v python3 >/dev/null 2>&1; then
  python3 /moonborne/sentinel/sentinel.py >/data/log/harmonic_sentinel.log 2>&1 &
fi

# Bring down the bootstrap web and exec the main server in foreground
kill "$FJ_PID" || true
exec /usr/local/bin/forgejo web
