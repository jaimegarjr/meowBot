#!/bin/bash

# Export requirements.txt
poetry export --without-hashes -f requirements.txt -o requirements.txt

# Build the Docker image
docker build -t gcr.io/meowbot-448505/meow-bot:latest .
