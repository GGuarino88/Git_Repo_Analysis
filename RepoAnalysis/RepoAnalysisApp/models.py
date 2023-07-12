from django.db import models
from django.contrib.auth import get_user_model

class Scan(models.Model):
    
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(max_length=200)
    
    class Meta():
        db_table = "user_scan"
    