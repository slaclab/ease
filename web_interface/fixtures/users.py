from account_mgr_app.models import *
from alert_config_app.models import *
from django.contrib.auth.models import User

'''
use this document to run the imports in django shell.
'''

a = User.objects.create_user("test0",password="test")
a.save()

b = User.objects.create_user("test1",password="test")
b.save()
