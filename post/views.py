from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post, Application
from home.models import Message, JobinSchool, JobinProgram, JobinMajor
from home.utils import new_message, new_notification
from .forms import NewPostForm
from company.models import Company
from student.models import Student
from resume.models import Resume, LanguageLink, SchoolLink, ExperienceLink, SkillLink, AwardLink
import datetime
from django.core.exceptions import ObjectDoesNotExist


class CompanyPosts(generic.ListView):
    template_name = 'post/company_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(company=Company.objects.filter(user=user).first(), status='open')
        for x in posts:
            if Application.objects.filter(post=x, cover_submitted=True, cover_opened=False, status='active').count() > 0:
                x.notified = True
            else:
                x.notified = False
            if Application.objects.filter(post=x, opened=False, status='active').count() > 0:
                x.new_apps = True
            else:
                x.new_apps = False
            x.save()
        return posts

    def get_context_data(self, **kwargs):
        context = super(CompanyPosts, self).get_context_data(**kwargs)
        msgs = Message.objects.filter(company=Company.objects.get(user=self.request.user))
        context['msgs'] = msgs
        for x in msgs:
            x.delete()
        return context


class NewPostView(CreateView):
    model = Post
    form_class = NewPostForm

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        post = form.save(commit=False)
        post.schools = 'ALL'
        post.company = company
        post.is_startup_post = company.is_startup
        msg = 'Your post was created successfully.'
        new_message('company', company, 'info', msg)
        return super(NewPostView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = NewPostForm

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        msg = 'Your post was successfully updated.'
        new_message('company', company, 'info', msg)
        return super(PostUpdateView, self).form_valid(form)


class ClosePostView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.status = 'closed'
        post.save()
        msg = 'Post ' + post.title + ' closed successfully'
        new_message('company', post.company, 'warning', msg)
        msg = 'Post ' + post.title + ' closed on ' + str(datetime.datetime.now()) + '.'
        new_notification('company', post.company, 0, msg)
        apps = Application.objects.filter(post=post, status='active')
        for x in apps:
            x.status = 'closed'
            x.save()
            msg = 'The position ' + post.title + ' has been closed.'
            new_notification('student', x.student, 100, msg)
        return redirect('post:companyposts')


class CompanyPost(View):
    template_name = 'post/company_post.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post, status='active')
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            l.append(xx)
        msgs = Message.objects.filter(company=post.company)
        context = {
            'post': post,
            'applicants': l,
            'msgs': msgs,
            'count': len(l)
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class StudentPosts(View):
    template_name = 'post/student_posts.html'

    def get(self, request, pk, pt):
        try:
            student = Student.objects.get(user=self.request.user)
            resumes = Resume.objects.filter(student=student)
            if pt == 'startup':
                p1 = Post.objects.filter(is_startup_post=True, status='open', programs='All Programs')
                p2 = Post.objects.filter(is_startup_post=True, status='open', programs=student.program)
            else:
                p1 = Post.objects.filter(type=pt, status='open', programs='All Programs')
                p2 = Post.objects.filter(type=pt, status='open', programs=student.program)
            posts = []
            for x in p2:
                posts.append(x)
            for x in p1:
                posts.append(x)
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
            rkey = 0
            for r in resumes:
                if r.is_active:
                    rkey = r.pk
            msgs = Message.objects.filter(student=student)
            vcount = Post.objects.filter(type='volunteer', status='open', programs=student.program).count() + \
                     Post.objects.filter(type='volunteer', status='open', programs='All Programs').count()
            icount = Post.objects.filter(type='internship', status='open', programs=student.program).count() + \
                     Post.objects.filter(type='internship', status='open', programs='All Programs').count()
            ptcount = Post.objects.filter(type='parttime', status='open', programs=student.program).count() + \
                     Post.objects.filter(type='parttime', status='open', programs='All Programs').count()
            ngcount = Post.objects.filter(type='newgrad', status='open', programs=student.program).count() + \
                     Post.objects.filter(type='newgrad', status='open', programs='All Programs').count()
            scount = Post.objects.filter(is_startup_post=True, status='open', programs=student.program).count() + \
                      Post.objects.filter(is_startup_post=True, status='open', programs='All Programs').count()
            vact = ''
            iact = ''
            pact = ''
            nact = ''
            sact = ''
            temp = pt
            if pt == 'volunteer':
                vact = 'active'
                pt = 'Volunteer'
            elif pt == 'internship':
                iact = 'active'
                pt = 'Internship'
            elif pt == 'parttime':
                pact = 'active'
                pt = 'Part-Time'
            elif pt == 'newgrad':
                nact = 'active'
                pt = 'New Grad'
            elif pt == 'startup':
                sact = 'active'
                pt = 'Start Up Company'
            context = {
                'list': l,
                'count': len(l),
                'resumes': resumes,
                'rkey': rkey,
                'msgs': msgs,
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
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')

    def post(self, request, pk, pt):
        r = request.POST.get('rk')
        student = Student.objects.get(user=self.request.user)
        resumes = Resume.objects.filter(student=student)
        for x in resumes:
            x.is_active = False
            if x.pk == r:
                x.is_active = True
            x.save()
        return self.get(request, pk=pk, pt=pt)


class StudentDetailsView(View):
    template_name = 'post/student_post_details.html'

    def get(self, request, pk, ak):
        post = Post.objects.get(pk=pk)
        app = Application.objects.get(pk=ak)
        msgs = Message.objects.filter(student=app.student)
        context = {
            'post': post,
            'comp': post.company,
            'app': app,
            'msgs': msgs,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk, ak):
        cover = request.POST.get('cover')
        post = Post.objects.get(pk=pk)
        app = Application.objects.get(pk=ak)
        if cover is not None:
            app.cover = cover
            app.cover_submitted = True
            app.save()
            msg = 'Cover letter successfully submitted for post: ' + app.post_title
            new_message('student', app.student, 'info', msg)
            msg = 'Cover letter submitted by applicant (' + app.student_name + ') for post ' + app.post_title
            new_notification('company', post.company, 100, msg)
            return redirect('student:index')
        msg = 'Cover letter cannot be left blank.'
        new_message('student', app.student, 'danger', msg)
        msgs = Message.objects.filter(student=app.student)
        context = {
            'post': post,
            'app': app,
            'msgs': msgs,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class ApplyView(View):

    def get(self, request, pk, pt):
        post = Post.objects.get(pk=pk)
        student = Student.objects.get(user=self.request.user)
        r = Resume.objects.filter(student=student).filter(is_active=True)
        test = Application.objects.filter(student=student, post=post)
        if test.count() > 0:
            msg = 'You have already applied for this post'
            new_message('student', student, 'warning', msg)
            return redirect('post:studentposts', pk=pk, pt=pt)
        if r.count() > 0:
            resume = r.first()
            app = Application()
            app.post_title = post.title
            app.student_name = student.firstname + ' ' + student.lastname
            app.post = post
            app.student = student
            app.resume = resume
            app.date = datetime.datetime.now()
            app.status = 'active'
            app.save()
            msg = 'You successfully applied for the post: ' + post.title
            new_message('student', student, 'info', msg)
            return redirect('post:studentposts', pk=pk, pt=pt)
        else:
            msg = 'You need to have at least one active resume to apply for posts. Activate one and try again.'
            new_message('student', student, 'warning', msg)
            return redirect('resume:index')


class PostApplicantsView(View):
    template_name = 'post/post_applicants.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post, status='active')
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            l.append(xx)
        msgs = Message.objects.filter(company=post.company)
        program = JobinProgram.objects.filter(name=post.programs)
        context = {
            'post': post,
            'list': l,
            'msgs': msgs,
            'schools': JobinSchool.objects.all(),
            'majors': JobinMajor.objects.filter(program=program),
            'count': len(l)
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        program = JobinProgram.objects.filter(name=post.programs)
        school_filter = request.POST.get('schools')
        major_filter = request.POST.get('majors')
        schools = []
        majors = []
        if school_filter and major_filter:
            schools = school_filter.split(',')
            majors = major_filter.split(',')
        elif school_filter:
            schools = school_filter.split(',')
        elif major_filter:
            majors = major_filter.split(',')
        msg = 'Current filters. Schools: '
        if school_filter:
            msg += school_filter
        else:
            msg+= 'None'
        if major_filter:
            msg += '; Majors: ' + major_filter
        else:
            msg += '; Majors: None'
        new_message('company', post.company, 'info', msg)
        keep = request.POST.get('keep')
        apps = Application.objects.filter(post=post, status='active')
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            if schools and majors:
                if xx.school in schools and xx.major in majors:
                    l.append(xx)
            elif schools:
                if xx.school in schools:
                    l.append(xx)
            elif majors:
                if xx.major in majors:
                    l.append(xx)
        if not keep:
            d = []
            for x in apps:
                xx = Applicant(x, x.student)
                if schools and majors:
                    if xx.school not in schools and xx.major not in majors:
                        d.append(x)
                elif majors:
                    if xx.major not in majors:
                        d.append(x)
                elif schools:
                    if xx.school not in schools:
                        d.append(x)
            for x in d:
                x.status = 'closed'
                x.save()
                msg = "Your application for the job " + x.post_title + " was discontinued."
                new_notification('student', x.student, 100, msg)
            msg = 'The applicants outside the filter (' + str(len(d)) + ') were removed successfully.'
            new_message('company', post.company, 'info', msg)
        msgs = Message.objects.filter(company=post.company)
        context = {
            'post': post,
            'list': l,
            'msgs': msgs,
            'schools': JobinSchool.objects.all(),
            'majors': JobinMajor.objects.filter(program=program),
            'count': len(l)
        }
        for m in msgs:
            m.delete()
        return render(request, self.template_name, context)


class SingleApplicantView(View):
    template_name = 'post/post_applicant.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post, status='active')
        if apps.count() > 0:
            xx = apps[0]
            if not xx.opened:
                xx.opened = True
                xx.save()
        else:
            msg = 'There are no more active applicants for this post'
            new_message('company', post.company, 'warning', msg)
            return redirect('post:applicants', pk=post.pk)
        app = Applicant(xx, xx.student)
        msgs = Message.objects.filter(company=post.company)
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
            'app': app,
            'page': 0,
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
            'msgs': msgs,
        }
        for m in msgs:
            m.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        keep = request.POST.get('keep')
        appid = request.POST.get('appid')
        page = int(request.POST.get('page'))
        cover = request.POST.get('cover')
        if not keep == 'True':
            x = Application.objects.get(pk=appid)
            x.status = 'closed'
            x.save()
            msg = 'The applicant was successfully removed.'
            new_message('company', post.company, 'info', msg)
            msg = 'Your application for the ' + x.post_title + ' opportunity was discontinued.'
            new_notification('student', x.student, 100, msg)
            apps = Application.objects.filter(post=post, status='active')
            if apps.count() > 0:
                if page >= apps.count():
                    page = 0
                xx = apps[page]
                if not xx.opened:
                    xx.opened = True
                    xx.save()
                app = Applicant(xx, xx.student)
                msgs = Message.objects.filter(company=post.company)
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
                    'app': app,
                    'page': page,
                    'resume': app.resume,
                    'lan': lan,
                    'exp': exp,
                    'aws': aws,
                    'schools': schs,
                    'skills': sks,
                    'msgs': msgs,
                    'acount': len(aws),
                    'ecount': len(exp),
                    'scount': len(schs),
                    'kcount': len(sks),
                    'lcount': len(lan),
                }
                for m in msgs:
                    m.delete()
                return render(request, self.template_name, context)
            else:
                return redirect('post:applicants', pk=pk)
        else:
            if cover == 'True':
                a = Application.objects.get(pk=appid)
                if not a.cover_requested:
                    msg = 'Cover letter requested successfully!'
                    new_message('company', post.company, 'info', msg)
                    msg = post.company.name + ' requests a cover letter for your application to the ' \
                        + post.title + ' position. Go to the application details to submit your cover letter'
                    new_notification('student', a.student, 100, msg)
                    a.cover_requested = True
                    a.save()
                else:
                    msg = 'A cover letter was already sent to the applicant; you will be' \
                                ' notified when a cover letter is received'
                    new_message('company', post.company, 'warning', msg)
            apps = Application.objects.filter(post=post, status='active')
            if page >= apps.count():
                page = 0
            elif page < 0:
                page = apps.count() - 1
            xx = apps[page]
            if not xx.opened:
                xx.opened = True
                xx.save()
            app = Applicant(xx, xx.student)
            msgs = Message.objects.filter(company=post.company)
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
                'app': app,
                'page': page,
                'resume': app.resume,
                'lan': lan,
                'exp': exp,
                'aws': aws,
                'schools': schs,
                'skills': sks,
                'msgs': msgs,
                'acount': len(aws),
                'ecount': len(exp),
                'scount': len(schs),
                'kcount': len(sks),
                'lcount': len(lan),
            }
            for m in msgs:
                m.delete()
            return render(request, self.template_name, context)


class ApplicantDetailsView(View):
    template_name = 'post/applicant_details.html'

    def get(self, request, pk):
        a = Application.objects.get(pk=pk)
        if not a.opened:
            a.opened = True
            a.save()
        if a.cover_submitted:
            a.cover_opened = True
            a.save()
        app = Applicant(a, a.student)
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
        post = a.post
        post.notified = False
        post.save()
        return render(request, self.template_name, context)


class DiscardApplicant(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        x.status = 'closed'
        x.save()
        msg = 'Applicant successfully removed.'
        new_message('company', x.post.company, 'info', msg)
        msg = 'Your application for the ' + x.post.title + ' opportunity was discontinued.'
        new_notification('student', x.student, 100, msg)
        return redirect('post:applicants', pk=pk)


class RequestCover(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        post = x.post
        if not x.cover_requested:
            x.cover_requested = True
            x.save()
            msg = 'Cover letter successfully requested.'
            new_message('company', post.company, 'info', msg)
            msg = post.company.name + ' requests a cover letter for your application to the ' \
                        + post.title + ' position. Go to the application details to submit your cover letter'
            new_notification('student', x.student, 100, msg)
        else:
            msg = 'A cover letter was already sent to the applicant; you will be notified when a cover letter ' \
                        'is received.'
            new_message('company', post.company, 'warning', msg)
        return redirect('post:applicants', pk=pk)


class CustomPost:

    def __init__(self, post, company, student):
        self.pk = post.pk
        self.name = company.name
        self.address = company.address + ', ' + company.city + ', ' + company.state + ', ' + company.zipcode
        self.website = company.website
        self.logo = company.logo
        self.title = post.title
        self.start_date = post.start_date
        self.end_date = post.end_date
        self.deadline = post.deadline
        self.wage = post.wage
        self.openings = post.openings
        self.requirements = post.requirements
        self.description = post.description
        if Application.objects.filter(post=post, student=student).count() > 0:
            self.applied = True
        else:
            self.applied = False


class Applicant:

    def __init__(self, app, stu):
        self.pk = app.pk
        self.fname = stu.firstname
        self.lname = stu.lastname
        self.email = stu.email
        self.phone = stu.phone
        self.address = stu.address + ' ' + stu.city + ' ' + stu.state + ' ' + stu.zipcode
        self.school = stu.school
        self.program = stu.program
        self.major = stu.major
        self.resume = app.resume
        self.post = app.post
        self.cover = app.cover
        self.cover_requested = app.cover_requested
        self.cover_submitted = app.cover_submitted
        self.cover_opened = app.cover_opened
        self.date_applied = app.date
        self.app_opened = app.opened
