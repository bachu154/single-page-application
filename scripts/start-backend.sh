#!/bin/bash

echo "Starting HTML Search Engine Backend..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/../backend" || exit

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the backend
echo "Starting FastAPI server on http://localhost:8000"
echo "API Documentation available at http://localhost:8000/docs"
python main.py
