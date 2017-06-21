from django.conf.urls import url
from . import views


app_name = 'resume'


urlpatterns = [
    # List views
    url(r'^$', views.resume_index, name='index'),

    # New views
    url(r'^new/resume/$', views.new_resume, name='new'),
    url(r'^new/language/(?P<pk>[0-9]+)/$', views.new_language, name='new_language'),
    url(r'^new/experience/(?P<pk>[0-9]+)/$', views.new_experience, name='new_experience'),
    url(r'^new/award/(?P<pk>[0-9]+)/$', views.new_award, name='new_award'),
    url(r'^new/school/(?P<pk>[0-9]+)/$', views.new_school, name='new_school'),
    url(r'^new/skill/(?P<pk>[0-9]+)/$', views.new_skill, name='new_skill'),
    url(r'^new/reference/(?P<pk>[0-9]+)/$', views.new_reference, name='new_reference'),

    # Update views
    url(r'^edit/resume/(?P<pk>[0-9]+)/$', views.edit_resume, name='edit'),
    url(r'^edit/language/(?P<pk>[0-9]+)/$', views.edit_language, name='edit_language'),
    url(r'^edit/experience/(?P<pk>[0-9]+)/$', views.edit_experience, name='edit_experience'),
    url(r'^edit/award/(?P<pk>[0-9]+)/$', views.edit_award, name='edit_award'),
    url(r'^edit/school/(?P<pk>[0-9]+)/$', views.edit_school, name='edit_school'),
    url(r'^edit/skill/(?P<pk>[0-9]+)/$', views.edit_skill, name='edit_skill'),
    url(r'^edit/reference/(?P<pk>[0-9]+)/$', views.edit_reference, name='edit_reference'),

    # Delete views
    url(r'^delete/resume/(?P<pk>[0-9]+)/$', views.delete_resume, name='delete'),
    url(r'^delete/language/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_language, name='delete_language'),
    url(r'^delete/experience/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_experience, name='delete_experience'),
    url(r'^delete/award/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_award, name='delete_award'),
    url(r'^delete/school/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_school, name='delete_school'),
    url(r'^delete/skill/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_skill, name='delete_skill'),
    url(r'^delete/reference/(?P<rk>[0-9]+)/(?P<pk>[0-9]+)/$', views.delete_reference, name='delete_reference'),

    # Links
    url(r'^add/school/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_school, name='add_school'),
    url(r'^add/skill/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_skill, name='add_skill'),
    url(r'^add/language/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_language, name='add_language'),
    url(r'^add/experience/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_experience, name='add_experience'),
    url(r'^add/award/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_award, name='add_award'),
    url(r'^add/reference/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.add_reference, name='add_reference'),

    # Misc
    url(r'^change/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.change_application_resume, name='change'),
    url(r'^activate/(?P<pk>[0-9]+)/$', views.change_active_resume, name='activate'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.resume_detail, name='details'),
    url(r'^copy/resume/(?P<pk>[0-9]+)/$', views.copy_resume, name='copy'),
]

