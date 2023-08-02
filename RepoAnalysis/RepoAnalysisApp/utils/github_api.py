import time, requests
class GitHubAPI:
    def __init__(self, token):
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {token}"}

    def make_authenticated_request(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and 'rate limit exceeded' in response.text.lower():
            print("API rate limit exceeded. Retrying in 1 second...")
            time.sleep(1)
            return self.make_authenticated_request(endpoint)
        else:
            return None

    def make_retry_request(self, endpoint, max_retries=5, retry_delay=1, params=None):
        for _ in range(max_retries):
            response = self.make_authenticated_request(endpoint)
            if response is not None:
                return response
        return None

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
    
    ## below code is very expensive ( loop over multiple times based on PR's count for Repository which takes so much of time to complete )
    # def get_all_pull_requests(self, repository_url):
    #     owner, repo = self.parse_repository_url(repository_url)
    #     endpoint = f"repos/{owner}/{repo}/pulls"
    #     all_pull_requests = []
    #     page = 1
    #     while True:
    #         params = {"state": "all", "per_page": 100, "page": page}
    #         pull_requests = self.make_retry_request(endpoint, params=params)
    #         if not pull_requests:
    #             break
    #         all_pull_requests.extend(pull_requests)
    #         page += 1
    #     return all_pull_requests