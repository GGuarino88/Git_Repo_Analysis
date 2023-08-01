## Modules Initialization
import os, json
from django.contrib import messages
from django.http import JsonResponse
from .models import ScanSession, SingleURLRepo
from django.db import IntegrityError
from django.urls import reverse_lazy
from .forms import ScanSessionForm, SingleURLRepoForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from RepoAnalysisApp.utils.github_api import GitHubAPI
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from RepoAnalysisApp.utils.SocialAccountDATA import SocialAccountDATA
from allauth.account.views import LoginView, LogoutView

## Results Dir Declaration create if not exists
RESULTS_DIR = "RepoAnalysisApp/static/results"
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

## function to Save the file in json
def save_json_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file)

## Implmented retry mechanism if api fails to get the response. So max tries is 5
def retry_api(api_call):
    retry_count = 0
    response = None
    while retry_count < 5:
        try:
            response = api_call()
            if response:
                break
            else:
                retry_count += 1
        except Exception as e:
            print(f"API call failed. Retry {retry_count+1}/5")
            print("Error:", e)
            retry_count += 1
    if response is None:
        print("Unable to retrieve data after 5 retries.")
    return response

def remove_all_files(directory):
    files = os.listdir(directory)
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

def analyze_repository(repository_url, access_token):
    ## This is temporary API KEY, please use your gitHub KEY code while running locally
    github_api = GitHubAPI(access_token)
    repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
    repo_directory = os.path.join(RESULTS_DIR, repo_name)
    if os.path.exists(repo_directory):
        remove_all_files(repo_directory)
    else:
        create_directory(repo_directory)
    try:
        ## Contributors Details
        contributors = retry_api(lambda: github_api.get_contributors(repository_url))
        if contributors:
            contributors_data = [{"login": contributor["login"],"contributions": contributor["contributions"],} for contributor in contributors]
            contributors_json_file = os.path.join(repo_directory, "contributors_graph.json")
            save_json_file(contributors_data, contributors_json_file)

        ## Code CRUD Details
        code_churn = retry_api(lambda: github_api.get_code_churn(repository_url))
        if code_churn:
            code_churn_data = [{"additions": entry[0], "deletions": entry[1], "commits": entry[2]} for entry in code_churn]
            code_churn_json_file = os.path.join(repo_directory, "code_churn_over_time.json")
            save_json_file(code_churn_data, code_churn_json_file)

        ## Commit Details
        commit_activity = retry_api(lambda: github_api.get_commit_activity(repository_url))
        if commit_activity:
            commit_activity_data = [{"week": data["week"], "total": data["total"]} for data in commit_activity]
            commit_activity_json_file = os.path.join(repo_directory, "commit_activity.json")
            save_json_file(commit_activity_data, commit_activity_json_file)

        ## Repository Info
        repo_info = retry_api(lambda: github_api.get_repository_info(repository_url))
        if repo_info:
            repo_info_json_file = os.path.join(repo_directory, "repo_info.json")
            save_json_file(repo_info, repo_info_json_file)

        ## Pull Requests
        pull_requests = retry_api(lambda: github_api.get_pull_requests(repository_url))
        if pull_requests:
            pull_requests_json_file = os.path.join(repo_directory, "pull_requests.json")
            save_json_file(pull_requests, pull_requests_json_file)

        ## Languages
        languages = retry_api(lambda: github_api.get_languages(repository_url))
        if languages:
            languages_json_file = os.path.join(repo_directory, "languages.json")
            save_json_file(languages, languages_json_file)

        ## Releases
        releases = retry_api(lambda: github_api.get_releases(repository_url))
        if releases:
            releases_json_file = os.path.join(repo_directory, "releases.json")
            save_json_file(releases, releases_json_file)

        ## Traffic Views
        traffic_views = retry_api(lambda: github_api.get_traffic_views(repository_url))
        if traffic_views:
            if isinstance(traffic_views, str):
                traffic_views = json.loads(traffic_views)
            traffic_views_json_file = os.path.join(repo_directory, "traffic_views.json")
            save_json_file(traffic_views, traffic_views_json_file)

    except Exception as e:
        print("An error occurred while analyzing the repository:")
        print(e)

# Create your views here.
def home(request):
    context = {}
    if request.user.is_superuser:
        request.session.clear()
        return redirect("home")
    
    elif request.user.is_authenticated:
        data = SocialAccountDATA(request).get_extra_data()
        context = data
        redirect("login")

    return render(request, "RepoAnalysisApp/home.html", context)

@login_required
def index(request):
    mydata = ScanSession.objects.filter(author=request.user).values()
    return render(request, "RepoAnalysisApp/index.html", {"mydata": mydata})

@method_decorator(login_required, name="dispatch")
class ScanCreateView(CreateView):
    model = ScanSession
    form_class = ScanSessionForm
    template_name = "RepoAnalysisApp/ScanSession/scan-create.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        form.instance.author = self.request.user
        scan_session_title = form.cleaned_data.get("title")
        try:
            new_scan_session = super().form_valid(form)
            messages.success(self.request, f'Session: "{ scan_session_title }" Created')
            return new_scan_session

        except IntegrityError:
            form.add_error(None, f'"{scan_session_title}" already exists')
            return self.form_invalid(form)
        
scan_create = ScanCreateView.as_view()

@method_decorator(login_required, name="dispatch")
class ScanEditView(UpdateView):
    model = ScanSession
    form_class = ScanSessionForm
    template_name = "RepoAnalysisApp/ScanSession/scan-edit.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        form.instance.author = self.request.user
        scan_session_title = form.initial.get("title")
        new_scan_session_title = form.cleaned_data.get("title")
        try:
            new_scan_session = super().form_valid(form)
            if scan_session_title == new_scan_session_title:
                messages.success(self.request, f'No changes to: "{scan_session_title}"')
            else:
                messages.info(
                    self.request,
                    f'Session: "{scan_session_title}" Changed to: "{new_scan_session_title}"',
                )
            return new_scan_session
        
        except IntegrityError:
            form.add_error(None, f'"{scan_session_title}" already exists')
            return self.form_invalid(form)

scan_edit = ScanEditView.as_view()

@method_decorator(login_required, name="dispatch")
class ScanDeleteView(DeleteView):
    model = ScanSession
    template_name = "RepoAnalysisApp/ScanSession/scan-delete.html"
    def get_success_url(self):
        deleted_scan_session_title = self.get_object().__dict__["title"]
        messages.success(self.request, f'Session: "{deleted_scan_session_title}" Deleted')
        return reverse_lazy("index")
    
scan_delete = ScanDeleteView.as_view()

def scan(request, scan_session):
    context = {}
    scan_session_id = (ScanSession.objects.filter(title=scan_session).filter(author_id=request.user.id).values()[0]["id"])
    user_scanned_repos = SingleURLRepo.objects.filter(scan_id=scan_session_id).values()
    context = {"scan_session": scan_session, "user_scanned_repos": user_scanned_repos}
    return render(request, "RepoAnalysisApp/scan.html", context)

@method_decorator(login_required, name="dispatch")

class RepoCreateView(CreateView):
    model = SingleURLRepo
    form_class = SingleURLRepoForm
    template_name = "RepoAnalysisApp/RepoScanned/repo-create.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session = {"scan_session": self.kwargs["scan_session"]}
        context.update(scan_session)
        return context
    def form_valid(self, form):
        scan_session = self.kwargs["scan_session"]
        repo_name = form.cleaned_data.get("repo_name")
        repo_url = form.cleaned_data.get("url_name")
        form.instance.scan_id = ScanSession.objects.filter(title=scan_session).filter(
            author_id=self.request.user.id
        )[0]
        try:
            new_repo = super().form_valid(form)
            messages.success(self.request, f'Repository: "{ repo_name }" Created')
            return new_repo

        except IntegrityError as integrity_exc:
            if (str(integrity_exc) == "UNIQUE constraint failed: user_scaned_repo.scan_id_id, user_scaned_repo.repo_name"):
                form.add_error(None, f'Repository Name: "{repo_name}" already exists in {scan_session}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_scaned_repo.scan_id_id, user_scaned_repo.url_name"):
                form.add_error(None, f'Repository URL: "{repo_url}" already exists in {scan_session}',)
            return self.form_invalid(form)
        
    def get_success_url(self):
        scan_session = self.kwargs["scan_session"]
        return reverse_lazy("scan", kwargs={"scan_session": scan_session})
    
repo_create = RepoCreateView.as_view()

@method_decorator(login_required, name="dispatch")
class RepoEditView(UpdateView):
    model = SingleURLRepo
    form_class = SingleURLRepoForm
    template_name = "RepoAnalysisApp/RepoScanned/repo-edit.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session = {"scan_session": self.kwargs["scan_session"]}
        context.update(scan_session)
        return context
    
    def form_valid(self, form):
        scan_session = self.kwargs["scan_session"]
        repo_name = form.initial.get("repo_name")
        repo_url = form.initial.get("url_name")
        new_repo_name = form.cleaned_data.get("repo_name")
        new_repo_url = form.cleaned_data.get("url_name")
        form.instance.scan_id = ScanSession.objects.filter(title=scan_session).filter(author_id=self.request.user.id)[0]
        try:
            edited_repo = super().form_valid(form)
            repo_data_changed = [key for key, value in form.cleaned_data.items() if form.initial.get(key) != value]
            if repo_data_changed:
                if repo_data_changed[0] == "repo_name":
                    messages.success(self.request, f'Repository name: "{repo_name}" changed to: "{new_repo_name}"',)
                elif repo_data_changed[0] == "url_name":
                    messages.success(self.request, f'"{repo_name}" URL changed to: "{new_repo_url}"')
            return edited_repo
        
        except IntegrityError as integrity_exc:
            if (str(integrity_exc) == "UNIQUE constraint failed: user_scaned_repo.scan_id_id, user_scaned_repo.repo_name"):
                form.add_error(None, f'Repository Name: "{repo_name}" already exists in {scan_session}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_scaned_repo.scan_id_id, user_scaned_repo.url_name"):
                form.add_error(None, f'Repository URL: "{repo_url}" already exists in {scan_session}',)
            return self.form_invalid(form)
        
    def get_success_url(self):
        scan_session = self.kwargs["scan_session"]
        return reverse_lazy("scan", kwargs={"scan_session": scan_session})
    
repo_edit = RepoEditView.as_view()

@method_decorator(login_required, name="dispatch")
class RepoDeleteView(DeleteView):
    model = SingleURLRepo
    template_name = "RepoAnalysisApp/RepoScanned/repo-delete.html"
    success_url = reverse_lazy("index")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scan_session = {"scan_session": self.kwargs["scan_session"]}
        context.update(scan_session)
        return context
    
    def get_success_url(self):
        scan_session = self.kwargs["scan_session"]
        deleted_repo = self.get_object().__dict__["repo_name"]
        messages.success(self.request, f'Repository: "{deleted_repo}" Deleted')
        return reverse_lazy("scan", kwargs={"scan_session": scan_session})
    
repo_delete = RepoDeleteView.as_view()

def about(request):
    context = {}
    return render(request, "RepoAnalysisApp/about.html", context)

def load_json_data(repo_name, file_name):
    file_path = os.path.join("RepoAnalysisApp/static/results/", repo_name, file_name)
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}

@login_required
def analyze(request, scan_session, url_name):
    if request.method == "POST":
        input_method = request.POST.get("input_method")
        if input_method == "repository":
            repository_url = request.POST.get("repository_url")
            analyze_repository(repository_url, SocialAccountDATA(request).get_access_token())
            repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
            context = {"repository_url": repository_url, "repo_name": repo_name, }
            return render(request, "RepoAnalysisApp/results.html", context)
    return render(request, "RepoAnalysisApp/index.html")

def generate_all_reports(request, scan_session):
    if request.method == "POST":
        selected_repos_json = request.POST.get("selected_repos")
        selected_repos = json.loads(selected_repos_json)
        if selected_repos:
            repo_ids = []
            for url in selected_repos:
                user_scan = SingleURLRepo.objects.filter(scan_id__title=scan_session, url_name=url).first()
                if user_scan:
                    repo_ids.append(user_scan.id)
            access_token = SocialAccountDATA(request).get_access_token()
            for repository_url in selected_repos:
                analyze_repository(repository_url, access_token)
            context = {"repository_urls": selected_repos, "repo_names": [repo_url.replace("https://github.com/", "").replace("/", "_") for repo_url in selected_repos]}
            repositories = list(zip(context["repository_urls"], context["repo_names"]))
            context = {'repositories': repositories}
            return render(request, "RepoAnalysisApp/results_multiple.html", context)
        
        else:
            return render(request, "RepoAnalysisApp/index.html")
        
    return redirect("scan", scan_session=scan_session)

class RepoAnalysisLogin(LoginView):
    template_name = "account/login.html"

repoAnalysisLogin = RepoAnalysisLogin.as_view()

class RepoAnalysisLogout(LogoutView):
    template_name = "account/logout.html"

repoAnalysisLogout = RepoAnalysisLogout.as_view()