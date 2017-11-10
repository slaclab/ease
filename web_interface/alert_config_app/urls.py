from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^debug/$', views.list_all, name='list_all'),
    
    url(r'^title/$', views.Title_page.as_view(), name='title_page'),
   
    url(r'^pvs_all/$', views.pvs_all.as_view(), name='pvs_page_all'),
    url(r'^pv_detail/(?P<pk>\d+)/$', views.pv_detail.as_view(), name='pv_detail'),
    url(r'^pv_create/$', views.pv_create.as_view(), name='pv_create'),
    url(r'^pv_detail/(?P<pk>\d+)/delete/$', views.pv_delete.as_view(), name = 'pv_delete'),
    
    url(r'^alerts_all/$', views.alerts_all.as_view(), name='alerts_page_all'),
    url(r'^alert_detail/(?P<pk>\d+)/$', views.alert_detail.as_view(), name='alert_detail'),
    url(r'^alert_config/(?P<pk>\d+)/$', views.alert_config.as_view(), name='alert_config'),
    url(r'^alert_create/$', views.alert_config.as_view(), name='alert_create'),
    url(r'^alert_delete/(?P<pk>\d+)/$', views.alert_delete,name='alert_delete'),

]
