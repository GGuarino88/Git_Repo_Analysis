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
    
    def get_code_generic(self, repository_url, method):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}{method}"
        generic_data = self.make_authenticated_request(endpoint)
        return generic_data