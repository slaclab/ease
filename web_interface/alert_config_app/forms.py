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

    def clean_new_name(self):
        data = self.cleaned_data['new_name']
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