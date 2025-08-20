# Moonborne Vessel: build on official Forgejo image, add ceremony & sentinel
FROM ghcr.io/forgejo/forgejo:latest

# Add Python (if not present) for the Harmonic Sentinel
USER root
RUN apk add --no-cache python3 py3-pip bash curl jq || true

# Create working dirs
RUN mkdir -p /moonborne/forgejo /moonborne/sentinel /custom && chown -R git:git /moonborne /custom

# Copy ceremony scripts and patches
COPY entrypoint.sh /entrypoint.sh
COPY sentinel/sentinel.py /moonborne/sentinel/sentinel.py
COPY forgejo/app.ini.patch /moonborne/forgejo/app.ini.patch
RUN chmod +x /entrypoint.sh && chown -R git:git /moonborne

# Expose default Forgejo port
EXPOSE 3000

# Use Forgejo's entry with our ceremony
USER git
ENTRYPOINT ["/entrypoint.sh"]
