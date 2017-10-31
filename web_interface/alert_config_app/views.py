"""Django consults this page to determine the html that should be sent
 to the user
"""


from django.shortcuts import render, redirect

from django.views import generic,View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)

from account_mgr_app.models import Profile
import account_mgr_app
from .models import Alert, Pv, Trigger #PVname #Does this allow you to say "model = Pv....model = Alert..."
from .forms import configAlert, configTrigger, deleteAlert, subscribeAlert, createPv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404
from django.http import Http404

from django.core.urlresolvers import reverse
from django.urls import reverse_lazy


from django.forms.formsets import formset_factory
from django.db import transaction, IntegrityError, models
from django.contrib import messages



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


#@login_required()
#def title(request):
#    context = {}
#    context['user'] = request.user
#    return render( request, 'title.html', context)
#------------------------------------------------------------------------------
@method_decorator(login_required, name = 'dispatch')
class Title_page(generic.ListView):
    #model = Alert
    template_name = 'title.html'
    form_class = configAlert
#    context_object_name='alert'
    paginate_by = 30
    
    def title(request):
       context = {}
       context['user'] = request.user
       return render( request, 'title.html', context)
   
    def get_queryset(self):
        new_context = Alert.objects.all().order_by('name')
        return new_context
        #return render(request, self.template_name, {'new_context': new_context })
    
    
#    def form_valid(self,form):
#        # form.cleaned_data.get('new_name')
#        form.instance.name = form.data['new_subscribe']
#
#        return super().form_valid(form)
#------------------------------------------------------------------------------



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
        query = self.request.GET.get("q")#
        if query:
            new_context = new_context.filter(name__icontains=query)#
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
        query = self.request.GET.get("q")
        if query:
            new_context = new_context.filter(name__icontains=query) 
        return new_context

@method_decorator(login_required, name = 'dispatch')
class pv_detail(generic.DetailView, UpdateView):
    model = Pv
    context_object_name='pv'
    template_name = 'pv_detail.html'
    form_class = createPv
    success_url = reverse_lazy('pvs_page_all')
    def form_valid(self,form):
        # form.cleaned_data.get('new_name')
        form.instance.name = form.cleaned_data.get('new_name')
        form.save()
        return super().form_valid(form)


@method_decorator(login_required, name = 'dispatch')
class pv_delete(DeleteView):
    model = Pv
    template_name = 'pv_delete.html'
    success_url = reverse_lazy('pvs_page_all')



@method_decorator(login_required, name = 'dispatch')
class pv_create(generic.edit.CreateView):
    """Draws page for PV creation
    
    Attributes
    __________
        template_name : string
            Determines the .html in aler_config_app/templates to use.

    """
    model = Pv
    template_name = 'pv_create.html'
    form_class = createPv
    success_url = reverse_lazy('pvs_page_all')
    def form_valid(self,form):
        """
        Receives and processes the form
        
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





@method_decorator(login_required, name = 'dispatch')
class alert_config(View):
    def get(self, request, *args, **kwargs):
        """Draw the page when create or config is loaded by the user
        """
        self.pk = kwargs.get("pk",None)
        if self.pk == None:
            create = True
        else:
            create = False
            # attempt to fetch database entry for alert, redirect on fail 
            try:
                alert_inst = get_object_or_404(Alert,pk=self.pk)
            except Http404:
                return HttpResponseRedirect(reverse('alert_create'))

        if not create:
            # reject non-owner users
            if request.user.profile not in alert_inst.owner.all():
                return HttpResponseRedirect(reverse(
                        'alert_detail',
                        kwargs={'pk':self.pk}))

        if create:
            alert_inst = None
            alert_initial = {}
            trigger_initial = []
        else:
            if request.user.profile in alert_inst.subscriber.all():
                subscribed = True
            else:
                subscribed = False
            # prepare initial values for form fields showing current values
            alert_initial = {
                'new_name': alert_inst.name,
                'new_owners':[x.pk for x in alert_inst.owner.all()],
                'new_subscribe': subscribed,
                'new_lockout_duration':alert_inst.lockout_duration,    
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

        triggerFormSet = formset_factory(configTrigger)
        
        form = configAlert(initial = alert_initial)
        triggerForm = triggerFormSet(
            initial = trigger_initial,
            prefix='tg'
        )

        return render(
            request = request, 
            template_name = "alert_config.html", 
            context = {
                'form':form,
                'triggerForm':triggerForm,
                'alert':alert_inst,
                'create':create,
            },
        )

    def post(self, request, *args, **kwargs):
        # DEBUG ONLY --------------------------------------
        if 0:
            print("")
            for x in sorted(request.POST):
                print("{:>20}  {:>20}  {:>20}".format(  
                    x,
                    str(dict(request.POST)[x]),
                    str(type(dict(request.POST)[x]))))
            print("")
        
            form = configAlert(request.POST,)
            #triggerForm = triggerFormSet(request.POST, prefix='tg')

            if form.is_valid():
                print(form.cleaned_data)
        # DEBUG ONLY --------------------------------------
        
       
        self.pk = kwargs.get("pk",None)
        triggerFormSet = formset_factory(configTrigger)
        if self.pk == None:
            create = True
        else:
            create = False
        
        form = configAlert(request.POST,)
        triggerForm = triggerFormSet(request.POST, prefix='tg')
        # if there is no preexisting Alert - create a new one
        if create:
            alert_inst = Alert()
            alert_inst.save()

        else:
            # attempt to get indicated alert instance, redirect on fail
            try:
                alert_inst = get_object_or_404(Alert,pk=self.pk)
            except Http404:
                return HttpResponseRedirect(reverse('alert_create'))
         
        if form.is_valid():
            
            # Set/Modify the alert's name 
            alert_inst.name = form.cleaned_data['new_name']

            # Set/Modify the alert's list of owners
            alert_inst.owner.clear()
            for new_owner in form.cleaned_data['new_owners']:
                alert_inst.owner.add(new_owner)

            # Set/Modify the alert's lockout duration
            alert_inst.lockout_duration = form.cleaned_data[
                'new_lockout_duration']

            # Set/Modify the alert's subscription relation with the user
            if ((form.cleaned_data['new_subscribe'])
                and (request.user.profile not in alert_inst.subscriber.all())):
                    alert_inst.subscriber.add(request.user.profile)
            elif ((not form.cleaned_data['new_subscribe'])
                and (request.user.profile in alert_inst.subscriber.all())):
                    alert_inst.subscriber.remove(request.user.profile)
        
            alert_inst.save()

            new_triggers = []
            for single_trigger_form in triggerForm:
                # reexamine this section, is it still necessary?
                # do values occasionally return false? like new_subscribe
                if single_trigger_form.is_valid():

                    new_triggers.append(
                        Trigger(
                            name = single_trigger_form.cleaned_data.get(
                                'new_name'),
                            alert = alert_inst,
                            pv = single_trigger_form.cleaned_data.get(
                                'new_pv'),
                            compare = single_trigger_form.cleaned_data.get(
                                'new_compare'),
                            value = single_trigger_form.cleaned_data.get(
                                'new_value'),
                        )
                    )
            
            try:
                # atomic prevents db change unless all changes are error free
                with transaction.atomic():
                    alert_inst.trigger_set.all().delete()
                    Trigger.objects.bulk_create(new_triggers)
                    pass

            except IntegrityError:
                pass
                #print("UPDATE FAILURE")
        else:
            #print(form.errors.as_data()['new_owners']) 
            return render(
                request = request, 
                template_name = "alert_config.html", 
                context = {
                    'form':form,
                    'triggerForm':triggerForm,
                    'alert':alert_inst,
                    'create':create,
                },
            )
            #return HttpResponseRedirect(reverse(
            #        'alert_config',
            #        kwargs={'pk':self.pk}
            #))

        return HttpResponseRedirect(reverse('alerts_page_all'))
       


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


#def profile(request):
#    args = {'user': request.user}
#    return render(request, 'profile.html', args)
#    
#def edit_profile(request):
#    if request.method == 'POST':
#        form = EditProfileForm(request.POST, instance=request.user)
#        
#        if form.is_valid():
#            form.save()
#            return redirect('/alert/profile')
#            
#    else:
#        form = EditProfileForm(instance=request.user)
#        args = {'form': form}
#        return render(request, 'edit_profile.html', args)
#    
#    
#def change_password(request):
#    if request.method == 'POST':
#        form = PasswordChangeForm(data=request.POST, user=request.user)
#        
#        if form.is_valid():
#            form.save()
#            update_session_auth_hash(request, form.user)
#            return redirect('/alert/profile')
#        else:
#            return redirect('/alert/profile/change_password')
#    else:
#        form = PasswordChangeForm(user=request.user)
#        args = {'form': form}
#        return render(request, 'change_password.html', args)
#        
