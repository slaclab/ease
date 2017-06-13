from django.db import models

# Create your models here.



class Alert(models.Model):
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)

    def __repr__(self):
        return "{}(name={},)".format(self.__class__.__name__, self.name)

    def __str__(self):
        return(str(self.name))

class Pv(models.Model):
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)

    def __repr__(self):
        return "{}(name={},)".format(self.__class__.__name__, self.name)

    def __str__(self):
        return(str(self.name))

class Trigger(models.Model):
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)

    def __repr__(self):
        return "{}(name={},alert={})".format(self.__class__.__name__, self.name, self.alert)

    def __str__(self):
        return(str(self.name))

    
