#!/bin/bash

# Exit immediately if a command fails
set -e

# Database connection URL
DB_URL="postgres://postgres:postgres@localhost:5434/cbdev"

echo "Starting database setup..."

# Run schema creation script
echo "Running schemas.sql..."
psql "$DB_URL" -f schemas.sql

# Run raw tables
echo "Running src_ext_stc_income.sql..."
psql "$DB_URL" -f src_ext_stc_income.sql

echo "Running src_ext_stc_noc.sql..."
psql "$DB_URL" -f src_ext_stc_noc.sql

# Run staging tables
echo "Running stg_stc_income.sql..."
psql "$DB_URL" -f stg_stc_income.sql

echo "Running stg_stc_noc.sql..."
psql "$DB_URL" -f stg_stc_noc.sql

echo "Database setup completed successfully!"
