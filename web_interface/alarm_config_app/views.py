from django.shortcuts import render


#----
from django.http import HttpResponse
from .models import Alarm, Pv




# Create your views here.

def list_all(request):
    context={}
    context['pv_list'] = Pv.objects.all()
    context['alarm_list'] = Alarm.objects.all()
    return render(request,'list_all.html', context)
    
    #return HttpResponse("<h1>Page is alive</h1>")
    
