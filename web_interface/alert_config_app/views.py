from django.shortcuts import render

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Alert, Pv
from .forms import configAlert

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.http import Http404

from django.core.urlresolvers import reverse



login_url = "/login/"


# Create your views here.

def list_all(request):
    context = {}
    context['pv_list'] = Pv.objects.all()
    context['alert_list'] = Alert.objects.all()
    context['user'] = request.user
    return render( request, 'debug_list_all.html', context)
    #return HttpResponse("<h1>Page is alive</h1>")

def title(request):
    context = {}
    context['user'] = request.user
    return render( request, 'title.html', context)

# def pvs(request):
#     context = {}
#     context['pv_list'] = Pv.objects.all()
#     context['user'] = request.user
#     return render( request, 'pvs.html', context)

# def alerts(request):
#     context = {}
#     context['alert_list'] = Alert.objects.all()
#     context['user'] = request.user
#     return render( request, 'alerts.html', context)
    
@method_decorator(login_required, name = 'dispatch')
class alerts_all(generic.ListView):
    model = Alert
    template_name = 'alerts_all.html'
    paginate_by = 30

    def get_queryset(self):
        new_context = Alert.objects.all().order_by('name')
        return new_context

@method_decorator(login_required, name = 'dispatch')
class pvs_all(generic.ListView):
    model = Pv
    template_name = 'pvs_all.html'
    paginate_by = 30

    def get_queryset(self):
        new_context = Pv.objects.all().order_by('name')
        return new_context

@method_decorator(login_required, name = 'dispatch')
class pv_detail(generic.DetailView):
    model = Pv
    context_object_name='pv'
    template_name = 'pv_detail.html'

@method_decorator(login_required, name = 'dispatch')
class alert_detail(generic.DetailView):
    model = Alert
    context_object_name='alert'
    template_name = 'alert_detail.html'

@login_required()
def alert_config(request,pk=None,*args,**kwargs):
    # if pk == None:
    if pk != None:
        try:
            alert_inst = get_object_or_404(Alert,pk=pk)
        
        except Http404:
            return HttpResponseRedirect(reverse('alert_create'))

    if request.path != reverse('alert_create'):
        create = True
    else:
        create = False

    initial = {}
    form = configAlert(initial = initial)
    

    return render(request, "alert_config.html", {'form':form})


