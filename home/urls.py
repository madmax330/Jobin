from django.conf.urls import url
from . import views


app_name = 'home'

urlpatterns = [

    url(r'^$', views.index_view, name='index'),
    url(r'^login/student/$', views.login_student, name='student_login'),
    url(r'^login/company/$', views.login_company, name='company_login'),
    url(r'^send/contact/message/$', views.send_contact_message, name='send_contact_message'),

    url(r'^register/student/$', views.register_student, name='register_student'),
    url(r'^register/company/$', views.register_company, name='register_company'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^activate/company/(?P<key>.+)/$', views.activate_company, name='activate_company'),
    url(r'^activate/student/(?P<key>.+)/$', views.activate_student, name='activate_student'),
    url(r'^new-activation/$', views.new_verification, name='new_activation'),
    url(r'^new/password/(?P<ut>\w+)/$', views.new_password_view, name='new_password'),

    url(r'^change/user/info/(?P<ut>\w+)/$', views.ChangeUserInfo.as_view(), name='change_info'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^privacy-policy/$', views.privacy_policy, name='policy'),
    url(r'^terms-and-conditions/$', views.terms_and_conditions, name='terms'),

    url(r'^create/content/(?P<n>[0-9]+)/$', views.create_test_content, name='gen_content'),
    url(r'^clear/content/$', views.clear_test_content, name='clear_content'),

]
