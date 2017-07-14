"""Django consults this page to determine the html that should be sent
 to the user
"""


from django.shortcuts import render

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect

from account_mgr_app.models import Profile
from .models import Alert, Pv, Trigger
from .forms import configAlert, configTrigger, deleteAlert, subscribeAlert, createPv

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.http import Http404

from django.core.urlresolvers import reverse
from django.urls import reverse_lazy


from django.forms.formsets import formset_factory
from django.db import transaction, IntegrityError



# login_url = reverse('login')
# login_url = '/acct/login/'



# Create your views here.
@login_required()
def list_all(request):
    """Currently unused - Draw a page with a full list of PVs and Alerts.

    Attributes
    __________
        request : django.http.HttpRequest

    Returns
    -------
        render : django.http.HttpResponse
    """
    context = {}
    context['pv_list'] = Pv.objects.all()
    context['alert_list'] = Alert.objects.all()
    context['user'] = request.user
    return render( request, 'debug_list_all.html', context)
    #return HttpResponse("<h1>Page is alive</h1>")

@login_required()
def title(request):
    """Blank filler page. First destination after logging in.

    Args
    ____
        request : django.http.HttpRequest

    Returns
    -------
        render : django.http.HttpResponse
    """
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
    """Currently unused - Draw a page with a full list of PVs and Alerts

    Args
    ____
        request : django.http.HttpRequest

    Returns
    -------
        render : django.http.HttpResponse
    """
    model = Alert
    template_name = 'alerts_all.html'
    paginate_by = 30

    def get_queryset(self):
        new_context = Alert.objects.all().order_by('name')
        return new_context

@method_decorator(login_required, name = 'dispatch')
class pvs_all(generic.ListView):
    """Draws page listing all PVs. Handles pagination.
    
    Attributes
    __________
        template_name : string
            Determines the .html in aler_config_app/templates to use.

        paginate_by : int
            number of PVs per page
    """
    model = Pv
    template_name = 'pvs_all.html'
    paginate_by = 30

    def get_queryset(self):
        """Organizes the Pvs Alphabetically
        """
        new_context = Pv.objects.all().order_by('name')
        return new_context

@method_decorator(login_required, name = 'dispatch')
class pv_detail(generic.DetailView):
    """Draws page showing information about PV
    
    Attributes
    __________
        template_name : string
            Determines the .html in aler_config_app/templates to use.

    """
    model = Pv
    context_object_name='pv'
    template_name = 'pv_detail.html'

@method_decorator(login_required, name = 'dispatch')
class pv_create(generic.edit.CreateView):
    """Draws page for PV creation
    
    Attributes
    __________
        template_name : string
            Determines the .html in aler_config_app/templates to use.

    """
    model = Pv
    # context_object_name='pv'
    template_name = 'pv_create.html'
    form_class = createPv
    # fields = []
    # form_class.fields = [createPv.new_name]
    # success_url = reverse('pvs_page_all')
    success_url = reverse_lazy('pvs_page_all')
    # fields = ['name']
    def form_valid(self,form):
        """Receives and processes the form
        """
        # form.cleaned_data.get('new_name')
        form.instance.name = form.cleaned_data.get('new_name')
        form.save()
        return super(pv_create, self).form_valid(form)


# @method_decorator(login_required, name = 'dispatch')
# class alert_detail(generic.DetailView):
#     model = Alert
#     context_object_name='alert'
#     template_name = 'alert_detail.html'

@login_required()
def alert_detail(request,pk,*args,**kwargs):
    """Draws read-only screen for individual alert

    Args
    ____
        pk : int
            DB index of the displayed alert. PK is sent automatically from the 
            regex in url. 

    Note
    ____
        It may be better to rewrite this function as a class so long as the 
        class can support the dynamic number of triggers.
    """
    try:
        alert_inst = get_object_or_404(Alert,pk=pk)
    except Http404:
        return HttpResponseRedirect(reverse('alerts_page_all'))



    if request.method == "POST":

        form = subscribeAlert(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('new_subscribe'):
                try:
                    alert_inst.subscriber.add(request.user.profile)
                except ValueError:
                    # instance already exists -- pass
                    pass
            else:
                try:
                    alert_inst.subscriber.remove(request.user.profile)
                except ValueError:
                    # instance already removed -- pass
                    pass


            return HttpResponseRedirect(reverse('alerts_page_all'))


    else:
        subscribed = False
        if request.user.profile in alert_inst.subscriber.all():
            subscribed = True
        form = subscribeAlert(
            initial = {
                'new_subscribe': subscribed
            }
        )

    context = {
        'alert': alert_inst,
        'form':form,
    }

    return render( 
        request, 
        'alert_detail.html', 
        context
    )


@login_required()
def alert_config(request,pk=None,*args,**kwargs):
    """Draws editable screen for individual alert.
    
    This page is accesssible only to the owner of the alert.

    Args
    ____
        pk : int, None
            DB index of the displayed alert. PK is sent automatically from the 
            regex in url. If pk is none, or does not match an existing alert,
            the user is redirected to to the alert creation url which links
            back to this function.

    Note
    ____
        It may be better to rewrite this function as a class so long as the 
        class can support the dynamic number of triggers. Having functions 
        specific to the creation and editing processes could produce much
        more readable and maintainable code. As it stands, this function is
        something of a mess.
    """
    for x in sorted(request.POST):
        print("{:>20}  {:>20}  {:>20}".format(x,str(request.POST[x]),str(type(request.POST[x]))))

    # dict sets the intial values in the form fields, is empty if alert is new
    alert_initial = {}


    # redirect for alert creation
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


    if not create:
        print(request.user.profile)
        print(alert_inst.owner.all())
        print(request.user.profile not in alert_inst.owner.all())
        if request.user.profile not in alert_inst.owner.all():
            return HttpResponseRedirect(reverse('alert_detail',kwargs={'pk':pk}))

    triggerFormSet = formset_factory(configTrigger)


    # handle POST request
    if request.method == 'POST':            
        form = configAlert(request.POST,)
        triggerForm = triggerFormSet(request.POST, prefix='tg')

        # if form.is_valid() and triggerForm.is_valid():
        if form.is_valid():
            if create:
                alert_inst = Alert()
                alert_inst.save()
            
            else:
                pass
            # alter name 
            alert_inst.name = form.cleaned_data['new_name']   
            # alter owners 
            owners_list = []
            for pk in form.cleaned_data['new_owners']:
                owners_list.append(Profile.objects.get(pk=pk))
            print(owners_list,"*******************************************************")
            alert_inst.owner = owners_list
            # alter user subscription relation note: LOGGED IN USER ONLY
            if form.cleaned_data['new_subscribe']:
                try:
                    alert_inst.subscriber.add(request.user.profile)
                except ValueError:
                    # instance already exists -- pass
                    pass
            else:
                try:
                    alert_inst.subscriber.remove(request.user.profile)
                except ValueError:
                    # instance already removed -- pass
                    pass

            alert_inst.save()

            # iterate through individual triggers, check each for validity
            new_triggers = []
            for single_trigger_form in triggerForm:
                # reexamine this section, is it still necessary?
                # do values occasionally return false? like new_subscribe
                if single_trigger_form.is_valid():

                    # if single_trigger_form.cleaned_data.get('new_pv') == None:
                    #     continue;
                    # if int(single_trigger_form.cleaned_data.get('new_pv')) == -1:
                    #     new_trigger_pv = None
                    # else:
                    #     new_trigger_pv = Pv.objects.get(pk=int(single_trigger_form.cleaned_data.get('new_pv')))

                    
                    # if single_trigger_form.cleaned_data.get('new_compare') == str(-1):
                    #     new_trigger_compare = None
                    # else:
                    #     new_trigger_compare = single_trigger_form.cleaned_data.get('new_compare')

                    new_triggers.append(
                        Trigger(
                            name = single_trigger_form.cleaned_data.get('new_name'),
                            alert = alert_inst,
                            pv = single_trigger_form.cleaned_data.get('new_pv'),
                            compare = single_trigger_form.cleaned_data.get('new_compare'),
                            value = single_trigger_form.cleaned_data.get('new_value'),
                        )
                    )
            
            # valid triggers in new_triggers[], now add them to db
            try:
                # atomic means no db change unless all changes are error free
                with transaction.atomic():
                    alert_inst.trigger_set.all().delete()
                    Trigger.objects.bulk_create(new_triggers)
                    pass

            except IntegrityError:
                print("UPDATE FAILURE")


        else:
            print("BAD FORM")
            # print(triggerForm.errors)
            # for single_trigger_form in triggerForm:
            #     # print(dir(single_trigger_form))
            #     print(single_trigger_form.is_valid())

        return HttpResponseRedirect(reverse('alerts_page_all'))
    

    # handle GET request
    else:
        if create:
            pass
        else:
            if request.user.profile in alert_inst.subscriber.all():
                subscribed = True
            else:
                subscribed = False
            alert_initial = {
                'new_name': alert_inst.name,
                'new_owners':[x.pk for x in alert_inst.owner.all()],
                'new_subscribe': subscribed,
                 
            }
            trigger_initial = [
                {   
                    'new_name': l.name,
                    'new_pv': l.pv.pk if l.pv else None,
                    'new_value':l.value,
                    'new_compare':l.compare,
                } 
                for l in alert_inst.trigger_set.all()
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
    """Draws deletion page for an alert.

    Args
    ____
        pk : int
            DB index of the displayed alert. PK is sent automatically from the 
            regex in url. 

    Note
    ____
        Having deletion occur on a post request is safer than a get request. 
        This page is designed solely to present the form required for receiving
        the post request.
    """
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
