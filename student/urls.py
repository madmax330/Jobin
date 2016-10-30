from django.conf.urls import url
from . import views


app_name = 'student'

urlpatterns = [
    url(r'^home/$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.NewStudentView.as_view(), name='new'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^activity/$', views.ActivityView.as_view(), name='activity'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.UpdateStudentView.as_view(), name='update'),
    url(r'^new/get_states/(?P<country_name>[a-zA-Z_ ]+)/$', views.get_states, name='get_states'),
    url(r'^update/(?P<pk>[0-9]+)/get_states/(?P<country_name>[a-zA-Z_ ]+)/$', views.get_states_update, name='get_states_update'),

    url(r'^new/get_majors/(?P<program_id>[a-zA-Z_& ]+)/$', views.get_majors, name='get_majors'),
    url(r'^update/(?P<pk>[0-9]+)/get_majors/(?P<program_id>[a-zA-Z_& ]+)/$', views.get_majors_update, name='get_majors_update'),


]

