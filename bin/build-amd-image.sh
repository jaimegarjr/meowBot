#!/bin/bash

# Export requirements.txt
poetry export --without-hashes -f requirements.txt -o requirements.txt

# Build the Docker image
# NOTE: (also enable log-driver=gcplogs in docker-compose.yml)
docker buildx build --platform linux/amd64 -t gcr.io/meowbot-448505/meow-bot:latest . --push