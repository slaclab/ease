from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import EditProfileForm

from django.contrib.auth import login, authenticate

from .forms import SignUpForm


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.


def signup(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form =SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {'user':user, 'domain':current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})
            mail_subject = 'Activate your Ease account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect('account_activation_sent')                
            
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('title_page')
    else:
        # form = UserCreationForm()
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    
    
    
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        return redirect('activation_complete')
    else:
        return redirect('activation_failed')
        
        
def account_activation_sent(request):
    args = {'user': request.user}
    return render(request, 'account_activation_sent.html', args) 

   

def activation_complete(request):
    args = {'user': request.user}
    return render(request, 'activation_complete.html', args) 
    
    
    
def activation_failed(request):
    args = {'user': request.user}
    return render(request, 'activation_failed.html', args) 
    

def profile(request):
    args = {'user': request.user}
    return render(request, 'profile.html', args)
    
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('/acct/profile')
            
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)
    
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/acct/profile')
        else:
            return redirect('/acct/profile/change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'change_password.html', args)
