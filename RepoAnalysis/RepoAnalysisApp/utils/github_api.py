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

    def get_commit_count_per_branch(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        branches = self.get_code_generic(repository_url, "/branches")
        commit_count_per_branch = {}
        for branch in branches:
            branch_name = branch['name']
            branch_endpoint = f"repos/{owner}/{repo}/commits?sha={branch_name}&per_page=100"
            commits = []
            page = 1
            while True:
                commits_response = self.make_authenticated_request(branch_endpoint + f"&page={page}")
                if not commits_response:
                    break
                commits.extend(commits_response)
                page += 1
            commit_count_per_branch[branch_name] = len(commits)
        return commit_count_per_branch
    
    def get_pull_request_count_per_contributor(self, repository_url):
        owner, repo = self.parse_repository_url(repository_url)
        endpoint = f"repos/{owner}/{repo}/pulls?state=all"
        pull_requests = self.make_authenticated_request(endpoint)
        pull_request_count_per_contributor = {}
        for pull_request in pull_requests:
            contributor = pull_request['user']['login']
            if contributor in pull_request_count_per_contributor:
                pull_request_count_per_contributor[contributor] += 1
            else:
                pull_request_count_per_contributor[contributor] = 1
        return pull_request_count_per_contributor