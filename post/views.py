from django.views.generic import View
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from company.util_company import CompanyContainer
from student.util_student import StudentContainer
from home.utils import MessageCenter, Pagination
from home.util_request import RequestUtil
from home.util_home import HomeUtil

from wkhtmltopdf.views import PDFTemplateResponse


@login_required(login_url='/')
def company_index(request):
    if request.method == 'GET':
        post_page = request.GET.get('pp', 1)
        ex_post_page = request.GET.get('xp', 1)
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
        msgs = MessageCenter.get_messages('company', company.get_company())
        posts = Pagination(company.get_posts(), 10)
        expired_posts = Pagination(company.get_expired_posts(), 10)
        context = {
            'company': company.get_company(),
            'posts': posts.get_page(post_page),
            'expired_posts': expired_posts.get_page(ex_post_page),
            'messages': msgs,
            'tab': 'posts',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'post/company_index.html', context)

    raise Http404


class NewPostView(LoginRequiredMixin, View):
    template_name = 'post/post_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        company = CompanyContainer(request.user)
        context = {
            'programs': HomeUtil.get_programs(),
            'company': company.get_company(),
            'tab': 'posts',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        context = {
            'programs': HomeUtil.get_programs(),
            'company': company.get_company(),
            'tab': 'posts',
            'new': True,
        }

        try:

            with transaction.atomic():
                if company.new_post(request.POST.copy()):
                    return redirect('post:company_posts')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['post'] = request.POST
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


class EditPostView(LoginRequiredMixin, View):
    template_name = 'post/post_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'post': company.get_post(pk),
            'programs': HomeUtil.get_programs(),
            'tab': 'posts',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'programs': HomeUtil.get_programs(),
            'tab': 'posts',
        }
        info = request.POST.copy()
        info['id'] = pk

        try:
            with transaction.atomic():
                if company.edit_post(pk, info):
                    return redirect('post:company_post', pk=pk)
                else:
                    raise IntegrityError

        except IntegrityError:
            context['post'] = info
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


@login_required(login_url='/')
def close_post(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.close_post(pk):
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(company.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def post_detail(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        msgs = MessageCenter.get_messages('company', company.get_company())
        post = company.get_post(pk)
        post.type = POST_CATEGORIES[post.type]
        context = {
            'company': company.get_company(),
            'post': post,
            'app_count': company.application_count(pk),
            'messages': msgs,
            'tab': 'posts',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'post/detail.html', context)

    raise Http404


POST_CATEGORIES = {
    'internship': 'Internship',
    'part_time': 'Part Time',
    'full_time': 'Full Time',
    'volunteer': 'Volunteer',
    'startup': 'Startup',
}


@login_required(login_url='/')
def student_index(request, cat, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        msgs = MessageCenter.get_messages('student', student.get_student())
        rq = RequestUtil()
        filters = rq.get_student_post_filter(request)
        posts = student.get_posts(cat, pk, filters)
        context = {
            'student': student.get_student(),
            'resumes': student.get_resumes(),
            'posts': posts,
            'count': len(posts),
            'category': cat,
            'd_category': POST_CATEGORIES[cat],
            'internship_count': student.get_post_count('internship', filters),
            'volunteer_count': student.get_post_count('volunteer', filters),
            'part_time_count': student.get_post_count('part_time', filters),
            'full_time_count': student.get_post_count('full_time', filters),
            'startup_count': student.get_post_count('startup', filters),
            'messages': msgs,
            'filters': filters,
            'tab': 'posts',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'post/student_index.html', context)

    raise Http404


@login_required(login_url='/')
def student_detail(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        msgs = MessageCenter.get_messages('student', student.get_student())
        app = student.get_application(pk)
        context = {
            'post': app.post,
            'application': app,
            'messages': msgs,
            'student': student.get_student(),
            'tab': 'posts',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'post/student_detail.html', context)

    raise Http404


@login_required(login_url='/')
def request_cover_letter(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.request_cover_letter(pk):
                    m = 'Cover letter requested successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(company.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def submit_cover_letter(request, pk):
    if request.method == 'POST':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.submit_cover_letter(pk, request.POST.copy()):
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def apply(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.new_application(pk):
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def post_applicants(request, pk):
    if request.method == 'GET' or request.method == 'POST':
        page = request.GET.get('page')
        company = CompanyContainer(request.user)
        post = company.get_post(pk)
        company.no_new_apps(post)
        program = HomeUtil.get_program(post.programs)
        msgs = MessageCenter.get_messages('company', company.get_company())
        filters = None
        if request.method == 'GET':
            apps = Pagination(company.get_applications(pk), 25)
        elif request.method == 'POST':
            rq = RequestUtil()
            filters = rq.get_applications_filter(request)
            apps = Pagination(company.get_applications(pk, filters=filters), 25)
        else:
            apps = None
        context = {
            'post': post,
            'applications': (apps.get_page(page) if apps else None),
            'count': (apps.count if apps else 0),
            'schools': HomeUtil.get_schools(),
            'majors': HomeUtil.get_program_majors(
                program) if not post.programs == 'All Programs' else HomeUtil.get_majors(),
            'filters': filters if filters else None,
            'messages': msgs,
            'applicants': 'True',
            'tab': 'posts',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'post/post_applicants.html', context)

    raise Http404


@login_required(login_url='/')
def single_applicant(request, pk, ak):
    if request.method == 'POST':
        company = CompanyContainer(request.user)
        post = company.get_post(pk)
        rq = RequestUtil()
        filters = rq.get_applications_filter(request)

        if filters is None:
            MessageCenter.new_message('company', company.get_company(), 'danger', str(rq.get_errors()))
        apps = company.get_applications(pk, ak=ak, filters=filters)
        if apps and len(apps) > 0:
            prev_app = apps[len(apps) - 1]
            app = apps[0]
            next_app = apps[(1 if 1 < len(apps) else 0)]
            if not ak == '0':
                for i in range(0, len(apps)):
                    if str(apps[i].id) == ak:
                        prev_app = apps[i - 1] if i - 1 >= 0 else apps[len(apps) - 1]
                        app = apps[i]
                        next_app = apps[i + 1] if i + 1 < len(apps) else apps[0]
            msgs = MessageCenter.get_messages('company', company.get_company())
            context = {
                'messages': msgs,
                'app': company.get_extended_application(app),
                'next_app': next_app.id,
                'prev_app': prev_app.id,
                'post': post,
                'company': company.get_company(),
                'filters': filters,
                'filter_schools': filters['schools'].split(',') if filters and filters['schools'] else None,
                'filter_majors': filters['majors'].split(',') if filters and filters['majors'] else None,
                'tab': 'posts',
            }
            MessageCenter.clear_msgs(msgs)
            return render(request, 'post/post_applicant.html', context)

        if filters:
            m = 'There are no more candidates in this filter.'
        else:
            m = 'There are no more applications for this post.'
        MessageCenter.new_message('company', company.get_company(), 'warning', m)
        return redirect('post:applicants', pk=pk)

    raise Http404


class RecoverPostView(LoginRequiredMixin, View):
    template_name = 'post/post_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        company = CompanyContainer(self.request.user)
        post = company.get_post(pk)
        context = {
            'company': company.get_company(),
            'post': post,
            'tab': 'posts',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        company = CompanyContainer(self.request.user)
        context = {
            'company': company.get_company(),
            'tab': 'posts',
        }
        info = request.POST.copy()
        info['id'] = pk

        try:
            with transaction.atomic():
                if company.recover_post(pk, info):
                    return redirect('post:company_posts')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['post'] = info
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


@login_required(login_url='/')
def withdraw_application(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.withdraw_application(pk):
                    m = 'Application successfully withdrawn.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:index')

    raise Http404


@login_required(login_url='/')
def activate_application(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.activate_application(pk):
                    m = 'Application successfully activated.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:index')

    raise Http404


@login_required(login_url='/')
def discard_application(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.close_application(pk):
                    m = 'Application successfully closed.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse(status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(company.get_errors())
            return HttpResponse(m, status=400)

        raise Http404

    raise Http404


@login_required(login_url='/')
def save_application(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.save_application(pk):
                    m = 'Application saved successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse(status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(company.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def remove_application_save(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.remove_application_save(pk):
                    m = 'Application no longer saved.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse(status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(company.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def increment_count(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        if student.increment_view_count(pk):
            return HttpResponse(status=200)
        else:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


class ApplicantPDF(LoginRequiredMixin, View):
    template_name = 'post/applicant_resume_pdf.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, ak):
        company = CompanyContainer(self.request.user)
        app = company.get_extended_application(company.get_application(ak))
        filename = app.name + 'Resume.pdf'
        context = {'app': app}
        # response = 'none'
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename=filename,
            context=context,
            show_content_in_browser=False,
            cmd_options={
                'page-size': 'A4',
                'orientation': 'portrait',
                'disable-smart-shrinking': True,
            },
        )
        return response
        # context = PostContexts.get_applicant_context(app)
        # return render(request, self.template_name, context)


class StudentResumePDF(LoginRequiredMixin, View):
    template_name = 'post/applicant_resume_pdf.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, rk):
        student = StudentContainer(self.request.user)
        app = student.get_pdf_resume_info(rk)
        filename = app['name'] + 'Resume.pdf'
        context = {'app': app}
        # response = 'none'
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            filename=filename,
            context=context,
            show_content_in_browser=False,
            cmd_options={
                'page-size': 'A4',
                'orientation': 'portrait',
                'disable-smart-shrinking': True,
            },
        )
        return response


#
#
#   API VIEWS
#
#
