(function () {
   async function get_data(path) {
      try {
         var response = await fetch(path)
         return await response.json()
      } catch (error) {
         console.log(error)
      }
   }
   async function populateRepoInfo(url,repoName) {
      const path = url + "repo_info.json";
      var data = await get_data(path);
      const repoIdCell = document.getElementById(`repoId-${repoName}`);
      const repoNameCell = document.getElementById(`repoName-${repoName}`);
      const privateRepoCell = document.getElementById(`privateRepo-${repoName}`);
      const repoURLCell = document.getElementById(`repoLink-${repoName}`);
      const repoSizeCell = document.getElementById(`repoSize-${repoName}`);
      const createdAtCell = document.getElementById(`created_at-${repoName}`);
      const updatedAtCell = document.getElementById(`updated_at-${repoName}`);
      const pushedAtCell = document.getElementById(`pushed_at-${repoName}`);
      repoIdCell.textContent = data.id;
      repoNameCell.textContent = data.full_name;
      privateRepoCell.textContent = data.private;
      repoURLCell.href = data.html_url;
      repoURLCell.textContent = data.html_url;
      repoSizeCell.textContent = data.size;
      createdAtCell.textContent = data.created_at;
      updatedAtCell.textContent = data.updated_at;
      pushedAtCell.textContent = data.pushed_at;
   }
   async function plot_contributors(url,repoName) {
      const path = url + "contributors_graph.json";
      var data = await get_data(path);
      const x = data.map(ob => ob.login);
      const y = data.map(ob => ob.contributions);
      var plot_data = {
         x: x,
         y: y,
         type: 'bar'
      };
      var layout = {
         xaxis: {
            title: {
               text: 'Contributors'
            }
         },
         yaxis: {
            title: {
               text: 'No. of Contributions'
            }
         }
      };
      const contributions = document.getElementById(`contributors-${repoName}`);
      Plotly.newPlot(contributions, [plot_data], layout);
   }
   async function populateContributorsTable(url, repoName) {
      const path = url + "contributors_graph.json";
      var data = await get_data(path);
      const contributorsTableBody = document.getElementById(`contributorsTableBody-${repoName}`);
      contributorsTableBody.innerHTML = "";
      data.forEach(contributor => {
         const row = document.createElement("tr");
         const contributorCell = document.createElement("td");
         const commitsCell = document.createElement("td");
         contributorCell.textContent = contributor.login;
         commitsCell.textContent = contributor.contributions;
         row.appendChild(contributorCell);
         row.appendChild(commitsCell);
         contributorsTableBody.appendChild(row);
      });
   }
   async function populateCodeChurnTable(url, repoName) {
      const path = url + "code_churn_over_time.json";
      var data = await get_data(path);
      const codeChurnTableBody = document.getElementById(`codeChurnTableBody-${repoName}`);
      codeChurnTableBody.innerHTML = "";
      data.forEach(codeChurn => {
         const row = document.createElement("tr");
         const timeCell = document.createElement("td");
         const additionsCell = document.createElement("td");
         const deletionsCell = document.createElement("td");
         const modificationsCell = document.createElement("td");
         timeCell.textContent = formatDate(codeChurn.additions * 1000);
         additionsCell.textContent = codeChurn.additions;
         deletionsCell.textContent = codeChurn.deletions;
         modificationsCell.textContent = codeChurn.additions + codeChurn.deletions;
         row.appendChild(timeCell);
         row.appendChild(additionsCell);
         row.appendChild(deletionsCell);
         row.appendChild(modificationsCell);
         codeChurnTableBody.appendChild(row);
      });
   }
   async function plot_lang(url, repoName) {
      const path = url + "languages.json";
      var data = await get_data(path);
      const langTableBody = document.getElementById(`languagesTableBody-${repoName}`);
      const langChart = document.getElementById(`languagesChart-${repoName}`);
      langTableBody.innerHTML = "";
      langChart.innerHTML = "";
      Object.entries(data).forEach(([language, total]) => {
         const row = document.createElement("tr");
         const languageCell = document.createElement("td");
         const totalCell = document.createElement("td");
         languageCell.textContent = language;
         totalCell.textContent = total;
         row.appendChild(languageCell);
         row.appendChild(totalCell);
         langTableBody.appendChild(row);
      });
      var plot_data = {
         labels: Object.keys(data),
         values: Object.values(data),
         type: 'pie'
      };
      Plotly.newPlot(langChart, [plot_data]);
   }
   const formatDate = (timestamp) => {
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
   }
   async function plot_code_churn(url, repoName) {
      const path = url + "code_churn_over_time.json";
      var data = await get_data(path);
      const code = document.getElementById(`code-${repoName}`);
      const week = data.map(ob => formatDate(ob.additions * 1000));
      const additions = data.map(ob => ob.deletions);
      const deletions = data.map(ob => -ob.commits);
      const modifications = additions.map((val, ind) => val + deletions[ind]);
      var addtion_trace = {
         x: week,
         y: additions,
         name: "addtions"
      }
      var deletion_trace = {
         x: week,
         y: deletions,
         name: "deletions"
      }
      var modification_trace = {
         x: week,
         y: modifications,
         name: "modifications"
      }
      var layout = {
         xaxis: {
            title: {
               text: 'Date'
            }
         },
         yaxis: {
            title: {
               text: 'lines of code'
            }
         }
      }
      Plotly.newPlot(code, [addtion_trace, deletion_trace, modification_trace], layout)
   }
   async function plot_commit(url, repoName) {
      const path = url + "commit_activity.json"
      var data = await get_data(path)
      const commit = document.getElementById(`commit-${repoName}`)
      const index = _.findIndex(data, (ob) => ob.total > 0)
      const week = data.slice(index).map(ob => formatDate(ob.week * 1000))
      const total = data.slice(index).map(ob => ob.total)
      var plot_data = {
         x: week,
         y: total,
      }
      Plotly.newPlot(commit, [plot_data])
   }
   async function plot_pr(url, repoName) {
      const path = url + "pull_requests.json";
      var data = await get_data(path);
      const pull = document.getElementById(`pull-${repoName}`);
      
      if (!data || data.length === 0) {
        const noPRMessage = document.createElement("h3");
        noPRMessage.textContent = "No PR's are made to this repository.";
        pull.appendChild(noPRMessage);
        return;
      }
    
      const pr_data = _.countBy(data, 'user.login');
      var plot_data = {
        x: Object.keys(pr_data),
        y: Object.values(pr_data),
        type: 'bar'
      };
    
      Plotly.newPlot(pull, [plot_data]);
    }    
   async function plot_releases(url, repoName) {
      const path = url + "releases.json";
      var data = await get_data(path);
      const releasesContainer = document.getElementById(`releasesContainer-${repoName}`);
      releasesContainer.innerHTML = "";

      if (!data || data.length === 0) {
          const noReleasesMessage = document.createElement("h3");
          noReleasesMessage.textContent = "No releases are created on this repository.";
          releasesContainer.appendChild(noReleasesMessage);
          return;
      }
      
      const table = document.createElement("table");
      table.className = "table";
      const thead = document.createElement("thead");
      const tr = document.createElement("tr");
      const headers = ["Created At", "Name", "Tag Name", "Message"];
      headers.forEach(header => {
          const th = document.createElement("th");
          th.textContent = header;
          tr.appendChild(th);
      });
      thead.appendChild(tr);
      table.appendChild(thead);
      const tbody = document.createElement("tbody");
      tbody.id = `releasesTableBody-${repoName}`;
      table.appendChild(tbody);
      data.forEach(release => {
          const row = document.createElement("tr");
          const createdAtCell = document.createElement("td");
          const nameCell = document.createElement("td");
          const tagNameCell = document.createElement("td");
          const bodyCell = document.createElement("td");
  
          createdAtCell.textContent = release.created_at;
          nameCell.textContent = release.name;
          tagNameCell.textContent = release.tag_name;
          bodyCell.textContent = release.body;
  
          row.appendChild(createdAtCell);
          row.appendChild(nameCell);
          row.appendChild(tagNameCell);
          row.appendChild(bodyCell);
          tbody.appendChild(row);
      });
  
      releasesContainer.appendChild(table);
  } 
   async function plot_views(url, repoName) {
      const path = url + "traffic_views.json"
      var data = await get_data(path)
      const views = document.getElementById(`views-${repoName}`)
      const view_data = data.views
      const timestamps = view_data.map(view => view.timestamp.slice(0, 10))
      const count = view_data.map(view => view.count)
      const uniques = view_data.map(view => view.uniques)
      var count_trace = {
         x: timestamps,
         y: count,
         name: 'count'
      }
      var unique_trace = {
         x: timestamps,
         y: uniques,
         name: 'uniques'
      }
      Plotly.newPlot(views, [count_trace, unique_trace])
   }
   window.addEventListener("DOMContentLoaded", () => {
      const repoElements = document.querySelectorAll(".repo-info");
      for(let i = 0; i < repoElements.length; i++){
         const repoName = repoElements[i].getAttribute("name");
         const url = document.getElementById(`path-${repoName}`).getAttribute('url')

         populateRepoInfo(url,repoName)
         plot_contributors(url, repoName)
         populateContributorsTable(url, repoName)
         plot_code_churn(url, repoName)
         populateCodeChurnTable(url, repoName)
         plot_commit(url, repoName)
         plot_pr(url, repoName)
         plot_lang(url, repoName)
         plot_releases(url, repoName)
         plot_views(url, repoName)

      }
   })
   
   function openModal(imgElement) {
      var modal = document.getElementById("myModal");
      var modalImg = document.getElementById("img01");

      modal.style.display = "block";
      modalImg.src = imgElement.src;

      var span = document.getElementsByClassName("close")[0];

      span.onclick = function () {
         modal.style.display = "none";
      }
   }
})();