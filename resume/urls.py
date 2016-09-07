from django.conf.urls import url
from . import views


app_name = 'resume'


urlpatterns = [
    # List views
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^list/language/(?P<rk>[0-9]+)/$', views.LanguageList.as_view(), name='languagelist'),
    url(r'^list/experience/(?P<rk>[0-9]+)/$', views.ExperienceList.as_view(), name='experiencelist'),
    url(r'^list/award/(?P<rk>[0-9]+)/$', views.AwardList.as_view(), name='awardlist'),
    url(r'^list/school/(?P<rk>[0-9]+)/$', views.SchoolList.as_view(), name='schoollist'),
    url(r'^list/skill/(?P<rk>[0-9]+)/$', views.SkillList.as_view(), name='skilllist'),

    # New views
    url(r'^new/resume/$', views.NewResumeView.as_view(), name='newresume'),
    url(r'^new/language/(?P<rk>[0-9]+)/$', views.NewLanguageView.as_view(), name='newlanguage'),
    url(r'^new/experience/(?P<rk>[0-9]+)/$', views.NewExperienceView.as_view(), name='newexperience'),
    url(r'^new/award/(?P<rk>[0-9]+)/$', views.NewAwardView.as_view(), name='newaward'),
    url(r'^new/school/(?P<rk>[0-9]+)/$', views.NewSchoolView.as_view(), name='newschool'),
    url(r'^new/skill/(?P<rk>[0-9]+)/$', views.NewSkillView.as_view(), name='newskill'),

    # Update views
    url(r'^update/resume/(?P<pk>[0-9]+)/$', views.ResumeUpdateView.as_view(), name='updateresume'),
    url(r'^update/language/(?P<pk>[0-9]+)/$', views.LanguageUpdateView.as_view(), name='updatelanguage'),
    url(r'^update/experience/(?P<pk>[0-9]+)/$', views.ExperienceUpdateView.as_view(), name='updateexperience'),
    url(r'^update/award/(?P<pk>[0-9]+)/$', views.AwardUpdateView.as_view(), name='updateaward'),
    url(r'^update/school/(?P<pk>[0-9]+)/$', views.SchoolUpdateView.as_view(), name='updateschool'),
    url(r'^update/skill/(?P<pk>[0-9]+)/$', views.SkillUpdateView.as_view(), name='updateskill'),

    # Delete views
    url(r'^delete/resume/(?P<pk>[0-9]+)/$', views.DeleteResume.as_view(), name='deleteresume'),
    url(r'^delete/language/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.DeleteLanguage.as_view(), name='deletelanguage'),
    url(r'^delete/experience/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.DeleteExperience.as_view(), name='deleteexperience'),
    url(r'^delete/award/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.DeleteAward.as_view(), name='deleteaward'),
    url(r'^delete/school/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.DeleteSchool.as_view(), name='deleteschool'),
    url(r'^delete/skill/(?P<pk>[0-9]+)/(?P<rk>[0-9]+)/$', views.DeleteSkill.as_view(), name='deleteskill'),

    url(r'^activate/(?P<pk>[0-9]+)/$', views.MakeActive.as_view(), name='makeactive'),
    url(r'^details/(?P<pk>[0-9]+)/$', views.ResumeDetailView.as_view(), name='details'),
]

