#!/usr/bin/env bash

set -e

# ==============================
# Configuration
# ==============================

CONTAINER_NAME="cb-pg-dev"
HOST_PORT="5434"
DATA_DIR="/home/cb-dev-data"
DB_NAME="cbdev"
DB_USER="postgres"

# ==============================
# Verify docker-compose.yml exists
# ==============================

if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found in current directory."
  echo "Please create it before running this script."
  exit 1
fi

# ==============================
# Prompt for password
# ==============================

read -s -p "Enter PostgreSQL password for user '$DB_USER': " DB_PASSWORD
echo

# ==============================
# Create data directory
# ==============================

echo "Creating data directory at $DATA_DIR..."
mkdir -p "$DATA_DIR"

echo "Setting ownership to UID 999 (postgres container user)..."
sudo chown -R 999:999 "$DATA_DIR"

# ==============================
# Create .env file
# ==============================

echo "Creating .env file..."
cat > .env <<EOF
POSTGRES_PASSWORD=$DB_PASSWORD
EOF

# ==============================
# Start container
# ==============================

echo "Starting PostgreSQL container..."
docker compose up -d

echo
echo "======================================"
echo "PostgreSQL is starting..."
echo
echo "Container name: ${CONTAINER_NAME}"
echo "Host: localhost"
echo "Port: ${HOST_PORT}"
echo "Database: ${DB_NAME}"
echo "User: ${DB_USER}"
echo "Data directory: ${DATA_DIR}"
echo "======================================"

echo
echo "Check status with:"
echo "  docker ps"
echo
echo "View logs with:"
echo "  docker logs -f ${CONTAINER_NAME}"
