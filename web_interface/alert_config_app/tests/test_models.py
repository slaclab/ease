from django.test import TestCase

from account_mgr_app.models import *
from alert_config_app.models import *
from django.contrib.auth.models import User

# Create your tests here.
class AlertFieldsTests(TestCase):
    '''Ensure that Alert Fields exist 
    '''
    @classmethod
    def setUpTestData(cls):
        # print("setUpTestData: Run once to set up non-modified data for all class methods.")
        # super().setUpClass()
        u = User.objects.create_user("unittest_user",password="pass")
        # u.save()
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
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('name').verbose_name
        self.assertEquals(field_label,'name')

    def test_field_subscriber(self):
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('subscriber').verbose_name
        self.assertEquals(field_label,'subscriber')

    def test_field_owner(self):
        alert = Alert.objects.get(name="unittest_alert")
        field_label = alert._meta.get_field('owner').verbose_name
        self.assertEquals(field_label,'owner')

    # def test_false_is_false(self):
    #     # print("Method: test_false_is_false.")
    #     self.assertFalse(False)

    # def test_false_is_true(self):
    #     # print("Method: test_false_is_true.")
    #     self.assertTrue(False)

    # def test_one_plus_one_equals_two(self):
    #     # print("Method: test_one_plus_one_equals_two.")
    #     self.assertEqual(1 + 1, 2)

    def tearDown(self):
        #Clean up run after every test method.
        pass
    
    @classmethod
    def tearDownClass(cls):
        # super().tearDownClass()
        pass