from django.conf.urls import url

from . import views
from django.contrib.auth.views import password_reset, password_reset_done


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^debug/$', views.list_all, name='list_all'),
    url(r'^title/$', views.title, name='title_page'),
    # url(r'^pvs/$', views.pvs, name='pvs_page'),
    # url(r'^alerts/$', views.alerts, name='alerts_page'),
   
    url(r'^pvs_all/$', views.pvs_all.as_view(), name='pvs_page_all'),
  
    url(r'^alerts_all/$', views.alerts_all.as_view(), name='alerts_page_all'),
   
    url(r'^pv_detail/(?P<pk>\d+)/$', views.pv_detail.as_view(), name='pv_detail'),
    url(r'^pv_create/$', views.pv_create.as_view(), name='pv_create'),
    
    url(r'^pv_detail/(?P<pk>\d+)/edit/$', views.pv_config.as_view(), name = 'pv_config'),
    url(r'^pv_detail/(?P<pk>\d+)/delete/$', views.pv_delete.as_view(), name = 'pv_delete'),

    # url(r'^alert_detail/(?P<pk>\d+)/$', views.alert_detail.as_view(), name='alert_detail'),
    url(r'^alert_detail/(?P<pk>\d+)/$', views.alert_detail, name='alert_detail'),

    url(r'^alert_config/(?P<pk>\d+)/$', views.alert_config, name='alert_config'),
    url(r'^alert_create/$', views.alert_config, name='alert_create'),
    url(r'^alert_delete/(?P<pk>\d+)/$', views.alert_delete,name='alert_delete'),

    url(r'^profile/$', views.profile, name='user_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/change_password/$', views.change_password, name='change_password'),
    # url(r'^reset-password/$', password_reset, name='reset_password'),
    # url(r'^reset-password/done/$', password_reset_done, name='password_reset_done')
    
]
