"""
Contains TriggerScan, the task to be run at regular intervals.
"""

############
# Standard #
############
import logging
import sys
import os

###############
# Third Party #
###############
import archapp

##########
# Custom #
##########
#import django_connect
#from .django_connect import prepare
from . import django_connect

#################
# Configuration #
#################
logger = logging.getLogger(__name__)
django_connect.prepare()
from alert_config_app.models import *
from account_mgr_app.models import *



def test_db():
    """
    teset db connection by scanning models in the config_app. Only intended for
    diagnostic use
    """
    #print("testing")
    for x in Alert.objects.all():
        print("\n--+",x)
        for y in x.trigger_set.all():
            print('  |-->',y)


class TriggerScan:
    def __init__(self):
        #timing info etc probs useful
        pass

    def dbPvPull(self,live=True):
        """
        Return list of relevant PVs. 

        Parameters
        ----------
        live : bool
            If true, filter the pvs to only those with triggers. Defaults to
            true.

        Returns
        -------
        django.db.models.query.QuerySet (Pv type)

        """
        if live:
            return Pv.objects.filter(trigger__isnull=False)
        else:
            return Pv.objects.all()

    def filterLivePvs(self):
        #remove PVs which have no living alerts, return remaining []
        #don't need this
        pass

    def archPull(self):
        #acquire, return [] necessary data from archiver 
        pass

    def compare(self):
        #examine 1 pv for violations 
        pass


if __name__ == '__main__':
    test_db()
