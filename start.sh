#!/usr/bin/env bash
# start.sh
#
# Create a Python 3.12 virtual environment, install dependencies, and run the app.

set -e

# Determine the directory of this script and navigate to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "textEditor312" ]; then
    python3.12 -m venv textEditor312
fi

# Activate virtual environment
source textEditor312/bin/activate

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
python run.py
