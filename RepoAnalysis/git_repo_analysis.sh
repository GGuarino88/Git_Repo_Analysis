#!/bin/bash

# Define variables
PROJECT_PATH="/path/to/Git_Repo_Analysis"
PYTHON_PATH="/path/to/python"
PIP_PATH="/path/to/pip"
ENV_FILE="$PROJECT_PATH/RepoAnalysis/.env"

# Check if the .env file exists in the directory
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: .env file is not present in the Git_Repo_Analysis/RepoAnalysis/ directory."
    echo "Please make sure the .env file is created and contains the necessary environment variables."
    exit 1
fi

# Navigate to the project directory
cd "$PROJECT_PATH" || { echo "ERROR: Could not change to the project directory. Check the path specified."; exit 1; }

# Create and activate a virtual environment (optional, but recommended)
if ! command -v "$PYTHON_PATH" &>/dev/null; then
    echo "ERROR: Python executable not found. Please set PYTHON_PATH variable correctly."
    exit 1
fi

if ! command -v "$PIP_PATH" &>/dev/null; then
    echo "ERROR: Pip executable not found. Please set PIP_PATH variable correctly."
    exit 1
fi

if [ ! -d "venv" ]; then
    $PYTHON_PATH -m venv venv || { echo "ERROR: Failed to create virtual environment."; exit 1; }
fi

source venv/bin/activate || { echo "ERROR: Failed to activate virtual environment."; exit 1; }

# Install project dependencies
$PIP_PATH install -r requirements.txt || { echo "ERROR: Failed to install project dependencies."; exit 1; }

# Run database migrations (if applicable)
python manage.py migrate || { echo "ERROR: Database migration failed."; exit 1; }

# Collect static files (if applicable)
python manage.py collectstatic --noinput || { echo "ERROR: Failed to collect static files."; exit 1; }

# Start the development server (adjust the command as per your project's setup)
python manage.py runserver || { echo "ERROR: Failed to start the development server."; exit 1; }

# Deactivate the virtual environment (if used)
deactivate