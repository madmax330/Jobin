from django.conf.urls import url
from . import views


app_name = 'student'

urlpatterns = [
    url(r'^home/$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.NewStudentView.as_view(), name='new'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^history/$', views.HistoryView.as_view(), name='history'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.UpdateStudentView.as_view(), name='update'),
]

