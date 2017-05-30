from django.db import models

# Create your models here.



class Alarm(models.Model):
    name = models.CharField(max_length=100)

class Pv(models.Model):
    name = models.CharField(max_length=100)

    
