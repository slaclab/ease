from django.db import models

# Create your models here.



class Alarm(models.Model):
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)

class Pv(models.Model):
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)

    
