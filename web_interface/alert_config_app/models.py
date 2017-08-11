"""Manage alert_config data models
"""
from django.db import models
from django.urls import reverse
from account_mgr_app.models import Profile

# Create your models here.

class Alert(models.Model):
    """This model represents EASE's alerts

    The Alert relates a collection of triggers to subscribers and owners.
    It is inteded to be directly editable by all users who are owners.
    When a linked trigger is tripped, alerts are sent to the subscribed
    users.
    """
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)
    subscriber = models.ManyToManyField(
        Profile,
        related_name="subscriptions"
    )
    owner = models.ManyToManyField(
        Profile,
        related_name=None
    )
    
    lockout_duration = models.DurationField(
        blank = True,
        null = True,
    )

    last_sent = models.DateTimeField(
        blank = True,
        null = True,
    )

    def __repr__(self):
        # attempting to print subscriber and owner leads to infinite recursive loop
        return "{}( name={})".format(
            self.__class__.__name__,
            self.name,
        )

    def __str__(self):
        return(str(self.name))


class Pv(models.Model):
    """Each PV instance is made to match with an EPICS PV.

    Alerts engine consults the table of PVs to decide which
    entries much be queried from the archiver
    """
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)
    

    def __repr__(self):
        return "{}(name={},)".format(self.__class__.__name__, self.name)

    def __str__(self):
        return(str(self.name))


class Trigger(models.Model):
    """Individual 'trip statemet'
    
    Each trigger defines a trip condition relating a numeric value, condition 
    and PV. Each trigger can be owned by a single Alert. Triggers are not
    edited directly but through the alerts config page.
    """
    name_max_length = 100
    name = models.CharField(max_length = name_max_length)
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE)
    pv = models.ForeignKey(
        Pv,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    
    value = models.FloatField(
        blank = True,
        null = True,
    )

    compare_choices = [
        ('==','=='),
        ('<=','<='),
        ('>=','>='),
        ('<','<'),
        ('>','>'),
        ('!=','!='),
    ]

    compare = models.CharField(
        choices = compare_choices,
        max_length = 2,
        blank = True,
        null = True,
    ) 


    def __repr__(self):
        return "{}(name={},alert={},value={},compare={})".format(
            self.__class__.__name__, 
            self.name, 
            self.alert,
            self.value,
            self.compare,
        )

    def __str__(self):
        return(str(self.name))

