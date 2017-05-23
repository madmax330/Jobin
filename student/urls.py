from django.conf.urls import url
from . import views


app_name = 'student'

urlpatterns = [
    url(r'^home/$', views.index_view, name='index'),
    url(r'^new/$', views.NewStudentView.as_view(), name='new'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^history/$', views.history_view, name='history'),
    url(r'^edit/$', views.EditStudentView.as_view(), name='edit'),
]

