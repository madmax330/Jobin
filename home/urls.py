from django.conf.urls import url
from . import views


app_name = 'home'

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^register/(?P<ut>\w+)/$', views.RegisterView.as_view(), name='register'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^activate/(?P<key>.+)$', views.activate, name='activate'),
    url(r'^new-activation/$', views.new_verification, name='new_activation'),
    url(r'^not/open/$', views.school_closed, name='closed'),
    url(r'^new/password/$', views.NewPasswordView.as_view(), name='new_password'),

    url(r'^change/user/info/(?P<ut>\w+)/$', views.ChangeUserInfo.as_view(), name='change_info'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^close/notification/(?P<pk>[0-9]+)/$', views.close_notification, name='close_notification'),
    url(r'^close/all/notifications/(?P<u>\w+)/$', views.close_notifications, name='close_all_notifications'),

    url(r'^privacy-policy/$', views.privacy_policy, name='policy'),
    url(r'^terms-and-conditions/$', views.terms_and_conditions, name='terms'),

    url(r'^create/content/(?P<n>[0-9]+)/$', views.create_test_content, name='gen_content'),
    url(r'^clear/content/$', views.clear_test_content, name='clear_content'),

]
