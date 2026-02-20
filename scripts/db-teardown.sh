#!/bin/bash

# Exit immediately if a command fails
set -e

# Database connection URL
DB_URL="postgres://postgres:postgres@localhost:5434/cbdev"

echo "Starting database teardown..."

# List of schemas to drop
SCHEMAS=("raw" "staging" "analytics" "serving")

for schema in "${SCHEMAS[@]}"; do
    echo "Dropping schema $schema..."
    psql "$DB_URL" -c "DROP SCHEMA IF EXISTS $schema CASCADE;"
done

echo "Database teardown completed successfully!"
