from django.test import TestCase, RequestFactory, Client
from unittest import skip

import alert_config_app.views as views
from alert_config_app.models import *
from account_mgr_app.models import *
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

# Create your tests here.
# @skip("Keeping this as an example template")
class test_alert_config_form(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.primary = User.objects.create_user("test")
        cls.primary_pass = "tests"
        cls.primary.set_password(cls.primary_pass)
        cls.primary.save()

        cls.secondary = User.objects.create_user("test2")
        cls.secondary_pass = "tests"
        cls.secondary.set_password(cls.secondary_pass)
        cls.secondary.save()

        
        cls.alerts = []
        for x in range(2):
            cls.alerts.append(Alert())
            cls.alerts[x].name = "alert_"+str(x)
            cls.alerts[x].save()
            cls.alerts[x].owner.add(cls.primary.profile)
            cls.alerts[x].save() 

        cls.factory = RequestFactory()
        cls.c = Client()

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

    def test_create_exists(self):
        """Test that the creation page can be drawn without errors.
        """
        self.c.login(
            username = self.primary.username,
            password = self.primary_pass)
        response = self.c.get('/alert/alert_create/',follow=True)
        self.assertEqual(response.status_code, 200)

    def test_config_exists(self):
        """Test that the configuration pages can be drawn without errors.
        """
        self.c.login(
            username = self.primary.username,
            password = self.primary_pass)
        
        for single_alert in self.alerts:
            pk = single_alert.pk
            response = self.c.get(
                '/alert/alert_config/'+str(pk)+'/',
                follow=True)
            self.assertEqual(response.status_code, 200)
        self.c.logout()

    def test_config_bad_pk(self):
        """Ensure that the user is redirected after providing a bad pk value
        """
        bad_pk = 9001
        response = self.c.get('/alert/alert_config/'+str(bad_pk)+'/',
                follow=True)
        self.assertTrue(
            (reverse('alert_create'), 302) in response.redirect_chain)
        self.assertNotEqual(len(response.redirect_chain),0)

    def test_login_create(self):
        """Ensure that these pages cannot be provided to logged-out users
        """
        self.c.logout()
        response = self.c.get('/alert/alert_create/',follow=True)
        self.assertNotEqual(len(response.redirect_chain),0)

    def test_login_create(self):
        """Ensure that these pages cannot be provided to logged-out users
        """
        self.c.logout()
        for single_alert in self.alerts:
            pk = single_alert.pk
            response = self.c.get(
                '/alert/alert_config/'+str(pk)+'/',
                follow=True)
            self.assertNotEqual(len(response.redirect_chain),0)

    def test_create_template_usage(self):
        """Ensure that the creation page loads the proper templates
        """
        with self.assertTemplateUsed('alert_config.html'):
            response = self.c.get('/alert/alert_create/',follow=True)

    def test_config_template_usage(self):
        """Ensure that the config  page loads the proper templates.
        """
        for single_alert in self.alerts:
            pk = single_alert.pk
            response = self.c.get(
                '/alert/alert_config/'+str(pk)+'/',
                follow=True)

            self.assertTemplateUsed(response,'alert_config.html')

    def test_redirect_for_non_owners(self):
        """Ensure that non-owners cannot access the edit pages
        """
        self.c.logout()
        self.c.login(
            username = self.secondary.username,
            password = self.secondary_pass)


        for single_alert in self.alerts:
            pk = single_alert.pk
            response = self.c.get(
                '/alert/alert_config/'+str(pk)+'/',
                follow=True)
            self.assertNotEqual(len(response.redirect_chain),0)
            self.assertTrue(
                (reverse(
                    'alert_detail',
                    kwargs={'pk':pk}),
                302) in response.redirect_chain)


    def test_create(self):
        """ UNDER WORK FOR ALERT CREATION
            

        """
        response = self.c.get('/alert/alert_create/',follow=True)
        response = self.c.post(
            '/alert/alert_create/',
            data={'alert-name':'name'},
            follow=True)


    def test_render(self):
        #request = self.factory.get('/alert/alert_create')
        #request.user = self.primary
        #ac_view = views.alert_config()
        pass



