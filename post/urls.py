from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^company/posts/$', views.CompanyPosts.as_view(), name='companyposts'),
    url(r'^new/$', views.NewPostView.as_view(), name='new'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.PostUpdateView.as_view(), name='update'),
    url(r'^close/(?P<pk>[0-9]+)/$', views.ClosePostView.as_view(), name='close'),
    url(r'^recover/(?P<pk>[0-9]+)/$', views.PostRecoveryView.as_view(), name='recover'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.CompanyPost.as_view(), name='companypost'),
    url(r'^student/posts/(?P<pk>[0-9]+)/(?P<pt>\w+)/$', views.StudentPosts.as_view(), name='studentposts'),
    url(r'^apply/(?P<pk>[0-9]+)/(?P<pt>\w+)/$', views.ApplyView.as_view(), name='apply'),
    url(r'^applicants/(?P<pk>[0-9]+)/$', views.PostApplicantsView.as_view(), name='applicants'),
    url(r'^applicant/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.SingleApplicantView.as_view(), name='applicant'),
    url(r'^discard/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.DiscardApplicant.as_view(), name='discard'),
    url(r'^cover/request/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.RequestCover.as_view(), name='coverrequest'),
    url(r'^student/details/(?P<pk>[0-9]+)/(?P<ak>[0-9]+)/$', views.StudentDetailsView.as_view(), name='studentdetails'),
]








