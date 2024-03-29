(function ()
{
   async function get_data(path)
   {
      try
      {
         var response = await fetch(path);
         var responseData = await response.json();
         // console.log("API response:", responseData) // enable while debugging
         return responseData;
      }
      catch (error)
      {
         console.log("Fetch Error:", error);
      }
   }

   async function populateRepoInfo(url, repoName)
   {
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
      privateRepoCell.textContent = data.private ? "No" : "Yes";
      repoURLCell.href = data.html_url;
      repoURLCell.textContent = data.html_url;
      repoSizeCell.textContent = data.size;
      createdAtCell.textContent = data.created_at;
      updatedAtCell.textContent = data.updated_at;
      pushedAtCell.textContent = data.pushed_at;
      createdAtCell.textContent = data.created_at.slice(0, -1).replace("T", " ");
      updatedAtCell.textContent = data.updated_at.slice(0, -1).replace("T", " ");
      pushedAtCell.textContent = data.pushed_at.slice(0, -1).replace("T", " ");
   }

   async function branchesTable(url, repoName)
   {
      const path1 = url + "repo_info.json";
      var data1 = await get_data(path1);
      const path = url + "branches.json";
      var data = await get_data(path);
      const pathCommits = url + "commits_per_branch.json";
      var commitsData = await get_data(pathCommits);
      const tableContainer = document.getElementById(`tableContainer-${repoName}`);
      const table = document.createElement("table");
      table.classList.add("table");
      const headerRow = document.createElement("tr");
      const branchNameHeader = document.createElement("th");
      branchNameHeader.textContent = "Branch Name";
      headerRow.appendChild(branchNameHeader);
      const commitsCountHeader = document.createElement("th");
      commitsCountHeader.textContent = "Commits Count";
      headerRow.appendChild(commitsCountHeader);
      const protectedHeader = document.createElement("th");
      protectedHeader.textContent = "Protected";
      headerRow.appendChild(protectedHeader);
      table.appendChild(headerRow);
      const rowsWithCommits = data.map((item) =>
      {
         const commitsCount = commitsData[item.name] || 0;
         return {
            row: createRow(item, commitsCount, data1),
            commitsCount: commitsCount
         };
      });
      rowsWithCommits.sort((a, b) => b.commitsCount - a.commitsCount);
      rowsWithCommits.forEach((rowWithCommits) =>
      {
         table.appendChild(rowWithCommits.row);
      });
      tableContainer.appendChild(table);
   }

   function createRow(item, commitsCount, data1)
   {
      const row = document.createElement("tr");
      const branchNameCell = document.createElement("td");
      const branchLink = document.createElement("a");
      branchLink.href = `${data1.html_url}/tree/${item.name}`;
      branchLink.textContent = item.name;
      branchLink.target = "_blank";
      branchNameCell.appendChild(branchLink);
      row.appendChild(branchNameCell);
      const commitsCountCell = document.createElement("td");
      commitsCountCell.textContent = commitsCount;
      row.appendChild(commitsCountCell);
      const protectedCell = document.createElement("td");
      protectedCell.textContent = item.protected;
      row.appendChild(protectedCell);
      return row;
   }

   async function plot_contributors(url, repoName)
   {
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
         xaxis:
         {
            title:
            {
               text: 'Contributors'
            }
         },
         yaxis:
         {
            title:
            {
               text: 'No. of Contributions'
            }
         },

      };
      const contributions = document.getElementById(`contributors-${repoName}`);
      Plotly.newPlot(contributions, [plot_data], layout);
   }

   async function populateContributorsTable(url, repoName)
   {
      const path = url + "contributors_graph.json";
      var data = await get_data(path);
      const contributorsTableBody = document.getElementById(`contributorsTableBody-${repoName}`);
      contributorsTableBody.innerHTML = "";
      data.forEach(contributor =>
      {
         const row = document.createElement("tr");
         const contributorCell = document.createElement("td");
         const contributorLink = document.createElement("a");
         contributorLink.href = "https://github.com/" + contributor.login;
         contributorLink.textContent = contributor.login;
         contributorLink.target = "_blank";
         contributorCell.appendChild(contributorLink);
         row.appendChild(contributorCell);
         const commitsCell = document.createElement("td");
         commitsCell.textContent = contributor.contributions;
         row.appendChild(commitsCell);
         contributorsTableBody.appendChild(row);
      });
   }

   async function plot_code_churn(url, repoName)
   {
      const path = url + "code_churn_over_time.json";
      try
      {
         var data = await get_data(path);
         if (!data)
         {
            console.error("Invalid data format: undefined");
            return;
         }
         const code = document.getElementById(`code-${repoName}`);
         const week = data.map(ob => formatDate(ob[0] * 1000));
         const additions = data.map(ob => ob[1]);
         const deletions = data.map(ob => -ob[2]);
         const modifications = additions.map((val, ind) => val + deletions[ind]);
         var addtion_trace = {
            x: week,
            y: additions,
            name: "additions",
            type: "line",
         };
         var deletion_trace = {
            x: week,
            y: deletions,
            name: "deletions",
            type: "line",
         };
         var modification_trace = {
            x: week,
            y: modifications,
            name: "modifications",
            type: "line",
         };
         var layout = {
            xaxis:
            {
               title:
               {
                  text: 'Date'
               }
            },
            yaxis:
            {
               title:
               {
                  text: 'lines of code'
               }
            }
         };
         Plotly.newPlot(code, [addtion_trace, deletion_trace, modification_trace], layout);
      }
      catch (error)
      {
         console.error("Error fetching or processing data:", error);
      }
   }

   async function populateCodeChurnTable(url, repoName)
   {
      const path = url + "code_churn_over_time.json";
      var data = await get_data(path);
      const codeChurnTableBody = document.getElementById(`codeChurnTableBody-${repoName}`);
      codeChurnTableBody.innerHTML = "";
      data.forEach(codeChurn =>
      {
         const row = document.createElement("tr");
         const timeCell = document.createElement("td");
         const additionsCell = document.createElement("td");
         const deletionsCell = document.createElement("td");
         timeCell.textContent = formatDate(codeChurn[0] * 1000);
         additionsCell.textContent = codeChurn[1];
         deletionsCell.textContent = codeChurn[2];
         row.appendChild(timeCell);
         row.appendChild(additionsCell);
         row.appendChild(deletionsCell);
         codeChurnTableBody.appendChild(row);
      });
   }

   async function plot_commit(url, repoName)
   {
      const path = url + "commit_activity.json";
      try
      {
         const data = await get_data(path);
         if (!data || data.length === 0)
         {
            console.error("Error fetching or processing data: Data is empty or undefined.", data);
            return;
         }
         const filteredData = [];
         let firstZeroSequence = true;
         for (const weekData of data)
         {
            if (firstZeroSequence && weekData.total === 0)
            {
               continue; // Skip the first sequence with total = 0
            }
            firstZeroSequence = false;
            filteredData.push(weekData);
         }
         const weekLabels = filteredData.map((weekData) =>
         {
            const date = new Date(weekData.week * 1000);
            return formatDate(date);
         });
         const commit = document.getElementById(`commit-${repoName}`);
         const week = filteredData.map((weekData) => formatDate(weekData.week * 1000));
         const total = filteredData.map((weekData) => weekData.total);
         var plot_data = {
            x: week,
            y: total,
         };
         var layout = {
            xaxis: {
               title: 'Date',
            },
            yaxis: {
               title: 'Count of Commits'
            }
         };
         Plotly.newPlot(commit, [plot_data], layout);
      }
      catch (error)
      {
         console.error("Error fetching or processing data:", error);
      }
   }

   async function plot_pr(url, repoName)
   {
      const path = url + "pull_requests.json";
      var data = await get_data(path);
      const pull = document.getElementById(`pull-${repoName}`);
      if (!data || data.length === 0)
      {
         const noPRMessage = document.createElement("h3");
         noPRMessage.textContent = "No PR's are made to this repository.";
         pull.appendChild(noPRMessage);
         return;
      }
      const pr_data = _.countBy(data, 'user');
      var plot_data = {
         x: Object.keys(pr_data),
         y: Object.values(pr_data),
         type: 'line'
      };
      var layout = {
         xaxis: {
            title: 'user',
         },
         yaxis: {
            title: 'Count of Pull Requests'
         }
      };
      Plotly.newPlot(pull, [plot_data], layout);
   }

   async function plot_lang(url, repoName)
   {
      const path = url + "languages.json";
      var data = await get_data(path);
      const langTableBody = document.getElementById(`languagesTableBody-${repoName}`);
      const langChart = document.getElementById(`languagesChart-${repoName}`);
      langTableBody.innerHTML = "";
      langChart.innerHTML = "";
      Object.entries(data).forEach(([language, total]) =>
      {
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
   const formatDate = (timestamp) =>
   {
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
   }

   async function plot_releases(url, repoName)
   {
      const path = url + "releases.json";
      var data = await get_data(path);
      const releasesContainer = document.getElementById(`releasesContainer-${repoName}`);
      releasesContainer.innerHTML = "";
      if (!data || data.length === 0)
      {
         const noReleasesMessage = document.createElement("h3");
         noReleasesMessage.textContent = "No releases are created on this repository.";
         releasesContainer.appendChild(noReleasesMessage);
         return;
      }
      const table = document.createElement("table");
      table.className = "table";
      const thead = document.createElement("thead");
      const tr = document.createElement("tr");
      const headers = ["Released On", "Name", "Tag Name", "Message"];
      headers.forEach(header =>
      {
         const th = document.createElement("th");
         th.textContent = header;
         tr.appendChild(th);
      });
      thead.appendChild(tr);
      table.appendChild(thead);
      const tbody = document.createElement("tbody");
      tbody.id = `releasesTableBody-${repoName}`;
      table.appendChild(tbody);
      data.forEach(release =>
      {
         const row = document.createElement("tr");
         const createdAtCell = document.createElement("td");
         const nameCell = document.createElement("td");
         const tagNameCell = document.createElement("td");
         const bodyCell = document.createElement("td");
         createdAtCell.textContent = release.created_at.slice(0, -1).replace("T", " ");
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
   window.addEventListener("DOMContentLoaded", () =>
   {
      const repoElements = document.querySelectorAll(".repo-info");
      for (let i = 0; i < repoElements.length; i++)
      {
         const repoName = repoElements[i].getAttribute("name");
         const url = document.getElementById(`path-${repoName}`).getAttribute('url')
         populateRepoInfo(url, repoName)
         branchesTable(url, repoName)
         plot_contributors(url, repoName)
         populateContributorsTable(url, repoName)
         plot_code_churn(url, repoName)
         populateCodeChurnTable(url, repoName)
         plot_commit(url, repoName)
         plot_pr(url, repoName)
         plot_lang(url, repoName)
         plot_releases(url, repoName)
      }
   })

   function openModal(imgElement)
   {
      var modal = document.getElementById("myModal");
      var modalImg = document.getElementById("img01");
      modal.style.display = "block";
      modalImg.src = imgElement.src;
      var span = document.getElementsByClassName("close")[0];
      span.onclick = function ()
      {
         modal.style.display = "none";
      }
   }
})();