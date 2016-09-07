from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post, Application
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


class NewPostView(CreateView):
    model = Post
    form_class = NewPostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.schools = 'ALL'
        post.programs = 'ALL'
        post.company = Company.objects.filter(user=self.request.user).first()
        return super(NewPostView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = NewPostForm


class CompanyPost(View):
    template_name = 'post/company_post.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post)
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            l.append(xx)
        return render(request, self.template_name, {'post': post, 'applicants': l})


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
            return render(request, self.template_name, {'list': l, 'count': len(l), 'resumes': resumes, 'rkey': rkey})
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

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, self.template_name, {'x': post})


class ApplyView(View):

    def get(self, request, pk, rk):
        post = Post.objects.get(pk=pk)
        resume = Resume.objects.get(pk=rk)
        student = Student.objects.get(user=self.request.user)
        if resume is not None:
            app = Application()
            app.post_title = post.title
            app.post = post
            app.student = student
            app.resume = resume
            app.date = datetime.datetime.now()
            app.status = 'active'
            app.save()
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
        return render(request, self.template_name, {'post': post, 'list': l})

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        school_filter = request.POST.get('school')
        program_filter = request.POST.get('program')
        keep = request.POST.get('keep')
        apps = Application.objects.filter(post=post).filter(status='active')
        l = []
        for x in apps:
            xx = Applicant(x, x.student)
            if school_filter and program_filter:
                if xx.school in school_filter and xx.program in program_filter:
                    l.append(xx)
            elif school_filter:
                if xx.school in school_filter:
                    l.append(xx)
            elif program_filter:
                if xx.program in program_filter and xx not in l:
                    l.append(xx)
        if not keep:
            d = []
            for x in apps:
                xx = Applicant(x, x.student)
                if school_filter and program_filter:
                    if xx.school not in school_filter and xx.program not in program_filter:
                        d.append(x)
                elif program_filter:
                    if xx.program not in program_filter:
                        d.append(x)
                elif school_filter:
                    if xx.school not in school_filter:
                        d.append(x)
            for x in d:
                x.status = 'closed'
                x.save()
        return render(request, self.template_name, {'post': post, 'list': l})


class SingleApplicantView(View):
    template_name = 'post/post_applicant.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        apps = Application.objects.filter(post=post).filter(status='active')
        if apps.count() > 0:
            xx = Application.objects.filter(post=post).filter(status='active')[0]
        else:
            return redirect('post:applicants', pk=post.pk)  # msg
        app = Applicant(xx, xx.student)
        context = {
            'app': app,
            'page': 0,
            'resume': app.resume,
            'lan': Language.objects.filter(resume=app.resume),
            'exp': Experience.objects.filter(resume=app.resume),
            'aws': Award.objects.filter(resume=app.resume),
            'schools': School.objects.filter(resume=app.resume),
            'skills': Skill.objects.filter(resume=app.resume),
        }
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
            apps = Application.objects.filter(post=post).filter(status='active')
            if apps.count() > 0:
                if page >= apps.count():
                    page = 0
                xx = apps[page]
                app = Applicant(xx, xx.student)
                context = {
                    'app': app,
                    'page': page,
                    'resume': app.resume,
                    'lan': Language.objects.filter(resume=app.resume),
                    'exp': Experience.objects.filter(resume=app.resume),
                    'aws': Award.objects.filter(resume=app.resume),
                    'schools': School.objects.filter(resume=app.resume),
                    'skills': Skill.objects.filter(resume=app.resume),
                }
                return render(request, self.template_name, context)
            else:
                return redirect('post:applicants', pk=pk)
        else:
            if cover == 'True':
                pass
            apps = Application.objects.filter(post=post).filter(status='active')
            if page >= apps.count():
                page = 0
            elif page < 0:
                page = apps.count() - 1
            xx = apps[page]
            app = Applicant(xx, xx.student)
            context = {
                'app': app,
                'page': 1,
                'resume': app.resume,
                'lan': Language.objects.filter(resume=app.resume),
                'exp': Experience.objects.filter(resume=app.resume),
                'aws': Award.objects.filter(resume=app.resume),
                'schools': School.objects.filter(resume=app.resume),
                'skills': Skill.objects.filter(resume=app.resume),
            }
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
        return render(request, self.template_name, context)


class DiscardApplicant(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        x.status = 'closed'
        x.save()
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
        self.date_applied = app.date
