from django.test import TestCase, LiveServerTestCase
from unittest import skip, skipIf, skipUnless
import unittest
import os
from selenium import webdriver
#from selenium.webdriver.firefox.webdriver import WebDriver
# Create your tests here.
# @skip("Keeping this as an example template")

webdriver_path = os.path.join(os.getcwd(),"geckodriver")

@skipUnless(
    os.path.isfile(webdriver_path),
    "Webdriver executable required for UI testing")
class SeleniumViewTests(LiveServerTestCase):
    '''I'm keeping this around as a template for other tests
    '''
    @classmethod
    def setUpTestData(cls):
        #cls.driver = WebDriver()
        print("setting up test data")
        pass

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        cls.wdriver = webdriver.Firefox(executable_path=webdriver_path)
        # how long to poll for a DOM object before giving up. 
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
