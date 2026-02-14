#!/bin/bash
set -e

echo "Configuring Docker Log Rotation..."

# Create logrotate configuration for Docker containers
cat <<EOF | sudo tee /etc/logrotate.d/docker-containers
/var/lib/docker/containers/*/*.log {
  rotate 7
  daily
  compress
  missingok
  delaycompress
  copytruncate
}
EOF

echo "Log rotation configured."
