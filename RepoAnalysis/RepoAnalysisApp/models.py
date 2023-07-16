from django.db import models
from django.contrib.auth import get_user_model
class Scan(models.Model):    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 200, unique=True)
    class Meta():
        db_table = "user_scan"
        
class User_Scans(models.Model):
    
    scan_id = models.ForeignKey(Scan, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, unique=True)
    url_name = models.URLField(max_length = 200, unique=True)
    
    class Meta():
        db_table = "user_scaned_repo"
    