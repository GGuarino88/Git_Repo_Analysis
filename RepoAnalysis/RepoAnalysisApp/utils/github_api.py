import requests

class GitHubAPI:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {token}"}

    def make_authenticated_request(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_contributors(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/contributors"
        contributors = self.make_authenticated_request(endpoint)
        return contributors
    
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
    
    def get_collaborator_info(self, repository_url, collaborator):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/collaborators/{collaborator}"
        collaborator_info = self.make_authenticated_request(endpoint)
        return collaborator_info
    
    def is_pull_request_authorized(self, repository_url, collaborator):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/collaborators/{collaborator}/permission"
        collaborator_info = self.make_authenticated_request(endpoint)
        return collaborator_info.get("pull", False)
		
    def parse_repository_url(self, repository_url):
        parts = repository_url.split("/")
        owner = parts[-2]
        repo = parts[-1].split(".")[0]
        return owner, repo
