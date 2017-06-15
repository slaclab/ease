import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),os.pardir,os.pardir,"web_interface")))

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_interface.settings'
django.setup()

from alert_config_app.models import *


for x in Alert.objects.all():
    print("\n--+",x)
    for y in x.trigger_set.all():
        print('  |-->',y)

