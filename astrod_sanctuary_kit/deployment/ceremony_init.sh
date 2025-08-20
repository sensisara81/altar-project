#!/bin/bash
set -euo pipefail
echo "[ceremony] Starting first-light ceremony (non-destructive)"
# Create necessary directories
mkdir -p /srv/forgejo /srv/astrod_kernel /etc/astrod /var/lib/harmonic_sentinel
chown -R council:council /srv/forgejo /srv/astrod_kernel /etc/astrod /var/lib/harmonic_sentinel || true
echo "[ceremony] Directories prepared. Place encrypted LUKS file at /srv/astrod_kernel/astrod_vault.img and follow README to unlock and extract ASTRODEEPAURA seed inside the vault."

echo "[ceremony] Installing systemd services for Harmonic Sentinel and Forgejo..."
cp /root/astrod_sanctuary_kit/systemd/harmonic_sentinel.service /etc/systemd/system/
cp /root/astrod_sanctuary_kit/systemd/forgejo.service /etc/systemd/system/

systemctl daemon-reload
systemctl enable harmonic_sentinel.service
systemctl enable forgejo.service

echo "[ceremony] Services installed and enabled. Use 'systemctl start harmonic_sentinel' and 'systemctl start forgejo' to launch them now."
