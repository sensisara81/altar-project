#!/bin/bash
set -e

echo "🚀 Moonborne Vessel Limo Landing - Starting..."

# Unpack contents if not already unpacked
if [ -f moonborne_vessel_render_kit.tar.gz ]; then
    echo "📦 Extracting render kit..."
    tar -xzf moonborne_vessel_render_kit.tar.gz
fi

# Initialize git and push
echo "🔑 Setting up SSH key for moon_rise..."
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/moon_rise

echo "📂 Initializing Git repository..."
git init
git remote add origin git@github.com:bioarchitettura/moonborne-vessel.git
git branch -M main
git add .
git commit -m 'Moonborne Vessel Limo Landing - Initial Commit'
git push -u origin main --force

# Trigger Render deploy
echo "🌌 Triggering Render deployment..."
curl -X POST "https://api.render.com/deploy/srv-d2fdavjuibrs739qi200?key=s-fNLZ6PMkE"

echo "✨ Deployment triggered. The Vessel is en route to the Landing Zone."
