from django.test import TestCase
from unittest import expectedFailure

from account_mgr_app.models import *
from alert_config_app.models import *
from django.contrib.auth.models import User
#from sqlite3 import IntegrityError
from django.db.utils import IntegrityError
# Create your tests here.
class AlertFieldsTests(TestCase):
    """Ensure that Alert Fields exist 
    """
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user( "unittest_user", password="pass")
        profile = u.profile
        a = Alert.objects.create(
            name="unittest_alert",
        )
        a.subscriber.add(profile)
        a.owner.add(profile)

    def setUp(self):
        # print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_field_name(self):
        """Ensure name field exists
        """
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_field_subscriber(self):
        """Ensure subscriber field exists
        """
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('subscriber').verbose_name
        self.assertEquals(field_label,'subscriber')

    def test_field_owner(self):
        """Ensure owner field exists
        """
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('owner').verbose_name
        self.assertEquals(field_label,'owner')
    
    def test_multi_user(self):
        """Ensure that usernames are unique

        Move to acct_mgr?
        """
        with self.assertRaises(IntegrityError):
            u = User.objects.create_user( "unittest_user", password="pass")

    def tearDown(self):
        #Clean up run after every test method.
        pass
    
    @classmethod
    def tearDownClass(cls):
        # super().tearDownClass()
        pass

class PVFieldsTests(TestCase):
    """Ensure that Alert Fields exist 
    """
    @classmethod
    def setUpTestData(cls):
        p = Pv.objects.create(
            name="unittest_pv",
        )

    def setUp(self):
        # print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_field_name(self):
        """Ensure name field exists
        """
        pv = Pv.objects.get(name="unittest_pv")
        field_label = pv._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    @expectedFailure
    def test_multi_user(self):
        """Ensure that PVs are unique
        """
        with self.assertRaises(IntegrityError):
            p = Pv.objects.create(
                name="unittest_pv",
            )

    def tearDown(self):
        #Clean up run after every test method.
        pass
    
    @classmethod
    def tearDownClass(cls):
        # super().tearDownClass()
        pass
