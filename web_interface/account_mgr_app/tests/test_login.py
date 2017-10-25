from django.test import TestCase

from django.test import Client

from account_mgr_app.models import *
from alert_config_app.models import *
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# Create your tests here.
class LoginTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usr = User.objects.create_user("test",password="testpass")
        cls.c = Client()
    
    def setUp(self):
        pass

    def test_login(self):
        """
        Ensure that the login page uses the correct templates
        """
        #self.c.login(username="test",password="testpass")
        with self.assertTemplateUsed(
                    template_name='registration/login.html'):
            response = self.c.get('/acct/login/')
            #alternative syntax
            #self.assertTemplateNotUsed(response, 'registration/login.html')
        self.c.logout()
