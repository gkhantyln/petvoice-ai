#!/bin/bash
# entrypoint.sh
# Docker entrypoint script

# Exit immediately if a command exits with a non-zero status
set -e

# Create necessary directories
mkdir -p uploads/sounds uploads/spectrograms logs

# Run database migrations if needed
# flask db upgrade

# Start the application
exec python run.py