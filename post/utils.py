from .models import Post, Application
from .classes import Applicant, CustomPost
from resume.models import LanguageLink, AwardLink, ExperienceLink, SchoolLink, SkillLink
from home.utils import MessageCenter
from django.db.models import Q
import datetime


class PostUtil:

    @staticmethod
    def do_post_notifications(posts):
        temp = []
        for x in posts:
            rem_date = (datetime.datetime.now() + datetime.timedelta(days=4)).date()
            if x.deadline < rem_date:
                MessageCenter.incoming_deadline(x.company, x.title)
            if Application.objects.filter(post=x, cover_submitted=True, cover_opened=False,
                                          status='active').count() > 0:
                x.notified = True
            else:
                x.notified = False
            if Application.objects.filter(post=x, opened=False, status='active').count() > 0:
                temp.append(x.title)
                x.new_apps = True
            else:
                x.new_apps = False
            x.save()
        return temp

    @staticmethod
    def get_student_posts(student, cat, pk):
        today = datetime.datetime.now().date()
        if cat == 'startup':
            posts = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program),
                                     is_startup_post=True, status='open', deadline__gte=today).order_by('deadline')
        else:
            posts = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program),
                                     type=cat, status='open', deadline__gte=today).order_by('deadline')
        l = []
        templ = []
        flag = False
        for x in posts:
            if int(x.pk) == int(pk) > 0:
                flag = True
            xx = x.company
            xxx = CustomPost(x, xx, student)
            if flag:
                l.append(xxx)
            else:
                templ.append(xxx)
        l.extend(templ)
        return l


class ApplicantUtil:

    @staticmethod
    def get_applicant(pk):
        a = Application.objects.get(pk=pk)
        return Applicant(a, a.student)

    @staticmethod
    def get_post_applicants(post):
        a1 = Application.objects.filter(Q(status='active') | Q(status='hold'), post=post)
        apps = []
        for x in a1:
            apps.append(Applicant(x, x.student))
        return apps

    @staticmethod
    def prep_app_filters(request, post):
        filters = {}
        school_filter = request.POST.get('schools')
        major_filter = request.POST.get('majors')
        gpa_filter = request.POST.get('gpa_filter')
        gpa = 0
        if gpa_filter:
            gpa = float(gpa_filter)
        schools = []
        majors = []
        if school_filter:
            schools = school_filter.split(',')
        if major_filter:
            majors = major_filter.split(',')
        MessageCenter.make_filter_message(school_filter, major_filter, gpa_filter, post)
        keep = request.POST.get('keep')
        filters['majors'] = majors
        filters['schools'] = schools
        filters['gpa'] = gpa
        filters['keep'] = keep
        return filters

    @staticmethod
    def apply_filters(filters, apps, post):
        gpa = filters['gpa']
        schools = filters['schools']
        majors = filters['majors']
        keep = filters['keep']
        l = {'apps': apps, 'ids': []}
        if gpa > 0:
            l = ApplicantUtil.__apply_gpa_filter(gpa, l['apps'])
        if schools:
            l = ApplicantUtil.__apply_school_filter(schools, l['apps'])
        if majors:
            l = ApplicantUtil.__apply_major_filter(majors, l['apps'])
        if not keep:
            d = [x for x in apps if int(x) not in l['ids']]
            for x in d:
                x.status = 'closed'
                x.save()
                msg = "Your application for the job " + x.post_title + " was discontinued."
                MessageCenter.new_notification('student', x.student, 100, msg)
            msg = 'The applicants outside the filter (' + str(len(d)) + ') were removed successfully.'
            MessageCenter.new_message('company', post.company, 'info', msg)
        return l['apps']

    @staticmethod
    def __apply_school_filter(schools, apps):
        l = {'apps': [], 'ids': []}
        for x in apps:
            if x.school in schools:
                l['apps'].append(x)
                l['ids'].append(int(x.pk))
        return l

    @staticmethod
    def __apply_major_filter(majors, apps):
        l = {'apps': [], 'ids': []}
        for x in apps:
            if x.major in majors:
                l['apps'].append(x)
                l['ids'].append(int(x.pk))
        return l

    @staticmethod
    def __apply_gpa_filter(gpa, apps):
        l = {'apps': [], 'ids': []}
        for x in apps:
            if float(x.gpa) >= gpa:
                l['apps'].append(x)
                l['ids'].append(int(x.pk))
        return l


class ApplicationUtil:

    @staticmethod
    def new_application(post, student, resume):
        app = Application()
        app.post_title = post.title
        app.student_name = student.firstname + ' ' + student.lastname
        app.post = post
        app.student = student
        app.resume = resume
        app.date = datetime.datetime.now()
        app.status = 'active'
        app.save()

    @staticmethod
    def get_application(pk):
        return Application.objects.get(pk=pk)

    @staticmethod
    def get_post_applications(post):
        a1 = Application.objects.filter(Q(status='active') | Q(status='hold'), post=post)
        apps = list(a1)
        return apps

    @staticmethod
    def get_held_applications(post):
        return Application.objects.filter(post=post, status='hold')

    @staticmethod
    def already_applied(student, post):
        return Application.objects.filter(student=student, post=post).count() > 0

    @staticmethod
    def update_opened_application(pk):
        app = ApplicationUtil.get_application(pk)
        changed = False
        if not app.app_opened:
            app.app_opened = True
            changed = True
        if app.cover_submitted and (not app.cover_opened):
            app.cover_opened = True
            changed = True
        if app.resume_notified:
            app.resume_notified = False
            changed = True
        if changed:
            app.save()


class PostContexts:

    @staticmethod
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
        context = {'post': app.post, 'app': app, 'resume': app.resume, 'lan': lan, 'exp': exp, 'aws': aws,
                   'schools': schs, 'skills': sks, 'acount': len(aws), 'ecount': len(exp), 'scount': len(schs),
                   'kcount': len(sks), 'lcount': len(lan),
        }
        return context

    @staticmethod
    def get_student_posts_context(post_type, student, posts, resumes, rkey):
        pt = post_type
        today = datetime.datetime.now().date()
        vcount = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program), type='volunteer',
                                     status='open', deadline__gte=today).count()
        icount = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program), type='internship',
                                     status='open', deadline__gte=today).count()
        ptcount = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program), type='parttime',
                                     status='open', deadline__gte=today).count()
        ngcount = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program), type='newgrad',
                                     status='open', deadline__gte=today).count()
        scount = Post.objects.filter(Q(programs='All Programs') | Q(programs=student.program), is_startup_post=True,
                                     status='open', deadline__gte=today).count()
        vact = iact = pact = nact = sact = ''
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
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {'list': posts, 'count': len(posts), 'resumes': resumes, 'rkey': rkey, 'nav_student': student,
                   'ptype': pt, 'pt': temp, 'vcount': vcount, 'icount': icount, 'ptcount': ptcount, 'ngcount': ngcount,
                   'scount': scount, 'vact': vact, 'iact': iact, 'pact': pact, 'nact': nact, 'sact': sact,
        }
        return context



