from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth.models import User
from account_mgr_app.models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        #fields = ('username', 'email', 'password1', 'password2', )
        
        
        
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ['password', ]
    def __init__(self, *args, **kwargs):
        #copy any functionality you want form UserChangeForm
        super().__init__(*args, **kwargs)
        #self.fields['password'].help_text = self.fields['password'].help_text.format('../password/')
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
    
    def clean_password(self):
        #copy functionality provided by UserChangeForm 
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


        
        
class EditProfileForm(UserForm):
    
    class Meta:
        model = User 
        #exclude = {'password',}
        fields = ('first_name', 'last_name', 'email')






