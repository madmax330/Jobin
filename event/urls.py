from django.conf.urls import url
from . import views

app_name = 'event'

urlpatterns = [

    url(r'^company/events/$', views.company_index, name='company_events'),
    url(r'^new/$', views.NewEventView.as_view(), name='new'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditEventView.as_view(), name='edit'),
    url(r'^close/(?P<pk>[0-9]+)/$', views.close_event, name='close'),
    url(r'^recover/(?P<pk>[0-9]+)/$', views.RecoverEventView.as_view(), name='recover'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.detail_view, name='details'),
    url(r'^student/events/(?P<pk>[0-9]+)/$', views.student_index, name='student_events'),
    url(r'^save/(?P<pk>[0-9]+)/$', views.save_event, name='save'),
    url(r'^remove/save/(?P<pk>[0-9]+)/$', views.remove_saved_event, name='remove_save'),

]

