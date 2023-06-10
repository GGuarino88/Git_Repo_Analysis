## Modules Initialization
import os
import csv
import argparse
from flask import Flask, request, render_template
from utils.github_api import GitHubAPI
from utils.graph_plotter import GraphPlotter

## Results Dir Declaration create if not exists
RESULTS_DIR = "results"
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

## Save the file to csv function
def save_csv_file(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

## Implmented retry mechanism if api fails to get the response. So max tries is 5
def retry_api(api_call):
    retry_count = 0
    response = None
    while retry_count < 5:
        response = api_call()
        if response:
            break
        else:
            retry_count += 1
    if response is None:
        print("Unable to retrieve data after 5 retries.")
    return response

def analyze_repository(repository_url):
    ## This is temporary API KEY, please use your gitHub KEY code while running locally 
    github_api = GitHubAPI("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")
    graph_plotter = GraphPlotter()
    repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
    repo_directory = os.path.join(RESULTS_DIR, repo_name)
    create_directory(repo_directory)
    
    ## Contributors Details
    contributors = retry_api(lambda: github_api.get_contributors(repository_url))
    if contributors:
        graph_plotter.plot_contributors_graph(contributors, repository_url, repo_directory)
        contributors_data = [[contributor["login"], contributor["contributions"]] for contributor in contributors]
        contributors_csv_file = os.path.join(repo_directory, "contributors_graph.csv")
        save_csv_file(contributors_data, contributors_csv_file)
        total_contributions = sum(contributor["contributions"] for contributor in contributors)
        meaningful_contributors = [contributor["login"] for contributor in contributors if contributor["contributions"] > total_contributions / len(contributors)]
        if len(meaningful_contributors) == len(contributors):
            print("Every team member has committed meaningful parts of the code.")
        else:
            print("Not every team member has committed meaningful parts of the code.")
            print("Meaningful contributors:", meaningful_contributors)
            
    ## Code CRUD Details
    code_churn = retry_api(lambda: github_api.get_code_churn(repository_url))
    if code_churn:
        graph_plotter.plot_code_churn(code_churn, repository_url, repo_directory)
        code_churn_data = [[entry[0], entry[1], entry[2]] for entry in code_churn]
        code_churn_csv_file = os.path.join(repo_directory, "code_churn_over_time.csv")
        save_csv_file(code_churn_data, code_churn_csv_file)
    
    ## Commit Details
    commit_activity = retry_api(lambda: github_api.get_commit_activity(repository_url))
    if commit_activity:
        graph_plotter.plot_commit_activity(commit_activity, repository_url, repo_directory)
        commit_activity_data = [[data["week"], data["total"]] for data in commit_activity]
        commit_activity_csv_file = os.path.join(repo_directory, "commit_activity.csv")
        save_csv_file(commit_activity_data, commit_activity_csv_file)
    print(f"Analyzing repository: {repository_url}")

app = Flask(__name__, static_folder='/')
@app.route('/analyze', methods=['POST'])
def analyze():
    input_method = request.form.get('input_method')
    if input_method == 'repository':
        repository_url = request.form.get('repository_url')
        analyze_repository(repository_url)
        repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
        return render_template('results.html', repository_url=repository_url, repo_name=repo_name)
    elif input_method == 'txt_file':
        file = request.files['file']
        file.save('repositories.txt')
        analyze_file('repositories.txt')
        return render_template('results.html', file_uploaded=True)
    return render_template('templates/index.html')

@app.route('/')
def index():
    return app.send_static_file('templates/index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)