from django.conf.urls import url
from . import views

app_name = 'event'

urlpatterns = [
    url(r'^company/events/$', views.CompanyEvents.as_view(), name='companyevents'),
    url(r'^new/$', views.NewEventView.as_view(), name='new'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.EventUpdateView.as_view(), name='update'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.CompanyEvent.as_view(), name='companyevent'),
    url(r'^student/events/(?P<pk>[0-9]+)/$', views.StudentEvents.as_view(), name='studentevents'),
    url(r'^interested/(?P<pk>[0-9]+)/$', views.NewInterest.as_view(), name='interest'),

    url(r'^new/get_states/(?P<country_name>[a-zA-Z_ ]+)/$', views.get_states, name='get_states'),
    url(r'^update/(?P<pk>[0-9]+)/get_states/(?P<country_name>[a-zA-Z_ ]+)/$', views.get_states_update, name='get_states_update'),
]

