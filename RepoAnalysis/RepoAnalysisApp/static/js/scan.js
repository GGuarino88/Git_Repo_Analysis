$(document).ready(function ()
{
   function updateGenerateAllReportsButtonState()
   {
      const atLeastOneCheckboxChecked = $(".repoCheckbox:checked").length > 0;
      $("#generateAllReportsBtn").prop("disabled", !atLeastOneCheckboxChecked);

      if (atLeastOneCheckboxChecked)
      {
         $('#generateAllReportsBtn').css(
         {
            "background-color": "#28a745", // Green
            "color": "white"
         });
      }
      else
      {
         $('#generateAllReportsBtn').css(
         {
            "background-color": "#cccccc", // Grey
            "color": "#666666"
         });
      }
   }

   $("#selectAllCheckbox").change(function ()
   {
      $(".repoCheckbox").prop("checked", this.checked);
      updateGenerateAllReportsButtonState();
   });

   $(".repoCheckbox").change(function ()
   {
      updateGenerateAllReportsButtonState();
   });

   $("#generateAllReportsForm").on("submit", function(e) {
      e.preventDefault();
      const selectedRepos = $(".repoCheckbox:checked").map(function() {
          return $(this).val();
      }).get();
      const filteredSelectedRepos = selectedRepos.filter(Boolean);
      $("#selectedReposField").val(JSON.stringify(filteredSelectedRepos));
      $("#generateAllReportsForm input[name='team_names[]']").remove();
      $("#generateAllReportsForm input[name='project_names[]']").remove();
      $(".repoCheckbox:checked").each(function() {
          const row = $(this).closest('tr');
          const teamName = row.find('td:nth-child(2)').text().trim();
          const projectName = row.find('td:nth-child(3)').text().trim();
          $("<input>").attr({
              type: "hidden",
              name: "team_names[]",
              value: teamName
          }).appendTo("#generateAllReportsForm");
          $("<input>").attr({
              type: "hidden",
              name: "project_names[]",
              value: projectName
          }).appendTo("#generateAllReportsForm");
      });
      this.submit();
  });  
});