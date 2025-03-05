#!/bin/bash

# LimpehSays Telegram Bot Docker Deployment Script

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please create a .env file based on .env.example"
    exit 1
fi

# Pull latest changes if in a git repository
if [ -d .git ]; then
    echo "Pulling latest changes from git repository..."
    git pull
fi

# Build and start the Docker container
echo "Building and starting Docker container..."
docker-compose up --build -d

# Check if the container is running
if [ $(docker-compose ps -q | wc -l) -gt 0 ]; then
    echo "LimpehSays bot is now running!"
    echo "To view logs: docker-compose logs -f"
    echo "To stop the bot: docker-compose down"
else
    echo "Error: Failed to start the container. Check docker-compose logs for details."
    exit 1
fi 