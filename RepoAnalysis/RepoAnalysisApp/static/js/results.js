async function get_data(path) {
    try {
        let response = await fetch(path)
        return await response.json()
    } catch (error) {
        console.log(error)
    }
}
async function plot_contributors(url) {
    const path = url + "contributors_graph.json"
    let data = await get_data(path)
    const x = data.map(ob => ob.login)
    const y = data.map(ob => ob.contributions)
    let plot_data = {
        x: x,
        y: y,
        type: 'bar'
    }
    let layout = {
        yaxis: {
            title: {
                text: 'contributions'
            }
        }
    }
    const contributions = document.getElementById("contributors")
    Plotly.newPlot(contributions, [plot_data], layout)
}
const formatDate = (timestamp) => {
    const date = new Date(timestamp)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}
async function plot_code_churn(url) {
    const path = url + "code_churn_over_time.json"
    let data = await get_data(path)
    const code = document.getElementById("code")
    const week = data.map(ob => formatDate(ob.additions * 1000))
    const additions = data.map(ob => ob.deletions)
    const deletions = data.map(ob => -ob.commits)
    const modifications = additions.map((val, ind) => val + deletions[ind])
    let addtion_trace = {
        x: week,
        y: additions,
        name: "addtions"
    }
    let deletion_trace = {
        x: week,
        y: deletions,
        name: "deletions"
    }
    let modification_trace = {
        x: week,
        y: modifications,
        name: "modifications"
    }
    let layout = {
        yaxis: {
            title: {
                text: 'lines of code'
            }
        }
    }
    Plotly.newPlot(code, [addtion_trace, deletion_trace, modification_trace], layout)
}
async function plot_commit(url) {
    const path = url + "commit_activity.json"
    let data = await get_data(path)
    const commit = document.getElementById("commit")
    const week = data.map(ob => formatDate(ob.week * 1000))
    const total = data.map(ob => ob.total)
    let plot_data = {
        x: week,
        y: total,
    }
    Plotly.newPlot(commit, [plot_data])
}
async function plot_pr(url) {
    const path = url + "pull_requests.json"
    let data = await get_data(path)
    const pull = document.getElementById("pull")
    const pr_data = _.countBy(data, 'user.login')
    let plot_data = {
        x: Object.keys(pr_data),
        y: Object.values(pr_data),
        type: 'bar'
    }
    Plotly.newPlot(pull, [plot_data])
}
async function plot_issues(url) {
    const path = url + "issues.json"
    let data = await get_data(path)
    const issues = document.getElementById("issues")
}
async function plot_lang(url) {
    const path = url + "languages.json"
    let data = await get_data(path)
    const lang = document.getElementById("languages")
    let plot_data = {
        labels: Object.keys(data),
        values: Object.values(data),
        type: 'pie'
    }
    Plotly.newPlot(lang, [plot_data])
}
async function plot_releases(url) {
    const path = url + "releases.json";
    let data = await get_data(path);
    const releasesContainer = document.getElementById("releases");
    if (data.length === 0) {
        releasesContainer.innerText = "No releases available for this repository.";
        return;
    }
    const releasesElement = document.createElement("div");
    releasesElement.id = "releases-plot";
    releasesContainer.appendChild(releasesElement);
    const xValues = data.map(release => release.created_at.split("T")[0]);
    const yValues = data.map(release => release.name);
    Plotly.newPlot("releases-plot", [{
        x: xValues,
        y: yValues,
        type: 'scatter',
        mode: 'lines',
        name: 'Releases',
        line: {
            color: 'rgba(0, 123, 255, 1)',
            width: 1
        }
    }]);
}
async function plot_views(url) {
    const path = url + "traffic_views.json"
    let data = await get_data(path)
    const views = document.getElementById("views")
    const view_data = data.views
    const timestamps = view_data.map(view => view.timestamp.slice(0, 10))
    const count = view_data.map(view => view.count)
    const uniques = view_data.map(view => view.uniques)
    let count_trace = {
        x: timestamps,
        y: count,
        name: 'count'
    }
    let unique_trace = {
        x: timestamps,
        y: uniques,
        name: 'uniques'
    }
    Plotly.newPlot(views, [count_trace, unique_trace])
}
window.addEventListener("DOMContentLoaded", () => {
    const repo_name = `{{repo_name}}`
    const url = document.getElementById('path').getAttribute('url')
    plot_contributors(url)
    plot_code_churn(url)
    plot_commit(url)
    plot_pr(url)
    plot_issues(url)
    plot_lang(url)
    plot_releases(url)
    plot_views(url)
    plot_clones(url)
})

function openModal(imgElement) {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("img01");

    modal.style.display = "block";
    modalImg.src = imgElement.src;

    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }
}