# Git_Repo_Analysis

GitHub Analysis is a web application that analyzes GitHub repositories and provides insights into contributors, code churn over time, and commit activity.

## Features

- Analyze GitHub repositories by providing the repository URL.
- Retrieve and visualize contributors' information with a graph.
- Plot code churn over time and display it as a graph.
- Analyze commit activity and present it as a graph.

## Requirements
```bash
python3 get-pip.py
```
- GitHub API token (replace `YOUR_GITHUB_API_TOKEN` in `views.py`)

## Getting Started
1. Clone the repository:
```bash
git clone https://github.com/GGuarino88/Git_Repo_Analysis
```
2. Activate virtual environment and Install the required dependencies:
First Time setting up virtual Environment
```bash
python3 -m venv my_venv
```
Everytime we access the application
```bash
source my_venv/bin/activate
```
Install requirements (First time and as new dependencies are installed)
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python3 manage.py runserver
```
4. Access the application in your web browser at http://127.0.0.1:8000/.
```Usage
Enter a repository URL in the provided input field.
```
5. Click on the "Analyze" button.
6. The analysis results, including the contributors graph, code churn over time, and commit activity.
