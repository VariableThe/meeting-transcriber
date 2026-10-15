#!/bin/bash
set -e
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo ""
echo "Starting Meeting Transcriber on http://localhost:5001"
python app.py
