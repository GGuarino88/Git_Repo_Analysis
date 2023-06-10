# GitHub Analysis

GitHub Analysis is a web application that analyzes GitHub repositories and provides insights into contributors, code churn over time, and commit activity.

## Features

- Analyze GitHub repositories by providing the repository URL.
- Retrieve and visualize contributors' information with a graph.
- Plot code churn over time and display it as a graph.
- Analyze commit activity and present it as a graph.

## Requirements

- Python 3.6+
- Flask
- GitHub API token (replace `YOUR_GITHUB_API_TOKEN` in `main.py`)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/girikMET/gitHub_Analysis.
```
2. Install the required dependencies:
```bash
sudo apt-get -y update && sudo apt-get install python3 python3-pip apache2
cd gitHub_Analysis
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py or python3 main.py
```
4. Access the application in your web browser at http://localhost:5000.
```Usage
Enter a repository URL in the provided input field.
```
5. Click on the "Analyze" button.
6. The analysis results, including the contributors graph, code churn over time, and commit activity.