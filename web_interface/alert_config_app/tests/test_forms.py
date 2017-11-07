from django.test import TestCase, RequestFactory, Client
from unittest import skip

from alert_config_app.models import *
from alert_config_app.forms import *
from account_mgr_app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your tests here.
# @skip("Keeping this as an example template")
class test_configTrigger_form(TestCase):
    '''Collection of tests inspecting the configTrigger form.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.primary = User.objects.create_user("testB")
        cls.primary_pass = "tests"
        cls.primary.set_password(cls.primary_pass)
        cls.primary.save()       
        cls.c = Client()

        cls.alert = Alert()
        cls.alert.name = "test alert"
        cls.alert.save()
        cls.alert.owner.add(cls.primary.profile)
        cls.alert.save()

    @classmethod 
    def setUpClass(cls):
        super().setUpClass()
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        pass

    def setUp(self):
        """Log the test user in before each test method.
        """
        self.c.login(
           username = self.primary.username,
           password = self.primary_pass)

    def tearDown(self):
        """Log the test user out after every test method.
        """
        self.c.logout()

    def test_single_form_rejection(self):
        """ensure that singular triggers will fail -- currently a blank test
        """
        form = configTrigger(
            data = {
                'new_pv' : None,
                'new_compare' : None,
                'new_name' : 'trigger name',
                'new_value' : None,})


class test_configAlert_form(TestCase):
    '''Collection of tests inspecting the configAlert form.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.primary = User.objects.create_user("testA")
        cls.primary_pass = "tests"
        cls.primary.set_password(cls.primary_pass)
        cls.primary.save()       
        cls.c = Client()

        cls.alert = Alert()
        cls.alert.name = "test alert"
        cls.alert.save()
        cls.alert.owner.add(cls.primary.profile)
        cls.alert.save()

    @classmethod 
    def setUpClass(cls):
        super().setUpClass()
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        pass

    def setUp(self):
        """Log the test user in before each test method.
        """
        self.c.login(
           username = self.primary.username,
           password = self.primary_pass)

    def tearDown(self):
        """Log the test user out after every test method.
        """
        self.c.logout() 
     
    def test_Alert_must_have_name(self):
        """ensure that alerts throw errors when they lack names
        """

        # name is none
        form = configAlert(
            data = {
                'new_owners' : str(self.primary.username),
                'new_name' : None,
                'new_subscribe' : 'on', #as opposed to None
                'new_lockout_duration' : None})
            
        errors = form['new_name'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertFalse(form.is_valid())
        
        # name not provided 
        form = configAlert(
            data = {
                'new_owners' : str(self.primary.username),
                'new_subscribe' : 'on', #as opposed to None
                'new_lockout_duration' : None})
            
        errors = form['new_name'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertFalse(form.is_valid())   

        # name too short
        form = configAlert(
            data = {
                'new_owners' : str(self.primary.username),
                'new_name' : "",
                'new_subscribe' : 'on', #as opposed to None
                'new_lockout_duration' : None})
            
        errors = form['new_name'].errors.as_data()
        self.assertEqual(len(errors), 1)
        self.assertFalse(form.is_valid())
    
    def test_clean_new_owners(self):
        """Ensure that clean_new_owners properly errs on bad names
        """

        # Ensure that errors are reported for bad owner inputs
        form = configAlert(
            data = {
                'new_owners' : 
                    str(self.primary.username)+", "+
                    "FAKE_USERNAME"
                ,
                'new_name' : "sample name",
                'new_subscribe' : 'on', #as opposed to None
                'new_lockout_duration' : None
            }
        )   

        form_errors = form.errors.as_data()
        
        self.assertTrue(
            len(form.errors.as_data()) > 0,
            "No Errors Reported"
        )

        self.assertEqual(
            ValidationError,
            type(form.errors.as_data()['new_owners'][0]),
            "Wrong error type"
        )

        self.assertTrue(
            "FAKE_USERNAME" in form.errors.as_data()['new_owners'][0].message,
            "error message failed to report bad name"
        )
        
        # Ensure that no errors are reported for good owner inputs 
        form = configAlert(
            data = {
                'new_owners' : str(self.primary.username),
                'new_name' : "sample name",
                'new_subscribe' : 'on', #as opposed to None
                'new_lockout_duration' : None
            }
        )   

        self.assertEqual(
            len(form.errors.as_data()),
            0,
            "No Errors Reported"
        )

        self.assertTrue(
            self.primary.profile in form.cleaned_data['new_owners'],
            "Profile not returned"
        )
