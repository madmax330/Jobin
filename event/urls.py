from django.conf.urls import url
from . import views

app_name = 'event'

urlpatterns = [
    url(r'^company/events/$', views.CompanyEvents.as_view(), name='companyevents'),
    url(r'^new$', views.NewEventView.as_view(), name='new'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.EventUpdateView.as_view(), name='update'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.CompanyEvent.as_view(), name='companyevent'),
    url(r'^student/events/$', views.StudentEvents.as_view(), name='studentevents'),
]

