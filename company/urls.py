from django.conf.urls import url
from . import views


app_name = 'company'

urlpatterns = [
    url(r'^home/$', views.index_view, name='index'),
    url(r'^new/$', views.NewCompanyView.as_view(), name='new'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^edit/$', views.EditCompanyView.as_view(), name='edit'),
]

