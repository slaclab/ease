from django import forms
from .models import Alert, Pv, Trigger
from account_mgr_app.models import Profile


class configTrigger(forms.Form):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['new_pv'] = forms.ChoiceField(
            label = 'PV name',
            # use this to sort alphabetiaclly if necessary
            # sorted([(np.random.random(),np.random.random()) for x in range(10)],key=lambda s: s[1])
            choices = [(-1,None)] + [ (x.pk,x.name) for x in Pv.objects.all()],
            # choices = ["a,"b"],
            widget = forms.Select(
                attrs = {
                    'class':'custom-select',
                }
            )
        )
    
    
    
    new_name = forms.CharField(
        label = 'Trigger name',
        max_length = Trigger.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        )
    )
    '''
    new_pv = forms.ChoiceField(
        label = 'PV name',
        # use this to sort alphabetiaclly if necessary
        # sorted([(np.random.random(),np.random.random()) for x in range(10)],key=lambda s: s[1])
        choices = [(-1,None)] + [ (x.pk,x.name) for x in Pv.objects.all()],
        # choices = ["a,"b"],
        widget = forms.Select(
            attrs = {
                'class':'custom-select',
            }
        )
    )
    '''
    new_value = forms.FloatField(
        label = 'Value',
        required = False,
        widget = forms.NumberInput(
            attrs = {
                'class':'form-control',
            }
        )
    )

    new_compare = forms.ChoiceField(
        label = 'Comparison',
        choices = [(-1,None)] + Trigger.compare_choices,
        widget = forms.Select(
            attrs = {
                'class':'custom-select',
            }
        )
    )


    def clean_new_name(self):
        data = self.cleaned_data['new_name']
        # print("DATA:",data)
        # if len(data) <= 0 or data == None:
        #     raise forms.ValidationError(
        #         'Links must have unique anchors and URLs.',
        #         code='duplicate_links'
        #     )
        return data

    def clean_new_pv(self):
        data = self.cleaned_data['new_pv']
        if data == str(-1):
            data = None
        else:
            data = Pv.objects.get(pk=int(data))

        return data

    def clean_new_compare(self):
        data = self.cleaned_data['new_compare']
        if data == str(-1):
            data = None
        if data == "":
            data = None

        return data


class configAlert(forms.Form):
    class Meta:
        model = Alert

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['new_owners'] = forms.MultipleChoiceField(
            label = 'Owners',
            # use this to sort alphabetiaclly if necessary
            # sorted([(np.random.random(),np.random.random()) for x in range(10)],key=lambda s: s[1])
            choices = [ (x.pk,x.user.username) for x in Profile.objects.all()],
            # choices = ["a,"b"],
            widget = forms.CheckboxSelectMultiple(
                attrs = {
                    'class':'form-control',
                }
            )
        )




    new_name = forms.CharField(
        label = 'Alert name',
        max_length = Alert.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        )
    )

    '''
    new_owners = forms.MultipleChoiceField(
        label = 'Owners',
        # use this to sort alphabetiaclly if necessary
        # sorted([(np.random.random(),np.random.random()) for x in range(10)],key=lambda s: s[1])
        choices = [ (x.pk,x.user.username) for x in Profile.objects.all()],
        # choices = ["a,"b"],
        widget = forms.CheckboxSelectMultiple(
            attrs = {
                'class':'form-control',
            }
        )
    )
    '''

    new_subscribe = forms.BooleanField(
        label = "Subscribed",
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input',
                'type':'checkbox',
            }
        )
    )

    def clean_new_subscribe(self):
        
        if self.cleaned_data['new_subscribe']:
            data = True
        else:
            data = False

        return data


class subscribeAlert(forms.Form):
    class Meta:
        model = Alert

    new_subscribe = forms.BooleanField(
        label = "Subscribed",
        required = False,
        widget = forms.CheckboxInput(
            attrs = {
                'class':'form-check-input',
                'type':'checkbox',
            }
        )
    )
    def clean_new_subscribe(self):
        
        if self.cleaned_data['new_subscribe']:
            data = True
        else:
            data = False

        return data

class createPv(forms.ModelForm):
    class Meta:
        model = Pv
        fields = ['new_name']

    new_name = forms.CharField(
        label = 'PV name',
        max_length = Pv.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'type':'text',
            }
        )
    )
    # forms.ModelForm.Meta.fields.append(new_name)
    



class deleteAlert(forms.Form):
    class Meta:
        model = Alert
        fields = []
