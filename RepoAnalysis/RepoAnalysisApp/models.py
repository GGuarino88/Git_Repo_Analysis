from django.db import models
from django.contrib.auth import get_user_model
class Scan(models.Model):    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    scan_created_at = models.DateTimeField(auto_now_add=True)
    scan_updated_at = models.DateTimeField(auto_now=True)
    class Meta():
        db_table = "user_scan"
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'], name='author title constraint')
        ]
    def __str__(self):
        return f"{self.title} {self.author}"
class User_Scans(models.Model):
    scan_id = models.ForeignKey(Scan, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    url_name = models.URLField(max_length = 200)
    user_scan_created_at = models.DateTimeField(auto_now_add=True)
    user_scan_updated_at = models.DateTimeField(auto_now=True)
    class Meta():
        db_table = "user_scaned_repo"
        constraints = [
            models.UniqueConstraint(fields=['scan_id', 'name'], name='scan_id_repo_name'),
            models.UniqueConstraint(fields=['scan_id', 'url_name'], name='repo_name_url_name')
        ]
    def __str__(self):
        return f"{self.name}"
