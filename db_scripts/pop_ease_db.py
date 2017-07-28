import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),os.pardir,os.pardir,"web_interface")))

import random

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'web_interface.settings'
django.setup()

from alert_config_app.models import *

def populate():
	a = "test_alert_"
	p = "test_pv_"
	t = "test_trigger_"
	compare_op = ['==', '>=', '<=', '!=']

	for i in range(1,6):
		al = a + str(i)
		test_alert = Alert(name=al)
		test_alert.save()

		pr = p + str(i)
		test_pv = Pv(name=pr)
		test_pv.save()

		tr = t + str(i)
	
		if (random.randint(100,1000)%2 == 0):
			test_trigger = Trigger(name=tr, alert=test_alert, pv=test_pv, value=random.randint(1,100), compare=random.choice(compare_op))
			test_trigger.save()
		else:
			test_trigger = Trigger(name=tr, alert=test_alert, pv=test_pv)
			test_trigger.save()



def depopulate():
	Alert.objects.all().delete()
	Pv.objects.all().delete()
	Trigger.objects.all().delete()

def main():
	print("Program can populate database with test data or delete data. ")
	

	while True:
		answer = input("Enter (p) to populate or (d) to depopulate: ")

		if answer == 'p':
			populate()
			break
		elif answer == 'd':
			depopulate()
			break
		else:
			print("invalid input. Try again.")	

if __name__ == "__main__":
	main()		
