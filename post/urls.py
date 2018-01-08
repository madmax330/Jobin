from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^company/posts/$', views.company_index, name='company_posts'),
    url(r'^student/posts/(?P<cat>[a-zA-Z_]+)/(?P<pk>[0-9]+)/$', views.student_index, name='student_posts'),
    url(r'^increment/(?P<pk>[0-9]+)/$', views.increment_count, name='increment'),

    url(r'^new/$', views.NewPostView.as_view(), name='new'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.EditPostView.as_view(), name='edit'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.post_detail, name='company_post'),
    url(r'^student/details/(?P<pk>[0-9]+)/$', views.student_detail, name='student_details'),
    url(r'^close/(?P<pk>[0-9]+)/$', views.close_post, name='close'),
    url(r'^recover/(?P<pk>[0-9]+)/$', views.RecoverPostView.as_view(), name='recover'),

    url(r'^apply/(?P<pk>[0-9]+)/$', views.apply, name='apply'),
    url(r'^submit/cover/(?P<pk>[0-9]+)/$', views.submit_cover_letter, name='submit_cover'),
    url(r'^recover/old/app/(?P<pk>[0-9]+)/$', views.activate_application, name='activate'),
    url(r'^withdraw/app/(?P<pk>[0-9]+)/$', views.withdraw_application, name='withdraw'),

    url(r'^applicants/(?P<pk>[0-9]+)/$', views.post_applicants, name='applicants'),
    url(r'^applicant/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.single_applicant, name='applicant'),
    url(r'^request/cover/(?P<pk>[0-9]+)/$', views.request_cover_letter, name='request_cover'),
    url(r'^discard/(?P<pk>[0-9]+)/$', views.discard_application, name='discard'),
    url(r'^save/(?P<pk>[0-9]+)/$', views.save_application, name='save'),
    url(r'^remove/save/(?P<pk>[0-9]+)/$', views.remove_application_save, name='remove_save'),
    url(r'^app/(?P<ak>[0-9]+)/pdf/$', views.ApplicantPDF.as_view(), name='app_pdf'),
    url(r'^student/app/(?P<ak>[0-9]+)/pdf/$', views.StudentApplicantPDF.as_view(), name='student_app_pdf'),
]








