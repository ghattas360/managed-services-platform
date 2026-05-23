#!/usr/bin/env bash
set -euo pipefail

# Create deploy user if missing
if ! id deploy &>/dev/null; then
  useradd -m -s /bin/bash deploy
  echo "deploy ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/deploy
  chmod 0440 /etc/sudoers.d/deploy
  echo "Created deploy user"
fi

# Base packages
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv curl jq

# Docker
if ! command -v docker &>/dev/null; then
  curl -fsSL https://get.docker.com | sh
  usermod -aG docker deploy
  echo "Installed Docker"
fi

# Docker Compose plugin
if ! docker compose version &>/dev/null 2>&1; then
  apt-get install -y -qq docker-compose-plugin
  echo "Installed docker compose plugin"
fi

# App directory
mkdir -p /opt/app
chown deploy:deploy /opt/app

# Systemd unit
cat > /etc/systemd/system/managed-app.service <<'EOF'
[Unit]
Description=Managed Services Platform
After=docker.service
Requires=docker.service

[Service]
User=deploy
Restart=always
RestartSec=5
ExecStartPre=-/usr/bin/docker stop managed-app
ExecStartPre=-/usr/bin/docker rm managed-app
ExecStart=/usr/bin/docker run --rm --name managed-app -p 8000:8000 \
  ghcr.io/ghattas360/managed-services-platform:latest
ExecStop=/usr/bin/docker stop managed-app

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable managed-app
echo "Provisioning complete."
