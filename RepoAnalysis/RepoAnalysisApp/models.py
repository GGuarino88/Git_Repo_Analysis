from django.db import models
from django.contrib.auth import get_user_model

class Semester(models.Model):    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    scan_created_at = models.DateTimeField(auto_now_add=True)
    scan_updated_at = models.DateTimeField(auto_now=True)
    
    class Meta():
        db_table = "user_semester"
        constraints = [models.UniqueConstraint(fields=['author', 'title'], name='author title constraint')]
    def __str__(self):
        return f"Semester:{self.title} - Author:{self.author}"
    
class SemesterProject(models.Model):
    scan_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    team_name = models.CharField(max_length = 200)
    repo_name = models.CharField(max_length = 200)
    url_name = models.URLField(max_length = 200)
    user_scan_created_at = models.DateTimeField(auto_now_add=True)
    user_scan_updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = "user_semester_projects"
        constraints = [
            models.UniqueConstraint(fields=['scan_id', 'repo_name'], name='scan_id_repo_name'),
            models.UniqueConstraint(fields=['scan_id', 'url_name'], name='scan_id_url_name')
        ]
    def __str__(self):
        print(self.scan_id.__str__())
        return f"Project:{self.repo_name} - {self.scan_id.__str__()}"