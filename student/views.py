from django.views.generic import View
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from home.util_home import HomeUtil
from home.util_request import RequestUtil
from home.utils import MessageCenter, Pagination

from .util_student import StudentContainer


@login_required(login_url='/')
def index_view(request):

    if request.method == 'GET':
        app_page = request.GET.get('ap', 1)
        e_page = request.GET.get('ep', 1)
        p_page = request.GET.get('pp', 1)
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        msgs = MessageCenter.get_messages('student', student.get_student())
        a = student.get_applications()
        apps = Pagination(a if a else [], 15)
        events = Pagination(student.get_saved_events(), 15)
        posts = Pagination(student.get_newest_posts(), 5)
        context = {
            'student': student.get_student(),
            'applications': apps.get_page(app_page),
            'old_apps': student.get_old_applications(),
            'events': events.get_page(e_page),
            'posts': posts.get_page(p_page),
            'resumes': student.get_resumes(),
            'messages': msgs,
            'notifications': MessageCenter.get_notifications('student', student.get_student()),
            'tab': 'home',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'student/index.html', context)

    raise Http404


class NewStudentView(LoginRequiredMixin, View):
    template_name = 'student/student_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_student_info(request)
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
        }
        if i:

            try:
                with transaction.atomic():
                    if student.new_student(i, request.user):
                        m = 'Student profile created successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return redirect('student:index')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['student'] = i
                context['errors'] = student.get_form().errors

        else:
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


class EditStudentView(LoginRequiredMixin, View):
    template_name = 'student/student_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        student = StudentContainer(request.user)
        context = {
            'student': student.get_student(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
            'tab': 'profile',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_student_info(request)
        context = {
            'student': student.get_student(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
            'tab': 'profile',
        }
        if i:

            try:
                with transaction.atomic():
                    if student.edit_student(i):
                        m = 'Student profile edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return redirect('student:index')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['errors'] = student.get_form().errors

        else:
            context['errors'] = str(rq.get_errors())

        return render(request, self.template_name, context)


@login_required(login_url='/')
def history_view(request):

    if request.method == 'GET':
        app_page = request.GET.get('ap', 1)
        e_page = request.GET.get('ep', 1)
        n_page = request.GET.get('np', 1)
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        ap = Pagination(student.get_all_applications(), 10)
        ep = Pagination(student.get_all_saved_events(), 10)
        np = Pagination(list(MessageCenter.get_all_notifications('student', student.get_student())), 10)
        context = {
            'student': student.get_student(),
            'all_notifications': np.get_page(n_page),
            'applications': ap.get_page(app_page),
            'events': ep.get_page(e_page),
            'tab': 'history',
        }
        return render(request, 'student/history.html', context)

    raise Http404


@login_required(login_url='/')
def profile_view(request):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        else:
            s = student.get_student()
            context = {
                'student': s,
                'user': student.get_user(),
                'notifications': MessageCenter.get_notifications('student', s),
                'tab': 'profile'
            }
            return render(request, 'student/profile.html', context)

    raise Http404


@login_required(login_url='/')
def student_not_new(request):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        if student.not_new():
            return HttpResponse('good', status=200)
        else:
            return HttpResponse(str(student.get_errors()), status=400)

    raise Http404


#
#
#   API VIEWS
#
#

