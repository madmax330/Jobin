from django.conf.urls import url
from . import views


app_name = 'student'

urlpatterns = [
    url(r'^home/$', views.index_view, name='index'),
    url(r'^new/$', views.NewStudentView.as_view(), name='new'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^history/$', views.history_view, name='history'),
    url(r'^edit/$', views.EditStudentView.as_view(), name='edit'),
    url(r'^not/new/$', views.student_not_new, name='not_new'),
    url(r'^add/transcript/$', views.add_transcript, name='add_transcript'),
    url(r'^delete/transcript/(?P<pk>[0-9]+)/$', views.delete_transcript, name='delete_transcript'),
]

