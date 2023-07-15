import os
import datetime
import collections
import numpy as np
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#mac OS patch
plt.switch_backend('Agg')

class GraphPlotter:
    def plot_contributors_graph(self, contributors, repository_url, repo_directory):
        x = range(len(contributors))
        y = [contributor["contributions"] for contributor in contributors]
        colors = ['blue', 'green', 'red', 'orange', 'purple']
        plt.clf()
        plt.figure(figsize=(10, 6))
        plt.bar(x, y, color=colors)
        plt.xticks(x, [contributor["login"] for contributor in contributors])
        plt.xlabel("Contributors")
        plt.ylabel("Commits")
        title = repository_url.replace("https://github.com/", "")
        plt.title(f"{title} Contributors Graph")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{repo_directory}/contributors_graph.png")

    def plot_code_churn(self, code_churn, repository_url, repo_directory):
        weeks = [entry[0] for entry in code_churn]
        additions = [entry[1] for entry in code_churn]
        deletions = [-entry[2] for entry in code_churn]
        modifications = [additions[i] + deletions[i] for i in range(len(weeks))]
        dates = [datetime.fromtimestamp(week) for week in weeks]
        colors = ['purple', 'blue', 'green']
        plt.clf()
        plt.figure(figsize=(10, 6))
        plt.plot(dates, additions, color=colors[0], label='Additions')
        plt.plot(dates, deletions, color=colors[1], label='Deletions')
        plt.plot(dates, modifications, color=colors[2], label='Modifications')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        plt.ylabel("Lines of Code")
        title = repository_url.replace("https://github.com/", "")
        plt.title(f"{title} Code Churn Over Time")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"{repo_directory}/code_churn_over_time.png")

    def plot_commit_activity(self, commit_activity, repository_url, repo_directory):
        if not commit_activity:
            print("Commit activity data not available.")
            return
        weeks = [datetime.fromtimestamp(data["week"]).strftime('%Y-%m-%d') for data in commit_activity]
        counts = [data["total"] for data in commit_activity]
        colors = ['green']
        plt.clf()
        plt.figure(figsize=(10, 6))
        plt.plot(weeks, counts, color=colors[0])
        plt.xlabel("Date")
        plt.ylabel("Commit Counts")
        title = repository_url.replace("https://github.com/", "")
        plt.title(f"{title} Commit Activity Over Time")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(f"{repo_directory}/commit_activity.png")

    def plot_pull_requests(self, pull_requests, repository_url, repo_directory):
        data = {}
        for pr in pull_requests:
            user = pr['user']['login']
            state = pr['state']
            if user not in data:
                data[user] = {'open': 0, 'closed': 0}
            data[user][state] += 1
        # Convert data into format suitable for plotting
        labels = list(data.keys())
        open_counts = [data[user]['open'] for user in labels]
        closed_counts = [data[user]['closed'] for user in labels]
        # Plotting
        fig, ax = plt.subplots(figsize=(10,6))
        bar_width = 0.35
        index = np.arange(len(labels))
        bar1 = ax.bar(index, open_counts, bar_width, label='Open')
        bar2 = ax.bar(index+bar_width, closed_counts, bar_width, label='Closed')
        ax.set_xlabel('User')
        ax.set_ylabel('Number of PRs')
        ax.set_title(f"Pull Request Distribution for {repository_url}")
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(labels, rotation=90)
        ax.legend()
        fig.tight_layout()
        plt.grid(True)
        plt.savefig(os.path.join(repo_directory, 'pull_requests.png'))

    def plot_issues(self, issues, repository_url, repo_directory):
        open_issues = [issue for issue in issues if issue['state'] == 'open']
        users = [issue['user']['login'] for issue in open_issues]
        user_counts = Counter(users)
        if user_counts:
            users, counts = zip(*user_counts.items())
            plt.figure(figsize=(10, 6))
            plt.bar(users, counts, alpha=0.5)
            plt.title(f"Open Issue Count by User for {repository_url}")
            plt.xlabel('User')
            plt.ylabel('Number of Open Issues')
            plt.grid(True)
            plt.xticks(rotation=90)
            plt.tight_layout()
            if len(open_issues) == 0:
                plt.text(0.5, 0.5, "No open issues found", ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
            plt.savefig(os.path.join(repo_directory, 'issues.png'))
        else:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, "No open issues found", ha='center', va='center', fontsize=12, transform=plt.gca().transAxes)
            plt.axis('off')
            plt.savefig(os.path.join(repo_directory, 'issues.png'))


    '''
    def plot_issues(self, issues, repository_url, repo_directory):
        users = [issue['user']['login'] for issue in issues]
        user_counts = collections.Counter(users)
        users, counts = zip(*user_counts.items())
        plt.figure(figsize=(10,6))
        plt.bar(users, counts, alpha=0.5)
        plt.title(f"Issue Count by User for {repository_url}")
        plt.xlabel('User')
        plt.ylabel('Number of Issues')
        plt.grid(True)
        plt.xticks(rotation=90)  # This rotates the labels on the x-axis for better visibility
        plt.tight_layout()  # This ensures that the labels fit into the figure
        plt.savefig(os.path.join(repo_directory, 'issues.png'))
    '''

    def plot_languages(self, languages, repository_url, repo_directory):
        sorted_languages = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        language_names = list(sorted_languages.keys())
        loc = list(sorted_languages.values())
        plt.figure(figsize=(10,6))
        plt.bar(language_names, loc, alpha=0.5, color='green')
        plt.title(f"Lines of Code per Language for {repository_url}")
        plt.xlabel('Languages')
        plt.ylabel('Lines of Code')
        plt.grid(True)
        plt.savefig(os.path.join(repo_directory, 'languages.png'))

    def plot_releases(self, releases, repository_url, repo_directory):
        # Assuming releases is a list of dicts, with each dict containing 'created_at'
        dates = [release['created_at'] for release in releases]
        plt.figure(figsize=(10,6))
        plt.hist(dates, bins=20, alpha=0.5)
        plt.title(f"Release Frequency for {repository_url}")
        plt.xlabel('Date')
        plt.ylabel('Number of Releases')
        plt.grid(True)
        plt.savefig(os.path.join(repo_directory, 'releases.png'))

    def plot_traffic_views(self, traffic_views, repository_url, repo_directory):
        traffic_views_list = traffic_views['views']  # Access the 'views' key
        timestamps = [view['timestamp'] for view in traffic_views_list]
        counts = [view['count'] for view in traffic_views_list]
        uniques = [view['uniques'] for view in traffic_views_list]
        dates = [datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").date() for timestamp in timestamps]
        plt.figure(figsize=(10,6))
        plt.plot_date(dates, counts, linestyle='solid', marker='None')
        plt.plot_date(dates, uniques, linestyle='solid', marker='None')
        plt.title(f"Traffic Views for {repository_url}")
        plt.xlabel('Date')
        plt.ylabel('Views')
        plt.legend(['Total Views', 'Unique Views'])
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(repo_directory, 'traffic_views.png'))

    def plot_traffic_clones(self, traffic_clones, repository_url, repo_directory):
        traffic_clones_list = traffic_clones['clones']  # Access the 'clones' key
        timestamps = [clone['timestamp'] for clone in traffic_clones_list]
        counts = [clone['count'] for clone in traffic_clones_list]
        uniques = [clone['uniques'] for clone in traffic_clones_list]
        # Convert timestamps from string to datetime and extract the date
        dates = [datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").date() for timestamp in timestamps]
        plt.figure(figsize=(10,6))
        plt.plot_date(dates, counts, linestyle='solid', marker='None')
        plt.plot_date(dates, uniques, linestyle='solid', marker='None')
        plt.title(f"Traffic Clones for {repository_url}")
        plt.xlabel('Date')
        plt.ylabel('Clones')
        plt.legend(['Total Clones', 'Unique Clones'])
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(repo_directory, 'traffic_clones.png'))
