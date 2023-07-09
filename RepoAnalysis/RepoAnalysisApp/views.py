import os
import csv
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

## Modules Initialization
from RepoAnalysisApp.utils.github_api import GitHubAPI
from RepoAnalysisApp.utils.graph_plotter import GraphPlotter
from RepoAnalysisApp.utils.SocialAccountDATA import SocialAccountDATA

# Social Accounts modules
from allauth.account.views import SignupView, LoginView, LogoutView


## Results Dir Declaration create if not exists
RESULTS_DIR = "RepoAnalysisApp/static/results"
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

## function to Save the file in json
def save_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

## function to Save the file in csv
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

def analyze_repository(repository_url, access_token):
    ## This is temporary API KEY, please use your gitHub KEY code while running locally
    github_api = GitHubAPI(access_token)
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
        save_json_file(contributors_data, contributors_json_file)
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
        save_json_file(code_churn_data, code_churn_json_file)

    ## Commit Details
    commit_activity = retry_api(lambda: github_api.get_commit_activity(repository_url))
    if commit_activity:
        graph_plotter.plot_commit_activity(commit_activity, repository_url, repo_directory)
        commit_activity_data = [[data["week"], data["total"]] for data in commit_activity]
        commit_activity_csv_file = os.path.join(repo_directory, "commit_activity.csv")
        save_csv_file(commit_activity_data, commit_activity_csv_file)
        save_json_file(commit_activity_data, commit_activity_json_file)
    print(f"Analyzing repository: {repository_url}")

# Create your views here.

def home(request):
    
    context={}
   
    if request.user.is_superuser:
        request.session.clear()
        return redirect('home')
    
    elif request.user.is_authenticated:
        data = SocialAccountDATA(request).get_extra_data()
        context = data
        redirect('login')
    
    return render(request, "RepoAnalysisApp/home.html", context)

@login_required
def index(request):
    context={}
    
    return render(request, "RepoAnalysisApp/index.html", context)

@login_required
def analyze(request):
    
    if request.method == "POST":

        input_method = request.POST.get("input_method")

        if input_method == 'repository':            
            repository_url = request.POST.get("repository_url")
            analyze_repository(repository_url, SocialAccountDATA(request).get_access_token())
            repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
            context={"repository_url": repository_url, "repo_name": repo_name}

            return render(request, "RepoAnalysisApp/results.html",context)

        elif input_method == 'txt_file':

            file = request.FILES["file"]
            file.save('repositories.txt')
            #analyze_file('repositories.txt')

            context={"file_uploaded" : True}
            return render(request, "RepoAnalysisApp/results.html",context)

    return render(request, "RepoAnalysisApp/index.html")
    
    
class RepoAnalysisLogin(LoginView):
    template_name = 'account/login.html'
    
repoAnalysisLogin = RepoAnalysisLogin.as_view()

class RepoAnalysisLogout(LogoutView):
    template_name = 'account/logout.html'
    
repoAnalysisLogout = RepoAnalysisLogout.as_view()