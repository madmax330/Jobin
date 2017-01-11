from django.conf.urls import url
from . import views

app_name = 'manual'

urlpatterns = [
    # Student side manuals
    url(r'^student/index', views.student_index, name='student_index'),
    url(r'^student/home$', views.student_home, name='student_home'),
    url(r'^student/posts', views.student_posts, name='student_posts'),
    url(r'^student/events', views.student_events, name='student_events'),
    url(r'^student/resume', views.student_resume, name='student_resume'),
    url(r'^student/profile', views.student_profile, name='student_profile'),

    # Company side manuals
    url(r'^company/index', views.company_index, name='company_index'),
    url(r'^company/home', views.company_home, name='company_home'),
    url(r'^company/posts', views.company_posts, name='company_posts'),
    url(r'^company/events', views.company_events, name='company_events'),
    url(r'^company/profile', views.company_profile, name='company_profile'),
]

