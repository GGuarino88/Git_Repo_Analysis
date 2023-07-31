document.addEventListener('DOMContentLoaded', function() {
    const repositoryUrlInput = document.getElementById(window.url_name_id);
    const generateReportBtn = document.getElementById('generateReportBtn');
    repositoryUrlInput.addEventListener('input', function () {
       const isValidUrl = validateRepositoryUrl(repositoryUrlInput.value);
       generateReportBtn.disabled = !isValidUrl;
       generateReportBtn.value = isValidUrl ? 'Validate' : 'Submit';
    });
    
    function validateRepositoryUrl(url) {
       const regex = /^(https?:\/\/)?(www\.)?github\.com\/[^\s\/]+\/[^\s\/]+$/;
       return regex.test(url);
    }
    if (repositoryUrlInput.value) {
       generateReportBtn.disabled = !validateRepositoryUrl(repositoryUrlInput.value);
       generateReportBtn.value = generateReportBtn.disabled ? 'Submit' : 'Validate';
    }
    let isFormSubmitted = false;
    $('#repositoryForm').on('submit', function (e) {
       if (!isFormSubmitted) {
          e.preventDefault();
          const repositoryUrl = repositoryUrlInput.value;
          const isValidUrl = validateRepositoryUrl(repositoryUrl);
          if (isValidUrl) {
             checkRepositoryExists(repositoryUrl);
          } else {
             alert('Invalid repository URL');
          }
       } else {
          isFormSubmitted = false;
       }
    });
    
    function checkRepositoryExists(repositoryUrl) {
       const strippedUrl = repositoryUrl.replace(/^(https?:\/\/)?(www\.)?github\.com\//, '');
       const apiUrl = `https://api.github.com/repos/${strippedUrl}`;
       $.ajax({
          url: apiUrl,
          type: 'GET',
          success: function (response) {
             console.log('Repository exists:', repositoryUrl);
             generateReportBtn.disabled = false;
             generateReportBtn.value = 'Submit';
             $('#repositoryForm').submit();
             isFormSubmitted = true;
          },
          error: function (xhr, status, error) {
             console.log('Repository does not exist:', repositoryUrl);
             generateReportBtn.value = 'Validate';
             alert('The repository does not exist.');
          }
       });
    }
});