from django import forms
from .models import Alert, Pv, Trigger



class configTrigger(forms.Form):
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


    def clean_new_name(self):
        data = self.cleaned_data['new_name']
        print("cleaning name")
        # print("DATA:",data)
        # if len(data) <= 0 or data == None:
        #     raise forms.ValidationError(
        #         'Links must have unique anchors and URLs.',
        #         code='duplicate_links'
        #     )
        return data

    def clean_new_pv(self):
        print("cleaning PV")
        data = self.cleaned_data['new_pv']
        if data == -1:
            data = None

        return data


class configAlert(forms.Form):
    class Meta:
        model = Alert

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

class deleteAlert(forms.Form):
    class Meta:
        model = Alert
        fields = []