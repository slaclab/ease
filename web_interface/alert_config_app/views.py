from django.shortcuts import render

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Alert, Pv, Trigger
from .forms import configAlert, configTrigger, deleteAlert

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.http import Http404

from django.core.urlresolvers import reverse

from django.forms.formsets import formset_factory
from django.db import transaction, IntegrityError



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
    for x in sorted(request.POST):
        print(x,"\t",request.POST[x])

    alert_initial = {}
    trigger_initial = []
    if pk != None:
        try:
            alert_inst = get_object_or_404(Alert,pk=pk)
        
        except Http404:
            return HttpResponseRedirect(reverse('alert_create'))


    if request.path == reverse('alert_create'):
        create = True
    else:
        create = False

    triggerFormSet = formset_factory(configTrigger)

    if request.method == 'POST':            
        form = configAlert(request.POST,)
        triggerForm = triggerFormSet(request.POST, prefix='tg')

        # if form.is_valid() and triggerForm.is_valid():
        if form.is_valid():
            if create:
                alert_inst = Alert()
            
            else:
                pass

            alert_inst.name = form.cleaned_data['new_name']
            alert_inst.save()

            new_triggers = []
            for single_trigger_form in triggerForm:
                # if single_trigger_form.cleaned_data.get('new_name') != None:
                print(single_trigger_form.data)
                if single_trigger_form.is_valid():
                    print(single_trigger_form.cleaned_data.get('new_pv'))
                    if int(single_trigger_form.cleaned_data.get('new_pv')) == -1:
                        new_trigger_pv = None
                    else:
                        new_trigger_pv = Pv.objects.get(pk=int(single_trigger_form.cleaned_data.get('new_pv')))
                    new_triggers.append(
                        Trigger(
                            name = single_trigger_form.cleaned_data.get('new_name'),
                            alert = alert_inst,
                            pv = new_trigger_pv,
                        )
                    )
            
            # print(new_triggers)
            try:
                with transaction.atomic():
                    alert_inst.trigger_set.all().delete()
                    Trigger.objects.bulk_create(new_triggers)
                    pass

            except IntegrityError:
                print("UPDATE FAILURE")


        else:
            print("BAD FORM")
            print(triggerForm.errors)
            for single_trigger_form in triggerForm:
                # print(dir(single_trigger_form))
                print(single_trigger_form.is_valid())

        return HttpResponseRedirect(reverse('alerts_page_all'))
        
    else:
        if create:
            pass

        else:
            alert_initial = {
                'new_name': alert_inst.name,
            }
            trigger_initial = [
                {'new_name': l.name,'new_pv': l.pv.pk if l.pv else None} for l in alert_inst.trigger_set.all()
            ]

        form = configAlert(initial = alert_initial)
        triggerForm = triggerFormSet(
            initial = trigger_initial,
            prefix='tg'
        )

    if create:
        alert_inst = None
    return render(
        request, 
        "alert_config.html", 
        {
            'form':form,
            'triggerForm':triggerForm,
            'alert':alert_inst,
            'create':create,
        },
    )


@login_required()
def alert_delete(request,pk=None,*args,**kwargs):
    for x in sorted(request.POST):
        print(x,"\t",request.POST[x])
    try:
        alert_inst = get_object_or_404(Alert,pk=pk)
    
    except Http404:
        return HttpResponseRedirect(reverse('alerts_page_all'))

    if request.method == "POST":
        deleteForm = deleteAlert(request.POST, )
        print("post detected")

        if deleteForm.is_valid():
            print("deleting")
            Alert.objects.filter(pk=pk).delete()
            return HttpResponseRedirect(reverse('alerts_page_all'))

        else:
            print("BAD FORM")

    else:
        deleteForm = deleteAlert()
    

    return render(
        request,
        "alert_delete.html",
        {'form':deleteForm,'alert':alert_inst},
    )