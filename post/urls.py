from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^company/posts/$', views.CompanyPosts.as_view(), name='companyposts'),
    url(r'^new/$', views.NewPostView.as_view(), name='new'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.PostUpdateView.as_view(), name='update'),
    url(r'^close/(?P<pk>[0-9]+)/$', views.ClosePostView.as_view(), name='close'),
    url(r'^recover/(?P<pk>[0-9]+)/$', views.PostRecoveryView.as_view(), name='recover'),
    url(r'^recover/old/app/(?P<ak>[0-9]+)/$', views.activate_old_application, name='recover_old_app'),
    url(r'^remove/old/app/(?P<ak>[0-9]+)/$', views.close_old_application, name='remove_old_app'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.CompanyPost.as_view(), name='companypost'),
    url(r'^student/posts/(?P<pk>[0-9]+)/(?P<pt>\w+)/$', views.StudentPosts.as_view(), name='studentposts'),
    url(r'^apply/(?P<pk>[0-9]+)/(?P<pt>\w+)/$', views.ApplyView.as_view(), name='apply'),
    url(r'^applicants/(?P<pk>[0-9]+)/$', views.PostApplicantsView.as_view(), name='applicants'),
    url(r'^applicant/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.SingleApplicantView.as_view(), name='applicant'),
    url(r'^discard/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.DiscardApplicant.as_view(), name='discard'),
    url(r'^student/details/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.StudentDetailsView.as_view(), name='studentdetails'),
    url(r'^app/(?P<ak>[0-9]+)/pdf/$', views.ApplicantPDF.as_view(), name='app_pdf'),
]








