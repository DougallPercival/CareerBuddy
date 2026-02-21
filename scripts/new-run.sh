#!/usr/bin/env bash

set -e  # Exit immediately if a command fails

echo "Tearing down database..."
./db-teardown.sh

echo "Rebuilding database..."
./db-build.sh

echo "Running raw pipeline loads..."
cd ../pipeline

../../.venv/bin/python -m load_raw_stc_noc \
    ../../data/noc_2021_version_1.0_-_classification_structure.csv

../../.venv/bin/python -m load_raw_stc_income \
    ../../data/98100452-eng/98100452.csv

echo "New run completed successfully."
