from django.test import TestCase, LiveServerTestCase
from unittest import skip, skipIf, skipUnless
import unittest
import os
from selenium import webdriver
from alert_config_app.models import Alert, Trigger
from account_mgr_app.models import Profile
from django.contrib.auth.models import User
import logging
import time
#from selenium.webdriver.firefox.webdriver import WebDriver

webdriver_path = os.path.join(os.getcwd(),"geckodriver")

logging.disable(logging.CRITICAL)

@unittest.skip("Selenium tests not yet implemented")
@skipUnless(
    os.path.isfile(webdriver_path),
    "Webdriver executable required for UI testing")
class SeleniumViewTests(LiveServerTestCase):
    '''I'm keeping this around as a template for other tests
    '''
    @classmethod
    def setUpTestData(cls):
        cls.primary = User.objects.create_user("test1")
        cls.primary_pass = "tests"
        cls.primary.set_password(cls.primary_pass)
        cls.primary.save()

        cls.secondary = User.objects.create_user("test2")
        cls.secondary_pass = "tests"
        cls.secondary.set_password(cls.secondary_pass)
        cls.secondary.save()

        
        cls.alerts = []
        for x in range(10):
            cls.alerts.append(Alert())
            cls.alerts[x].name = "alert_"+str(x)
            cls.alerts[x].save()
            if x == 0:
                cls.alerts[x].owner.add(cls.primary.profile)
            
            if x == 1:
                cls.alerts[x].owner.add(cls.secondary.profile)
            
            if x == 2:
                cls.alerts[x].owner.add(cls.primary.profile)
                cls.alerts[x].owner.add(cls.secondary.profile)
             
                
            cls.alerts[x].save() 

        cls.factory = RequestFactory()
        cls.c = Client()
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.wdriver = webdriver.Firefox(executable_path=webdriver_path)
        # how long to wait for a DOM object before giving up. 
        cls.wdriver.implicitly_wait(10)
        
    
    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        #cls.selenium.quit()
        cls.wdriver.close()

        super().tearDownClass()

    def tearDown(self):
        #Clean up run after every test method.
        pass
    
    def test_visit_page(self):
        self.wdriver.get(
            '{}{}'.format(
                self.live_server_url,
                '/accounts/login/'
            )
        )

