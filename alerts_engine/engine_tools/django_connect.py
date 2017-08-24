"""
Initiate connection with the django features. The prepare function must be run
before imports from django files (e.g. models) can be used. Avoid editing this
document as it stands to break a lot of scripts.
"""


import sys, os
    
import django
def prepare():
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.realpath(__file__),
                os.pardir,
                os.pardir,
                os.pardir,
                "web_interface"
            )
        )
    )
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'web_interface.settings'
    django.setup()
    
    
    #from alert_config_app.models import *

if __name__ == '__main__':
    prepare()
    from alert_config_app.models import *
