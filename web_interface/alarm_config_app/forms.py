from django import forms
from .models import Alarm, Pv


class configAlert(forms.Form):
    class Meta:
        model = Alarm

    new_name = forms.CharField(
        label = 'New Alert name',
        max_length = Alarm.name_max_length,
        widget = forms.TextInput( 
            attrs = {
                'class':'form-control',
                'name':'some_random_name',
                'type':'text',
            }
        )
    )