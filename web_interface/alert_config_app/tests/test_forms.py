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


class test_config_Alert_form(TestCase):
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
                    "FAKE_USERNAME, "
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

    def test_parse_usernames(self):
        """Ensure that the parse_usernames method properly extracts usernames
        from possible input strings
        """
        data = "username"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["username"]),
            "unable to handle single username-only entries"
        )

        data = "username1,username2,username3"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["username1","username2","username3"]),
            "unable to handle multiple, username-only entries"
        )
        
        data = "username (first, last)"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["username"]),
            "unable to handle single username w/ name"
        )

        data = "user1(first,last),user2 (  first,last),user3 (first, last)"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["user1","user2","user3"]),
            "unable to handle multiple, username-only entries"
        )

        data = "user1(first, last   ),user2  ,user3 ( first, last)"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["user1","user2","user3"]),
            "unable to handle multiple, mixed-type entries"
        )
        
        data = "user1(first, last   ),user2 , ,user3 ( first, last)"
        result = configAlert.parse_usernames(data)
        self.assertEqual(
            result,
            set(["user1","user2","user3"]),
            "unable to scrub blank (bad) entires"
        )




class test_detail_Alert_form(TestCase):
    """Collection of tests inspecting the detail_alert form 
    """

    @classmethod
    def setUpTestData(cls):
        """Create a collection of users and alerts for this TestCase
        """
        cls.primary = User.objects.create_user("testA")
        cls.primary_pass = "tests"
        cls.primary.set_password(cls.primary_pass)
        cls.primary.save()
        
        cls.secondary = User.objects.create_user("testB")
        cls.secondary_pass = "tests"
        cls.secondary.set_password(cls.secondary_pass)
        cls.secondary.save()

        cls.c = Client()

        cls.alert = Alert()
        cls.alert.name = "test alert"
        cls.alert.save()
        cls.alert.owner.add(cls.primary.profile)
        cls.alert.save()
    
    def setUp(self):
        """Log the test user in before each test method.
        """
        self.c.login(
           username = self.primary.username,
           password = self.primary_pass)

    def test_clean_new_subscribe(self):
        """Ensure that the cleaner for the new_subscribe field errs properly
        """
        # Ensure that subscription is handled properly
        form = detailAlert(
            data = {
                'new_subscribe' : 'on',
            }
        )
        errors = form['new_subscribe'].errors.as_data()
        self.assertFalse(
            len(errors),
            "Errors should not have been reported",
        )
        self.assertTrue(
            form.cleaned_data['new_subscribe'],
            "True value not reported",
        )

        # Ensure that unsubscription is handled properly
        form = detailAlert(data = {})
        errors = form['new_subscribe'].errors.as_data()
        self.assertFalse(
            len(errors),
            "Errors should not have been reported",
        )
        self.assertFalse(
            form.cleaned_data['new_subscribe'],
            "False value not reported",
        )

