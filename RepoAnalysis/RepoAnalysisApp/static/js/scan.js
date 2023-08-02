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

   $("#generateAllReportsForm").on("submit", function (e)
   {
      e.preventDefault();
      const selectedRepos = $(".repoCheckbox:checked").map(function ()
      {
         return $(this).val();
      }).get();
      const filteredSelectedRepos = selectedRepos.filter(Boolean);
      $("#selectedReposField").val(JSON.stringify(filteredSelectedRepos));
      this.submit();
   });
});