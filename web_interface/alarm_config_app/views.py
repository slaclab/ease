from django.shortcuts import render

from django.views import generic
from django.http import HttpResponse
from .models import Alarm, Pv




# Create your views here.

def list_all(request):
    context = {}
    context['pv_list'] = Pv.objects.all()
    context['alarm_list'] = Alarm.objects.all()
    context['user'] = request.user
    return render( request, 'debug_list_all.html', context)
    #return HttpResponse("<h1>Page is alive</h1>")

def title(request):
    context = {}
    context['user'] = request.user
    return render( request, 'title.html', context)

def pvs(request):
    context = {}
    context['pv_list'] = Pv.objects.all()
    context['user'] = request.user
    return render( request, 'pvs.html', context)

def alerts(request):
    context = {}
    context['alert_list'] = Alarm.objects.all()
    context['user'] = request.user
    return render( request, 'alerts.html', context)
    
class alerts_all(generic.ListView):
    model = Alarm
    template_name = 'alerts_all.html'
    paginate_by = 10

class alert_detail(generic.DetailView):
    model = Alarm
    context_object_name='alert'
    template_name = 'alert_detail.html'


