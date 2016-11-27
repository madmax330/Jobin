from .models import Post, Application
from resume.models import LanguageLink, AwardLink, ExperienceLink, SchoolLink, SkillLink
import datetime

def get_applicant_context(app):
    ll = LanguageLink.objects.filter(resume=app.resume)
    al = AwardLink.objects.filter(resume=app.resume)
    el = ExperienceLink.objects.filter(resume=app.resume)
    sl = SchoolLink.objects.filter(resume=app.resume)
    kl = SkillLink.objects.filter(resume=app.resume)
    lan = []
    for x in ll:
        lan.append(x.language)
    exp = []
    for x in el:
        exp.append(x.experience)
    aws = []
    for x in al:
        aws.append(x.award)
    schs = []
    for x in sl:
        schs.append(x.school)
    sks = []
    for x in kl:
        sks.append(x.skill)
    context = {
        'post': app.post,
        'app': app,
        'resume': app.resume,
        'lan': lan,
        'exp': exp,
        'aws': aws,
        'schools': schs,
        'skills': sks,
        'acount': len(aws),
        'ecount': len(exp),
        'scount': len(schs),
        'kcount': len(sks),
        'lcount': len(lan),
    }
    return context


def get_student_posts_context(post_type, student, posts, resumes, rkey):
    pt = post_type
    today = datetime.datetime.now().date()
    vcount = Post.objects.filter(type='volunteer', status='open', programs=student.program, deadline__gte=today).count() + \
             Post.objects.filter(type='volunteer', status='open', programs='All Programs', deadline__gte=today).count()
    icount = Post.objects.filter(type='internship', status='open', programs=student.program, deadline__gte=today).count() + \
             Post.objects.filter(type='internship', status='open', programs='All Programs', deadline__gte=today).count()
    ptcount = Post.objects.filter(type='parttime', status='open', programs=student.program, deadline__gte=today).count() + \
              Post.objects.filter(type='parttime', status='open', programs='All Programs', deadline__gte=today).count()
    ngcount = Post.objects.filter(type='newgrad', status='open', programs=student.program, deadline__gte=today).count() + \
              Post.objects.filter(type='newgrad', status='open', programs='All Programs', deadline__gte=today).count()
    scount = Post.objects.filter(is_startup_post=True, status='open', programs=student.program, deadline__gte=today).count() + \
             Post.objects.filter(is_startup_post=True, status='open', programs='All Programs', deadline__gte=today).count()
    vact = ''
    iact = ''
    pact = ''
    nact = ''
    sact = ''
    temp = pt
    if pt == 'volunteer':
        vact = 'pnb-active'
        pt = 'Volunteer'
    elif pt == 'internship':
        iact = 'pnb-active'
        pt = 'Internship'
    elif pt == 'parttime':
        pact = 'pnb-active'
        pt = 'Part-Time'
    elif pt == 'newgrad':
        nact = 'pnb-active'
        pt = 'New Grad'
    elif pt == 'startup':
        sact = 'pnb-active'
        pt = 'Start Up Company'
    context = {
        'list': posts,
        'count': len(posts),
        'resumes': resumes,
        'rkey': rkey,
        'nav_student': student,
        'ptype': pt,
        'pt': temp,
        'vcount': vcount,
        'icount': icount,
        'ptcount': ptcount,
        'ngcount': ngcount,
        'scount': scount,
        'vact': vact,
        'iact': iact,
        'pact': pact,
        'nact': nact,
        'sact': sact,
    }
    return context



