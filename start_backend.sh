#!/bin/bash
cd "$(dirname "$0")/backend"
source venv/bin/activate 2>/dev/null || {
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip3 install -q -r requirements.txt
}
echo "🚀 Starting backend server on http://localhost:5000"
echo "Press Ctrl+C to stop"
python3 app.py
