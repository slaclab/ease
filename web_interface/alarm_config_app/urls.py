from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^debug/$', views.list_all, name='list_all'),
    url(r'^title/$', views.title, name='title_page'),
    url(r'^pvs/$', views.pvs, name='pvs_page'),
    url(r'^alerts/$', views.alerts, name='alerts_page'),
    url(r'^pvs_all/$', views.pvs, name='pvs_page_all'),
    url(r'^alerts_all/$', views.alerts_all.as_view(), name='alerts_page_all'),
    url(r'^alert_detail/(?P<pk>\d+)/$', views.alert_detail.as_view(), name='alert_detail'),

]
