#!/bin/bash

# Simple script to run the backend server

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.deps_installed" ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    touch venv/.deps_installed
fi

# Run the Flask app
echo "Starting Flask server on http://localhost:5000"
python3 app.py

