import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
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
        dates = [datetime.datetime.fromtimestamp(week) for week in weeks]
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
        weeks = [datetime.datetime.fromtimestamp(data["week"]).strftime('%Y-%m-%d') for data in commit_activity]
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