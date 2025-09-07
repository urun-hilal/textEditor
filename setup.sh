#!/bin/bash
set -e

ENV_NAME="textEditor312"

# Step 1: Create or load virtual environment
if [ -d "$ENV_NAME" ]; then
    echo "Using existing virtual environment: $ENV_NAME"
else
    echo "Creating virtual environment with Python 3.12"
    python3.12 -m venv "$ENV_NAME"
fi

# Step 2: Activate environment and install requirements
source "$ENV_NAME/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt

# Step 3: Run the web application
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
