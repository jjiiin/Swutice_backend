from django.db import models

# Create your models here.
class recent_ann(models.Model):
    dept=models.CharField(max_length=25,default='')
    title=models.CharField(max_length=100,default='')
    content=models.TextField(blank=True)
    link=models.TextField(blank=True)