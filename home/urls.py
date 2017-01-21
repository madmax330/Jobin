from django.conf.urls import url
from . import views


app_name = 'home'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^section/(?P<section>\w+)/$', views.section_view, name='section'),
    url(r'^register/(?P<utype>\w+)/$', views.RegisterView.as_view(), name='register'),
    url(r'^verify/$', views.VerifyView.as_view(), name='verify'),
    url(r'^password_forgotten/$', views.Reset_password, name='Reset_password'),
    url(r'^change_password/$',  views.Change_password.as_view(), name='Change_password'),
    url(r'^closed/$', views.NotOpenView.as_view(), name='closed'),
    url(r'^updateinfo/(?P<utype>\w+)/$', views.ChangeUserInfo.as_view(), name='updateinfo'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^closenote/(?P<u>\w+)/(?P<nk>[0-9]+)/(?P<page>\w+)/(?P<pk>[0-9]+)/(?P<pt>\w+)/$',
        views.CloseNotification.as_view(), name='closenote'),
    url(r'^closenote/all/(?P<u>\w+)/(?P<page>\w+)/(?P<pk>[0-9]+)/(?P<pt>\w+)/$',
        views.CloseAllNotifications.as_view(), name='closeallnotes'),
    url(r'^invalid_user/(?P<Infos>[\w\.\-_ ]+)', views.UnvalidUser.as_view(), name='invalid_user'),
    url(r'^register/student/confirm_email/(?P<token>[\w\.\-_ ]+)', views.confirm_email, name='confirm_email'),
    url(r'^register/company/confirm_email/(?P<token>[\w\.\-_ ]+)', views.confirm_email, name='confirm_email'),
    url(r'^privacy-policy/$', views.privacy_policy, name='policy'),
    url(r'^terms-and-conditions/$', views.terms_and_conditions, name='terms'),
]