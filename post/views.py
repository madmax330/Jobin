from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post, Application
from home.models import Message, Notification, JobinSchool, JobinProgram, JobinMajor
from .forms import NewPostForm
from company.models import Company
from student.models import Student
from resume.models import Resume, Language, Experience, Award, School, Skill
import datetime
from django.core.exceptions import ObjectDoesNotExist


class CompanyPosts(generic.ListView):
    template_name = 'post/company_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(company=Company.objects.filter(user=self.request.user).first())

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
        post = form.save(commit=False)
        post.schools = 'ALL'
        post.programs = 'ALL'
        post.company = Company.objects.filter(user=self.request.user).first()
        x = Message()
        x.code = 'info'
        x.message = 'Your post was created successfully.'
        x.company = Company.objects.get(user=self.request.user)
        x.save()
        return super(NewPostView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = NewPostForm

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        x = Message()
        x.code = 'info'
        x.message = 'Your post was successfully updated.'
        x.company = company
        x.save()
        return super(PostUpdateView, self).form_valid(form)


class CompanyPost(View):
    template_name = 'post/company_post.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post).filter(status='active')
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

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            resumes = Resume.objects.filter(student=student)
            posts = Post.objects.all()
            l = []
            for x in posts:
                xx = x.company
                xxx = CustomPost(x, xx)
                l.append(xxx)
            rkey = 0
            for r in resumes:
                if r.is_active:
                    rkey = r.pk
            msgs = Message.objects.filter(student=student)
            context = {
                'list': l,
                'count': len(l),
                'resumes': resumes,
                'rkey': rkey,
                'msgs': msgs,
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')

    def post(self, request):
        r = request.POST.get('rk')
        student = Student.objects.get(user=self.request.user)
        resumes = Resume.objects.filter(student=student)
        for x in resumes:
            x.is_active = False
            if x.pk == r:
                x.is_active = True
            x.save()
        return self.get(request)


class StudentDetailsView(View):
    template_name = 'post/student_post_details.html'

    def get(self, request, pk, ak):
        post = Post.objects.get(pk=pk)
        app = Application.objects.get(pk=ak)
        msgs = Message.objects.filter(student=app.student)
        context = {
            'post': post,
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
            post.notified = True
            post.save()
            x = Message()
            x.student = app.student
            x.message = 'Cover letter successfully submitted for post: ' + app.post_title
            x.code = 'info'
            x.save()
            xx = Notification()
            xx.code = 100
            xx.message = 'Cover letter submitted by applicant (' + app.student_name + ') for post ' + app.post_title
            xx.company = post.company
            xx.save()
            return redirect('student:index')
        xx = Message()
        xx.student = app.student
        xx.message = 'Cover letter cannot be left blank.'
        xx.code = 'danger'
        xx.save()
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

    def get(self, request, pk, rk):
        post = Post.objects.get(pk=pk)
        resume = Resume.objects.get(pk=rk)
        student = Student.objects.get(user=self.request.user)
        if resume is not None:
            app = Application()
            app.post_title = post.title
            app.student_name = student.firstname + ' ' + student.lastname
            app.post = post
            app.student = student
            app.resume = resume
            app.date = datetime.datetime.now()
            app.status = 'active'
            app.save()
            x = Message()
            x.code = 'info'
            x.message = 'You successfully applied for the post: ' + post.title
            x.student = student
            x.save()
            return redirect('post:studentposts')
        else:
            return redirect('post:studentposts')


class PostApplicantsView(View):
    template_name = 'post/post_applicants.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post).filter(status='active')
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
        x = Message()
        x.company = post.company
        x.message = 'Current filters. Schools: '
        if school_filter:
            x.message += school_filter
        else:
            x.message += 'None'
        if major_filter:
            x.message += ' ' + major_filter
        else:
            x.message += ' Majors: None'
        x.save()
        keep = request.POST.get('keep')
        apps = Application.objects.filter(post=post).filter(status='active')
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            if schools and majors:
                if xx.school in schools and xx.program in majors:
                    l.append(xx)
            elif schools:
                if xx.school in schools:
                    l.append(xx)
            elif majors:
                if xx.program in majors:
                    l.append(xx)
        if not keep:
            d = []
            for x in apps:
                xx = Applicant(x, x.student)
                if schools and majors:
                    if xx.school not in schools and xx.program not in majors:
                        d.append(x)
                elif majors:
                    if xx.program not in majors:
                        d.append(x)
                elif schools:
                    if xx.school not in schools:
                        d.append(x)
            for x in d:
                x.status = 'closed'
                x.save()
            xx = Message()
            xx.code = 'info'
            xx.message = 'The applicants outside the filter (' + str(len(d)) + ') were removed successfully.'
            xx.company = post.company
            xx.save()
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
        apps = Application.objects.filter(post=post).filter(status='active')
        if apps.count() > 0:
            xx = Application.objects.filter(post=post).filter(status='active')[0]
        else:
            x = Message()
            x.company = post.company
            x.message = 'There are no more active applicants for this post'
            x.code = 'warning'
            x.save()
            return redirect('post:applicants', pk=post.pk)
        app = Applicant(xx, xx.student)
        msgs = Message.objects.filter(company=post.company)
        context = {
            'app': app,
            'page': 0,
            'resume': app.resume,
            'lan': Language.objects.filter(resume=app.resume),
            'exp': Experience.objects.filter(resume=app.resume),
            'aws': Award.objects.filter(resume=app.resume),
            'schools': School.objects.filter(resume=app.resume),
            'skills': Skill.objects.filter(resume=app.resume),
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
            xx = Message()
            xx.code = 'info'
            xx.message = 'The applicant was successfully removed.'
            xx.company = post.company
            xx.save()
            n = Notification()
            n.student = x.student
            n.message = 'Your application for the ' + x.post.title + ' opportunity was discontinued.'
            n.save()
            apps = Application.objects.filter(post=post).filter(status='active')
            if apps.count() > 0:
                if page >= apps.count():
                    page = 0
                xx = apps[page]
                app = Applicant(xx, xx.student)
                msgs = Message.objects.filter(company=post.company)
                context = {
                    'app': app,
                    'page': page,
                    'resume': app.resume,
                    'lan': Language.objects.filter(resume=app.resume),
                    'exp': Experience.objects.filter(resume=app.resume),
                    'aws': Award.objects.filter(resume=app.resume),
                    'schools': School.objects.filter(resume=app.resume),
                    'skills': Skill.objects.filter(resume=app.resume),
                    'msgs': msgs,
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
                    x = Message()
                    x.code = 'info'
                    x.message = 'Cover letter requested successfully!'
                    x.company = post.company
                    x.save()
                    xx = Notification()
                    xx.code = 100
                    xx.message = post.company.name + ' requests a cover letter for your application to the ' \
                        + post.title + ' position. Go to the application details to submit your cover letter'
                    xx.student = Student.objects.get(pk=a.student.pk)
                    xx.save()
                    a.cover_requested = True
                    a.save()
                else:
                    m = Message()
                    m.code = 'warning'
                    m.company = post.company
                    m.message = 'A cover letter was already sent to the applicant; you will be' \
                                ' notified when a cover letter is received'
                    m.save()
            apps = Application.objects.filter(post=post).filter(status='active')
            if page >= apps.count():
                page = 0
            elif page < 0:
                page = apps.count() - 1
            xx = apps[page]
            app = Applicant(xx, xx.student)
            msgs = Message.objects.filter(company=post.company)
            context = {
                'app': app,
                'page': page,
                'resume': app.resume,
                'lan': Language.objects.filter(resume=app.resume),
                'exp': Experience.objects.filter(resume=app.resume),
                'aws': Award.objects.filter(resume=app.resume),
                'schools': School.objects.filter(resume=app.resume),
                'skills': Skill.objects.filter(resume=app.resume),
                'msgs': msgs,
            }
            for m in msgs:
                m.delete()
            return render(request, self.template_name, context)


class ApplicantDetailsView(View):
    template_name = 'post/applicant_details.html'

    def get(self, request, pk):
        x = Application.objects.get(pk=pk)
        xx = Applicant(x, x.student)
        context = {
            'app': xx,
            'resume': xx.resume,
            'lan': Language.objects.filter(resume=xx.resume),
            'exp': Experience.objects.filter(resume=xx.resume),
            'aws': Award.objects.filter(resume=xx.resume),
            'schools': School.objects.filter(resume=xx.resume),
            'skills': Skill.objects.filter(resume=xx.resume),
        }
        post = x.post
        post.notified = False
        post.save()
        return render(request, self.template_name, context)


class DiscardApplicant(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        x.status = 'closed'
        x.save()
        xx = Message()
        xx.code = 'info'
        xx.message = 'Applicant successfully removed.'
        xx.company = x.post.company
        xx.save()
        n = Notification()
        n.student = x.student
        n.message = 'Your application for the ' + x.post.title + ' opportunity was discontinued.'
        n.save()
        return redirect('post:applicants', pk=pk)


class RequestCover(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        post = x.post
        if not x.cover_requested:
            x.cover_requested = True
            x.save()
            xx = Message()
            xx.code = 'info'
            xx.message = 'Cover letter successfully requested.'
            xx.company = post.company
            xx.save()
            xxx = Notification()
            xxx.student = x.student
            xxx.code = 100
            xxx.message = post.company.name + ' requests a cover letter for your application to the ' \
                        + post.title + ' position. Go to the application details to submit your cover letter'
            xxx.save()
        else:
            m = Message()
            m.code = 'warning'
            m.company = post.company
            m.message = 'A cover letter was already sent to the applicant; you will be notified when a cover letter ' \
                        'is received.'
            m.save()
        return redirect('post:applicants', pk=pk)


class CustomPost:

    def __init__(self, post, company):
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
        self.resume = app.resume
        self.post = app.post
        self.cover = app.cover
        self.cover_requested = app.cover_requested
        self.cover_submitted = app.cover_submitted
        self.date_applied = app.date
