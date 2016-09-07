from django.conf.urls import url
from . import views


app_name = 'company'

urlpatterns = [
    url(r'^home/$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.NewCompanyView.as_view(), name='new'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.DetailsView.as_view(), name='details'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.UpdateCompanyView.as_view(), name='update'),
]

