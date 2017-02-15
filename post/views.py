from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post, Application
from .classes import Applicant
from .forms import NewPostForm
from .utils import PostContexts, ApplicantUtil, ApplicationUtil, PostUtil
from home.models import JobinSchool, JobinProgram, JobinMajor
from home.utils import MessageCenter, Pagination
from company.models import Company
from student.models import Student
from resume.models import Resume
from django.core.exceptions import ObjectDoesNotExist
#from wkhtmltopdf.views import PDFTemplateResponse


class CompanyPosts(View):
    template_name = 'post/company_posts.html'

    def get(self, request):
        company = Company.objects.get(user=self.request.user)
        posts = Post.objects.filter(company=company, status='open')
        msgs = MessageCenter.get_messages('company', company)
        ex_posts = Post.objects.filter(company=company, status='closed')
        temp = PostUtil.do_post_notifications(posts)
        if len(temp) > 0:
            MessageCenter.new_applicants_message(company, temp)
        context = {
            'posts': Pagination.get_page_items(posts),
            'expired_posts': Pagination.get_page_items(ex_posts),
            'company': company,
            'msgs': msgs,
            'ppages': Pagination.get_pages(posts),
            'ppage': 1,
            'xpages': Pagination.get_pages(ex_posts),
            'xpage': 1,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request):
        company = Company.objects.get(user=self.request.user)
        ppage = int(request.POST.get('post_page'))
        xpage = int(request.POST.get('xpost_page'))
        posts = Post.objects.filter(company=company, status='open')
        msgs = MessageCenter.get_messages('company', company)
        ex_posts = Post.objects.filter(company=company, status='closed')
        temp = PostUtil.do_post_notifications(posts)
        if len(temp) > 0:
            MessageCenter.new_applicants_message(company, temp)
        context = {
            'posts': Pagination.get_page_items(posts, ppage),
            'expired_posts': Pagination.get_page_items(ex_posts, xpage),
            'company': company,
            'msgs': msgs,
            'ppages': Pagination.get_pages(posts, ppage),
            'ppage': ppage + 1,
            'xpages': Pagination.get_pages(ex_posts, xpage),
            'xpage': xpage + 1,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class NewPostView(CreateView):
    model = Post
    form_class = NewPostForm

    def get_context_data(self, **kwargs):
        context = super(NewPostView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['company'] = company
        return context

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        post = form.save(commit=False)
        post.schools = 'ALL'
        post.company = company
        post.is_startup_post = company.is_startup
        MessageCenter.post_created(company, post.title)
        return super(NewPostView, self).form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = NewPostForm

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['company'] = company
        context['update'] = 'True'
        return context

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        post = form.save(commit=False)
        MessageCenter.post_updated(company, post.title)
        return super(PostUpdateView, self).form_valid(form)


class ClosePostView(View):

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.status = 'closed'
        post.notified = False
        post.save()
        MessageCenter.post_closed(post.company, post.title)
        MessageCenter.post_closed_notification(post.company, post.title)
        apps = ApplicationUtil.get_post_applications(post)
        for x in apps:
            x.status = 'hold'
            x.save()
            MessageCenter.post_closed_student_notification(x.student, x.post_title)
        return redirect('post:companyposts')


class CompanyPost(View):
    template_name = 'post/company_post.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        l = ApplicantUtil.get_post_applicants(post)
        msgs = MessageCenter.get_messages('company', post.company)
        context = {
            'company': post.company,
            'post': post,
            'applicants': l[0:10],
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
            resumes = Resume.objects.filter(student=student, is_complete=True, status='open')
            l = PostUtil.get_student_posts(student, pt, pk)
            rkey = 0
            for r in resumes:
                if r.is_active:
                    rkey = r.pk
            msgs = MessageCenter.get_messages('student', student)
            notes = MessageCenter.get_notifications('student', student)
            context = PostContexts.get_student_posts_context(pt, student, l, resumes, rkey)
            context['msgs'] = msgs
            context['notifications'] = notes
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')

    def post(self, request, pk, pt):
        r = request.POST.get('rk')
        student = Student.objects.get(user=self.request.user)
        resumes = Resume.objects.filter(student=student, is_complete=True, status='open')
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
        student = app.student
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        msgs = MessageCenter.get_messages('student', student)
        context = {
            'post': post,
            'comp': post.company,
            'app': app,
            'msgs': msgs,
            'nav_student': student,
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
            MessageCenter.cover_letter_submitted(app.student, app.post_title)
            MessageCenter.cover_letter_received(post.company, app.post_title, app.student_name)
            return redirect('student:index')
        MessageCenter.cover_letter_blank(app.student)
        msgs = MessageCenter.get_messages('student', app.student)
        student = app.student
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'post': post,
            'app': app,
            'msgs': msgs,
            'nav_student': student
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class ApplyView(View):

    def get(self, request, pk, pt):
        post = Post.objects.get(pk=pk)
        student = Student.objects.get(user=self.request.user)
        r = Resume.objects.filter(student=student, is_active=True)
        if ApplicationUtil.already_applied(student, post):
            MessageCenter.already_applied(student, post.title)
            return redirect('post:studentposts', pk=pk, pt=pt)
        if r.count() > 0:
            ApplicationUtil.new_application(post, student, r.first())
            MessageCenter.apply_message(student, post.title)
            return redirect('post:studentposts', pk=pk, pt=pt)
        else:
            MessageCenter.apply_no_resume(student)
            return redirect('resume:index')


class PostApplicantsView(View):
    template_name = 'post/post_applicants.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        l = ApplicantUtil.get_post_applicants(post)
        msgs = MessageCenter.get_messages('company', post.company)
        program = JobinProgram.objects.filter(name=post.programs)
        context = {
            'post': post,
            'list': Pagination.get_page_items(l, 0, 2),
            'msgs': msgs,
            'schools': JobinSchool.objects.all(),
            'majors': JobinMajor.objects.filter(program=program),
            'count': len(l),
            'pages': Pagination.get_pages(l, 0, 2),
            'page': 1,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk):
        page = int(request.POST.get('page'))
        post = Post.objects.get(pk=pk)
        program = JobinProgram.objects.filter(name=post.programs)
        apps = ApplicantUtil.get_post_applicants(post)
        filters = ApplicantUtil.prep_app_filters(request, post)
        l = ApplicantUtil.apply_filters(filters, apps, post)
        msgs = MessageCenter.get_messages('company', post.company)
        school_val = ''
        major_val = ''
        gpa_val = 0
        if filters:
            for x in filters['schools']:
                school_val += x + ','
            for x in filters['majors']:
                major_val += x + ','
            gpa_val = filters['gpa']
        context = {
            'post': post,
            'list': Pagination.get_page_items(l, page, 2),
            'msgs': msgs,
            'schools': JobinSchool.objects.all(),
            'majors': JobinMajor.objects.filter(program=program),
            'count': len(l),
            'pages': Pagination.get_pages(l, page, 2),
            'page': page + 1,
            'gpa_val': (gpa_val if gpa_val > 0 else ''),
            'major_val': major_val,
            'school_val': school_val,
        }
        for m in msgs:
            m.delete()
        return render(request, self.template_name, context)


class SingleApplicantView(View):
    template_name = 'post/post_applicant.html'

    def get(self, request, pk, ak):
        post = Post.objects.get(pk=pk)
        apps = ApplicantUtil.get_post_applicants(post)
        if len(apps) > 0:
            app = apps[0]
        else:
            MessageCenter.no_applicants_left(post.company)
            return redirect('post:applicants', pk=post.pk)
        page = 0
        if not int(ak) == 0:
            for x in apps:
                if int(x.pk) == int(ak):
                    app = x
                    break
                page += 1
        ApplicationUtil.update_opened_application(app.pk)
        context = PostContexts.get_applicant_context(app)
        msgs = MessageCenter.get_messages('company', post.company)
        context['msgs'] = msgs
        context['page'] = page
        for m in msgs:
            m.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk, ak):
        post = Post.objects.get(pk=pk)
        keep = request.POST.get('keep')
        page = int(request.POST.get('page'))
        cover = request.POST.get('cover')
        if keep == 'Delete':
            x = Application.objects.get(pk=ak)
            x.status = 'closed'
            x.save()
            MessageCenter.applicant_removed(post.company, x.student_name)
            MessageCenter.application_discontinued(x.student, x.post_title)
        if cover == 'True':
            a = Application.objects.get(pk=ak)
            if not a.cover_requested:
                MessageCenter.cover_letter_request(post.company, a.student_name)
                MessageCenter.cover_letter_notification(a.student, post.company.name, post.title)
                a.cover_requested = True
                a.cover_submitted = False
                a.cover_opened = False
                a.save()
            else:
                MessageCenter.cover_letter_already_requested(post.company)

        apps = ApplicantUtil.get_post_applicants(post)
        filters = ApplicantUtil.prep_app_filters(request, post)
        if filters:
            apps = ApplicantUtil.apply_filters(filters, apps, post)

        if len(apps) > 0:
            if page >= len(apps):
                page = 0
            elif page < 0:
                page = len(apps) - 1

            if not int(ak) == 0 and not keep == 'Delete':
                page = 0
                for x in apps:
                    if int(x.pk) == int(ak):
                        break
                    page += 1

            app = apps[page]
            ApplicationUtil.update_opened_application(app.pk)
            context = PostContexts.get_applicant_context(app)
            msgs = MessageCenter.get_messages('company', post.company)
            context['msgs'] = msgs
            context['page'] = page
            school_val = ''
            major_val = ''
            gpa_val = 0
            if filters:
                for x in filters['schools']:
                    school_val += x + ','
                for x in filters['majors']:
                    major_val += x + ','
                    gpa_val = filters['gpa']
            context['gpa_val'] = (gpa_val if gpa_val > 0 else '')
            context['major_val'] = major_val
            context['school_val'] = school_val
            for m in msgs:
                m.delete()
            return render(request, self.template_name, context)
        else:
            MessageCenter.no_applicants_left(post.company)
            return redirect('post:applicants', pk=pk)


class PostRecoveryView(View):
    form_class = NewPostForm
    template_name = 'post/post_form.html'

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        company = post.company
        MessageCenter.post_reactivate_info_message(company)
        form = self.form_class(instance=post)
        msgs = MessageCenter.get_messages('company', company)
        context = {
            'form': form,
            'company': company,
            'msgs': msgs,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, pk):
        company = Company.objects.get(user=self.request.user)
        p = Post.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=p)

        if form.is_valid():
            post = form.save(commit=False)
            post.company = company
            post.is_startup_post = company.is_startup
            post.schools = 'ALL'
            post.status = 'open'
            post.save()
            MessageCenter.post_reactivated(company, post.title)
            apps = ApplicationUtil.get_held_applications(post)
            for x in apps:
                MessageCenter.post_reactivated_notification(x.student, post.title, company)
                x.cover_requested = False
                x.save()
            return redirect('post:companyposts')
        msgs = MessageCenter.get_messages('company', company)
        context = {
            'company': company,
            'msgs': msgs,
            'form': form,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


def close_old_application(request, ak):

    if request.method == 'GET':
        app = ApplicationUtil.get_application(ak)
        app.status = 'closed'
        app.save()
        MessageCenter.application_withdrew(app.student, app.post_title)
        return redirect('student:index')
    return redirect('home:index')


def activate_old_application(request, ak):

    if request.method == 'GET':
        app = ApplicationUtil.get_application(ak)
        app.status = 'active'
        app.save()
        MessageCenter.application_continued(app.student, app.post_title)
        return redirect('student:index')
    return redirect('home:index')


class DiscardApplicant(View):

    def get(self, request, pk, ak):
        x = Application.objects.get(pk=ak)
        x.status = 'closed'
        x.save()
        MessageCenter.applicant_removed(x.post.company, x.student_name)
        MessageCenter.application_discontinued(x.student, x.post_title)
        return redirect('post:applicants', pk=pk)


class ApplicantPDF(View):
    template_name = 'post/applicant_resume_pdf.html'

    def get(self, request, ak):
        a = Application.objects.get(pk=ak)
        app = Applicant(a, a.student)
        filename = app.fname + app.lname + 'Resume.pdf'
        context = PostContexts.get_applicant_context(app)
        reponse = 'none'
        # response = PDFTemplateResponse(
        #     request=request,
        #     template=self.template_name,
        #     filename=filename,
        #     context=context,
        #     show_content_in_browser=False,
        #     cmd_options={
        #         'page-size': 'A4',
        #         'orientation': 'portrait',
        #         'disable-smart-shrinking': True,
        #     },
        # )
        #return response
        context = PostContexts.get_applicant_context(app)
        return render(request, self.template_name, context)

















