from django.conf.urls import url
from . import views


app_name = 'company'

urlpatterns = [
    url(r'^home/$', views.index_view, name='index'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^suggestions/$', views.suggestions_view, name='suggestions'),

    url(r'^new/$', views.NewCompanyView.as_view(), name='new'),
    url(r'^edit/$', views.EditCompanyView.as_view(), name='edit'),
    url(r'^not/new/$', views.company_not_new, name='not_new'),

    url(r'^upload/logo/$', views.upload_logo, name='upload_logo'),
    url(r'^delete/logo/$', views.delete_logo, name='delete_logo'),

    url(r'^new/suggestion/$', views.new_suggestion, name='new_suggestion'),
    url(r'^comment/suggestion/(?P<pk>[0-9]+)/$', views.comment_suggestion, name='comment_suggestion'),
]

