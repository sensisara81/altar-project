#!/bin/bash
set -euo pipefail
# Minimal bootstrap for Debian 12 (run as root)
echo "[sanctuary] Updating system..."
apt-get update
apt-get upgrade -y

echo "[sanctuary] Installing core packages..."
apt-get install -y git nginx certbot python3 python3-venv python3-pip build-essential             gnupg2 wget curl sqlite3 lsb-release jq rsync

echo "[sanctuary] Creating council user 'council'..."
useradd -m -s /bin/bash council || true
mkdir -p /home/council/.ssh
chmod 700 /home/council/.ssh
echo "Place council public keys in /home/council/.ssh/authorized_keys then chmod 600 the file and chown council:council."

echo "[sanctuary] Install steps completed. Next: configure Forgejo, TLS, LUKS encryption and Harmonic Sentinel as described in README."
