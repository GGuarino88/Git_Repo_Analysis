import requests
class GitHubAPI:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {token}"}

    def make_authenticated_request(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def parse_repository_url(self, repository_url):
        parts = repository_url.split("/")
        owner = parts[-2]
        repo = parts[-1].split(".")[0]
        return owner, repo

    def get_repository_info(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}"
        repo_info = self.make_authenticated_request(endpoint)
        return repo_info

    def get_contributors(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/contributors"
        contributors = self.make_authenticated_request(endpoint)
        return contributors

    def get_pull_requests(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/pulls?state=all"
        pull_requests = self.make_authenticated_request(endpoint)
        return pull_requests

    def get_issues(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/issues?state=all"
        issues = self.make_authenticated_request(endpoint)
        return issues

    def get_commit_details(self, repository_url, sha):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/commits/{sha}"
        commit = self.make_authenticated_request(endpoint)
        return commit

    def get_languages(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/languages"
        languages = self.make_authenticated_request(endpoint)
        return languages

    def get_releases(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/releases"
        releases = self.make_authenticated_request(endpoint)
        return releases

    def get_traffic_views(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/traffic/views"
        views = self.make_authenticated_request(endpoint)
        return views

    def get_commit_activity(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/stats/commit_activity"
        commit_activity = self.make_authenticated_request(endpoint)
        return commit_activity

    def get_code_churn(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/stats/code_frequency"
        code_churn = self.make_authenticated_request(endpoint)
        return code_churn