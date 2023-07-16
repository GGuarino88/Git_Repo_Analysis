import os
import csv
import json
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

## Modules Initialization
from RepoAnalysisApp.utils.github_api import GitHubAPI
from RepoAnalysisApp.utils.graph_plotter import GraphPlotter
from RepoAnalysisApp.utils.SocialAccountDATA import SocialAccountDATA

# Social Accounts modules
from allauth.account.views import SignupView, LoginView, LogoutView

from .models import Scan, User_Scans

## Results Dir Declaration create if not exists
RESULTS_DIR = "RepoAnalysisApp/static/results"
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

## function to Save the file in json
def save_json_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

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
        contributors_data = [{"login": contributor["login"], "contributions": contributor["contributions"]} for contributor in contributors]
        contributors_json_file = os.path.join(repo_directory, "contributors_graph.json")
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
        code_churn_data = [{"additions": entry[0], "deletions": entry[1], "commits": entry[2]} for entry in code_churn]
        code_churn_json_file = os.path.join(repo_directory, "code_churn_over_time.json")
        save_json_file(code_churn_data, code_churn_json_file)

    ## Commit Details
    commit_activity = retry_api(lambda: github_api.get_commit_activity(repository_url))
    if commit_activity:
        graph_plotter.plot_commit_activity(commit_activity, repository_url, repo_directory)
        commit_activity_data = [{"week": data["week"], "total": data["total"]} for data in commit_activity]
        commit_activity_json_file = os.path.join(repo_directory, "commit_activity.json")
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
    mydata = Scan.objects.filter(author=request.user).values()
    print(mydata)
    return render(request, "RepoAnalysisApp/index.html", {'mydata':mydata})

@method_decorator(login_required, name='dispatch')
class ScanCreateView(CreateView):
    model = Scan
    template_name = 'RepoAnalysisApp/ScanSession/scan-create.html'
    fields = ('title',)
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

scan_create = ScanCreateView.as_view()

@method_decorator(login_required, name='dispatch')
class ScanEditView(UpdateView):
    model = Scan
    template_name = 'RepoAnalysisApp/ScanSession/scan-edit.html'
    fields = ('title',)
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
scan_edit = ScanEditView.as_view()

@method_decorator(login_required, name='dispatch')
class ScanDeleteView(DeleteView):
    model = Scan
    template_name = 'RepoAnalysisApp/ScanSession/scan-delete.html'
    success_url = reverse_lazy('index')
    
scan_delete = ScanDeleteView.as_view()

@login_required
def scan(request, scan_session):    
    
    context = {}
    
    scan_session_id = Scan.objects.filter(title=scan_session).values()[0]['id']
    user_scanned_repos = User_Scans.objects.filter(scan_id=scan_session_id).values()
    context = {'scan_session' : scan_session, 'user_scanned_repos': user_scanned_repos}
    
    return render(request,"RepoAnalysisApp/scan.html", context)

@method_decorator(login_required, name='dispatch')
class RepoCreateView(CreateView):
    
    model = User_Scans
    template_name = 'RepoAnalysisApp/RepoScanned/repo-create.html'
    fields = ('name','url_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session ={'scan_session': self.kwargs['scan_session']}
        context.update(scan_session)
        return context
    
    def form_valid(self, form):
        scan_session = self.kwargs['scan_session']
        form.instance.scan_id = Scan.objects.filter(title=scan_session)[0]
        return super().form_valid(form)
    
    def get_success_url(self):

          scan_session=self.kwargs['scan_session']
          return reverse_lazy('scan', kwargs={'scan_session': scan_session})
    
repo_create = RepoCreateView.as_view()

@method_decorator(login_required, name='dispatch')
class RepoEditView(UpdateView):
    model = User_Scans
    template_name = 'RepoAnalysisApp/RepoScanned/repo-edit.html'
    fields = ('name','url_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session ={'scan_session': self.kwargs['scan_session']}
        context.update(scan_session)
        return context
    
    def form_valid(self, form):
        scan_session = self.kwargs['scan_session']
        form.instance.scan_id = Scan.objects.filter(title=scan_session)[0]
        return super().form_valid(form)
    
    def get_success_url(self):

        scan_session=self.kwargs['scan_session']
        return reverse_lazy('scan', kwargs={'scan_session': scan_session})
    
repo_edit = RepoEditView.as_view()

@method_decorator(login_required, name='dispatch')
class RepoDeleteView(DeleteView):
    model = User_Scans
    template_name = 'RepoAnalysisApp/RepoScanned/repo-delete.html'
    success_url = reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session ={'scan_session': self.kwargs['scan_session']}
        context.update(scan_session)
        return context
    
    def get_success_url(self):

          scan_session=self.kwargs['scan_session']
          return reverse_lazy('scan', kwargs={'scan_session': scan_session})
    
repo_delete = RepoDeleteView.as_view()

@login_required
def about(request):
    context = {}
    return render(request, "RepoAnalysisApp/about.html", context)

@login_required
def analyze(request, scan_session, url_name):
    
    if request.method == "POST":
        input_method = request.POST.get("input_method")
        if input_method == 'repository':
            repository_url = request.POST.get("repository_url")
            analyze_repository(repository_url, SocialAccountDATA(request).get_access_token())
            repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
            context={"repository_url": repository_url, "repo_name": repo_name}
            return render(request, "RepoAnalysisApp/results.html", context)
        elif input_method == 'txt_file':
            file = request.FILES["file"]
            file.save('repositories.txt')
            context={"file_uploaded" : True}
            return render(request, "RepoAnalysisApp/results.html", context)
    return render(request, "RepoAnalysisApp/index.html")

class RepoAnalysisLogin(LoginView):
    template_name = 'account/login.html'

repoAnalysisLogin = RepoAnalysisLogin.as_view()

class RepoAnalysisLogout(LogoutView):
    template_name = 'account/logout.html'

repoAnalysisLogout = RepoAnalysisLogout.as_view()