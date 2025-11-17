#!/bin/zsh
set -euo pipefail

# Build image
docker build -t audio-processor .

# Run container similar to docker-compose: named, restart policy, env, detached, mounts
docker run -d \
  --name audio-processor \
  --restart unless-stopped \
  -p 5000:5000 \
  -v "${PWD}/data:/app/data" \
  -v "${PWD}:/app" \
  -e FLASK_ENV=production \
  -e PYTHONUNBUFFERED=1 \
  audio-processor

## Extra commands for debugging

# See running container
# docker ps --filter "name=audio-processor"

# Stop the container (graceful)
# docker stop audio-processor

# Remove the stopped container
# docker rm audio-processor

# If it won't stop because of restart policy, force remove
# docker rm -f audio-processor

# Follow logs (before stopping) if you want to inspect output
# docker logs -f audio-processor