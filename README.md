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
Everytime we access the code editor
```bash
source my_venv/bin/activate
```
Install requirements (First time and as new dependencies are installed)
```bash
pip install -r requirements.txt
```
Create environment Variables in the Base directory "../RepoAnalysis/.env"
```bash
touch .env
nano .env
SECRET_KEY=<DJANGO_SECRET_KEY> # Located in Settings.py
DEBUG=True # Will switch to "False" once in production
GIT_API_TOKEN=<GIT_HUB_PERSONAL_TOKEN> # Generate your own in GitHUB
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

# GitHub Repository Analysis Community

Welcome to the GitHub Repository Analysis community! This page provides information and resources for contributing to the project.

## Code of Conduct

We have adopted a [Code of Conduct](./CODE_OF_CONDUCT.md) to ensure a welcoming and inclusive community environment. Please read it and abide by the guidelines.

## Contributing

We welcome contributions from the community to make GitHub Repository Analysis even better. If you're interested in contributing, please check out our [Contributing Guidelines](./CONTRIBUTING.md) for more details.

### Writing Contributing Guidelines

If you're new to writing contributing guidelines, you can refer to our [Contributing Guidelines Template](./CONTRIBUTING_TEMPLATE.md) to get started.

## License

GitHub Repository Analysis is released under the [MIT License](./LICENSE). Make sure to review the license terms before using or contributing to the project.

## Security Policy

Ensuring the security of our users is a top priority. If you discover any security vulnerabilities or issues, please follow our [Security Policy](./SECURITY.md) and report them responsibly.

### Set up a Security Policy

To set up a security policy for your own projects, you can use our [Security Policy Template](./SECURITY_TEMPLATE.md) as a starting point.

## Issue Templates

To streamline the issue creation process and provide clear guidelines for bug reports, feature requests, and other types of issues, we have provided [Issue Templates](./.github/ISSUE_TEMPLATE).

## Pull Request Template

When submitting a pull request, please follow our [Pull Request Template](./.github/PULL_REQUEST_TEMPLATE.md) to ensure that all necessary information is included.

We appreciate your contributions and look forward to building a thriving GitHub Repository Analysis community together!
