$(document).ready(function() {
    $("#selectAllCheckbox").change(function() {
        $(".repoCheckbox").prop("checked", this.checked);
        updateGenerateAllReportsButtonState();
    });
    $(".repoCheckbox").change(function() {
        updateGenerateAllReportsButtonState();
    });
    function updateGenerateAllReportsButtonState() {
        const atLeastOneCheckboxChecked = $(".repoCheckbox:checked").length > 0;
        $("#generateAllReportsBtn").prop("disabled", !atLeastOneCheckboxChecked);
    }
    $("#generateAllReportsForm").on("submit", function(e) {
        e.preventDefault();
        const selectedRepos = $(".repoCheckbox:checked").map(function() {
            return $(this).val();
        }).get();
        const filteredSelectedRepos = selectedRepos.filter(Boolean);
        $("#selectedReposField").val(JSON.stringify(filteredSelectedRepos));
        this.submit();
    });
});