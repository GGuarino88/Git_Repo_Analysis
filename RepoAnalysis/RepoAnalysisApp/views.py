## Modules Initialization
import os, json
from django.contrib import messages
from .models import Semester, SemesterProject
from django.db import IntegrityError
from django.urls import reverse_lazy
from .forms import SemesterForm, ProjectForm
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
        contributors = retry_api(lambda: github_api.get_code_generic(repository_url, "/contributors"))
        if contributors:
            contributors_data = [{"login": contributor["login"],"contributions": contributor["contributions"],} for contributor in contributors]
            contributors_json_file = os.path.join(repo_directory, "contributors_graph.json")
            save_json_file(contributors_data, contributors_json_file)

        ## Code CRUD Details
        code_churn = retry_api(lambda: github_api.get_code_generic(repository_url, "/stats/code_frequency"))
        if code_churn:
            code_churn_json_file = os.path.join(repo_directory, "code_churn_over_time.json")
            save_json_file(code_churn, code_churn_json_file)

        ## Commit Details
        commit_activity = retry_api(lambda: github_api.get_code_generic(repository_url, "/stats/commit_activity"))
        if commit_activity:
            commit_activity_json_file = os.path.join(repo_directory, "commit_activity.json")
            save_json_file(commit_activity, commit_activity_json_file)

        ## Repository Info
        repo_info = retry_api(lambda: github_api.get_code_generic(repository_url, ""))
        if repo_info:
            repo_info_json_file = os.path.join(repo_directory, "repo_info.json")
            save_json_file(repo_info, repo_info_json_file)

        ## Pull Requests
        pull_requests = retry_api(lambda: github_api.get_code_generic(repository_url, "/pulls?state=all&per_page=1000"))
        if pull_requests:
            filtered_pull_requests = []
            for pr in pull_requests:
                filtered_pr = {
                    "url": pr["url"],
                    "number": pr["number"],
                    "title": pr["title"],
                    "user": pr["user"]["login"],
                    "merged_at": pr["merged_at"],
                    "created_at": pr["created_at"]
                }
                filtered_pull_requests.append(filtered_pr)
            filtered_pull_requests_json_file = os.path.join(repo_directory, "pull_requests.json")
            save_json_file(filtered_pull_requests, filtered_pull_requests_json_file)

        ## Languages
        languages = retry_api(lambda: github_api.get_code_generic(repository_url, "/languages"))
        if languages:
            languages_json_file = os.path.join(repo_directory, "languages.json")
            save_json_file(languages, languages_json_file)

        ## Releases
        releases = retry_api(lambda: github_api.get_code_generic(repository_url, "/releases"))
        if releases:
            releases_json_file = os.path.join(repo_directory, "releases.json")
            save_json_file(releases, releases_json_file)

        ## Branches
        branches = retry_api(lambda: github_api.get_code_generic(repository_url, "/branches"))
        if branches:
            branches_json_file = os.path.join(repo_directory, "branches.json")
            save_json_file(branches, branches_json_file)

        ## Commits Count per branch
        commits_per_branch = retry_api(lambda: github_api.get_commit_count_per_branch(repository_url))
        if commits_per_branch:
            commits_per_branch_json_file = os.path.join(repo_directory, "commits_per_branch.json")
            save_json_file(commits_per_branch, commits_per_branch_json_file)

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
    mydata = Semester.objects.filter(author=request.user).values()
    return render(request, "RepoAnalysisApp/index.html", {"mydata": mydata})

@method_decorator(login_required, name="dispatch")
class SemesterCreateView(CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = "RepoAnalysisApp/Semester/semester-create.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        form.instance.author = self.request.user
        semester_title = form.cleaned_data.get("title")
        try:
            new_semester = super().form_valid(form)
            messages.success(self.request, f'Semester: "{ semester_title }" Created')
            return new_semester

        except IntegrityError:
            form.add_error(None, f'"{semester_title}" already exists')
            return self.form_invalid(form)
        
semester_create = SemesterCreateView.as_view()

@method_decorator(login_required, name="dispatch")
class SemesterEditView(UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = "RepoAnalysisApp/Semester/semester-edit.html"
    success_url = reverse_lazy("index")
    def form_valid(self, form):
        form.instance.author = self.request.user
        semester_title = form.initial.get("title")
        new_semester_title = form.cleaned_data.get("title")
        try:
            new_semester_session = super().form_valid(form)
            if semester_title == new_semester_title:
                messages.success(self.request, f'No changes to: "{semester_title}"')
            else:
                messages.info(self.request, f'Semester: "{semester_title}" Changed to: "{new_semester_title}"')
            return new_semester_session
        
        except IntegrityError:
            form.add_error(None, f'"{semester_title}" already exists')
            return self.form_invalid(form)

semester_edit = SemesterEditView.as_view()

@method_decorator(login_required, name="dispatch")
class SemesterDeleteView(DeleteView):
    model = Semester
    template_name = "RepoAnalysisApp/Semester/semester-delete.html"
    def get_success_url(self):
        deleted_semester = self.get_object().__dict__["title"]
        messages.success(self.request, f'Semester: "{deleted_semester}" Deleted')
        return reverse_lazy("index")
    
semester_delete = SemesterDeleteView.as_view()

def scan(request, semester):
    context = {}
    semester_id = (Semester.objects.filter(title=semester).filter(author_id=request.user.id).values()[0]["id"])
    user_semester_projects = SemesterProject.objects.filter(scan_id=semester_id).values()
    context = {"semester": semester, "user_semester_projects": user_semester_projects}
    return render(request, "RepoAnalysisApp/scan.html", context)

@method_decorator(login_required, name="dispatch")

class ProjectCreateView(CreateView):
    model = SemesterProject
    form_class = ProjectForm
    template_name = "RepoAnalysisApp/Project/project-create.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester = {"semester": self.kwargs["semester"]}
        context.update(semester)
        return context
    def form_valid(self, form):
        semester = self.kwargs["semester"]
        team_name = form.cleaned_data.get("team_name")
        repo_name = form.cleaned_data.get("repo_name")
        repo_url = form.cleaned_data.get("url_name")
        form.instance.scan_id = Semester.objects.filter(title=semester).filter(author_id=self.request.user.id)[0]
        try:
            new_repo = super().form_valid(form)
            messages.success(self.request, f'Repository: "{ repo_name }" Created')
            return new_repo

        except IntegrityError as integrity_exc:
            if (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.team_name"):
                form.add_error(None, f'Team: "{team_name}" already exists in {semester}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.repo_name"):
                form.add_error(None, f'Project Name: "{repo_name}" already exists in {semester}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.url_name"):
                form.add_error(None, f'GitHub URL: "{repo_url}" already exists in {semester}',)
            return self.form_invalid(form)
        
    def get_success_url(self):
        semester = self.kwargs["semester"]
        return reverse_lazy("scan", kwargs={"semester": semester})
    
project_create = ProjectCreateView.as_view()

@method_decorator(login_required, name="dispatch")
class ProjectEditView(UpdateView):
    model = SemesterProject
    form_class = ProjectForm
    template_name = "RepoAnalysisApp/Project/project-edit.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester = {"semester": self.kwargs["semester"]}
        context.update(semester)
        return context
    
    def form_valid(self, form):
        semester = self.kwargs["semester"]
        team_name = form.initial.get("team_name")
        repo_name = form.initial.get("repo_name")
        repo_url = form.initial.get("url_name")
        new_team_name = form.cleaned_data.get("team_name")
        new_repo_name = form.cleaned_data.get("repo_name")
        new_repo_url = form.cleaned_data.get("url_name")
        form.instance.scan_id = Semester.objects.filter(title=semester).filter(author_id=self.request.user.id)[0]
        try:
            edited_repo = super().form_valid(form)
            repo_data_changed = [key for key, value in form.cleaned_data.items() if form.initial.get(key) != value]
            if repo_data_changed:
                if "team_name" in repo_data_changed:
                    messages.success(self.request, f'"{team_name}" changed to: "{new_team_name}"',)
                elif "repo_name" in repo_data_changed:
                    messages.success(self.request, f'Project: "{repo_name}" changed to: "{new_repo_name}"',)
                elif "url_name" in repo_data_changed:
                    messages.success(self.request, f'"{repo_name}" URL changed to: "{new_repo_url}"')
            return edited_repo
        
        except IntegrityError as integrity_exc:
            if (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.team_name"):
                form.add_error(None, f'Team: "{team_name}" already exists in {semester}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.repo_name"):
                form.add_error(None, f'Project Name: "{repo_name}" already exists in {semester}',)
            elif (str(integrity_exc) == "UNIQUE constraint failed: user_semester_projects.scan_id_id, user_semester_projects.url_name"):
                form.add_error(None, f'GitHub URL: "{repo_url}" already exists in {semester}',)
            return self.form_invalid(form)
        
    def get_success_url(self):
        semester = self.kwargs["semester"]
        return reverse_lazy("scan", kwargs={"semester": semester})
    
project_edit = ProjectEditView.as_view()

@method_decorator(login_required, name="dispatch")
class ProjectDeleteView(DeleteView):
    model = SemesterProject
    template_name = "RepoAnalysisApp/Project/project-delete.html"
    success_url = reverse_lazy("index")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        semester = {"semester": self.kwargs["semester"]}
        context.update(semester)
        return context

    def get_success_url(self):
        semester = self.kwargs["semester"]
        deleted_repo = self.get_object().__dict__["repo_name"]
        messages.success(self.request, f'Repository: "{deleted_repo}" Deleted')
        return reverse_lazy("scan", kwargs={"semester": semester})

project_delete = ProjectDeleteView.as_view()

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
def analyze(request, semester, team_name, repo_name):
    project_title = repo_name
    if request.method == "POST":
        input_method = request.POST.get("input_method")
        if input_method == "repository":
            repository_url = request.POST.get("repository_url")
            analyze_repository(repository_url, SocialAccountDATA(request).get_access_token())
            repo_name = repository_url.replace("https://github.com/", "").replace("/", "_")
            context = {"repository_url": repository_url, "team_name": team_name, "repo_name": repo_name, "project_title": project_title, }
            return render(request, "RepoAnalysisApp/results.html", context)
    return render(request, "RepoAnalysisApp/index.html")

def generate_all_reports(request, semester):
    if request.method == "POST":
        selected_repos_json = request.POST.get("selected_repos")
        selected_repos = json.loads(selected_repos_json)
        team_names = request.POST.getlist("team_names[]")
        project_names = request.POST.getlist("project_names[]")
        if selected_repos:
            repo_ids = []
            for url in selected_repos:
                user_semester_projects = SemesterProject.objects.filter(scan_id__title=semester, url_name=url).first()
                if user_semester_projects:
                    repo_ids.append(user_semester_projects.id)
            access_token = SocialAccountDATA(request).get_access_token()
            for repository_url in selected_repos:
                analyze_repository(repository_url, access_token)
            context = {
                "repository_urls": selected_repos,
                "repo_names": [repo_url.replace("https://github.com/", "").replace("/", "_") for repo_url in selected_repos],
                "team_names": team_names,
                "project_names": project_names,
            }
            repositories = list(zip(context["repository_urls"], context["repo_names"], context["team_names"], context["project_names"]))
            context = {'repositories': repositories}
            return render(request, "RepoAnalysisApp/results_multiple.html", context)
        else:
            return render(request, "RepoAnalysisApp/index.html")
        
    return redirect("scan", semester=semester)

class RepoAnalysisLogin(LoginView):
    template_name = "account/login.html"

repoAnalysisLogin = RepoAnalysisLogin.as_view()

class RepoAnalysisLogout(LogoutView):
    template_name = "account/logout.html"

repoAnalysisLogout = RepoAnalysisLogout.as_view()