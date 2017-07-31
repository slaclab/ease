from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^reset-password/$', auth_views.password_reset, name='reset_password'),
    url(r'^reset-password/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset-password/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^profile/$', views.profile, name='user_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change_password/$', views.change_password, name='change_password'),
        
]