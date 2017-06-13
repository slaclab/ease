from django import forms
from .models import Alert, Pv


class configAlert(forms.Form):
    class Meta:
        model = Alert

    new_name = forms.CharField(
        label = 'New Alert name',
        max_length = Alert.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'name':'some_random_name',
                'type':'text',
            }
        )
    )