from django.views.generic import View
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from home.util_home import HomeUtil
from home.utils import MessageCenter, Pagination
from home.util_activation import ActivationUtil

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
            'new': True,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        student = StudentContainer(request.user)
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
            'new': True,
        }
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if student.new_student(info, request.user):
                    m = 'Student profile created successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    return redirect('student:index')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['student'] = info
            context['errors'] = student.get_form().errors

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
        context = {
            'student': student.get_student(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'programs': HomeUtil.get_student_programs(),
            'majors': HomeUtil.get_majors(),
            'tab': 'profile',
        }
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if student.edit_student(info):
                    m = 'Student profile edited successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    return redirect('student:index')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['student'] = info
            context['errors'] = student.get_form().errors

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
            msgs = MessageCenter.get_messages('student', student.get_student())
            context = {
                'student': s,
                'user': student.get_user(),
                'schools': HomeUtil.get_schools(),
                'countries': HomeUtil.get_countries(),
                'tab': 'profile',
                'messages': msgs,
            }
            MessageCenter.clear_msgs(msgs)
            return render(request, 'student/profile.html', context)

    raise Http404


@login_required(login_url='/')
def add_transcript(request):
    if request.method == 'POST':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_transcript(request.POST, request.FILES):
                    m = 'Transcript uploaded successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    data = {'is_valid': True}
                    return JsonResponse(data)
                else:
                    raise IntegrityError
        except IntegrityError:
            data = {'is_valid': False, 'error': str(student.get_errors())}
            return JsonResponse(data)

    raise Http404


@login_required(login_url='/')
def delete_transcript(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_transcript():
                    m = 'File resume deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=pk)

    raise Http404


@login_required(login_url='/')
def request_school_verification(request):
    if request.method == 'POST':
        student = StudentContainer(request.user)
        activation = ActivationUtil(request.user)
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if activation.send_student_school_verification(info) and student.request_school_verification(info):
                    m = 'A verification was sent to your school email.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors()) + '\n' + str(activation.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:profile')

    raise Http404


@login_required(login_url='/')
def request_new_school_verification(request):
    if request.method == 'POST':
        student = StudentContainer(request.user)
        activation = ActivationUtil(request.user)
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if activation.send_student_school_verification(info) and student.request_school_verification(info):
                    m = 'A verification was sent to your school email.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors()) + '\n' + str(activation.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:profile')

    raise Http404


@login_required(login_url='/')
def verify_student_school(request, key):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        activation = ActivationUtil(request.user)

        try:
            with transaction.atomic():
                if activation.verify_student_school(key) and student.school_verified():
                    m = 'Your school was verified successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors()) + '\n' + str(activation.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:profile')

    raise Http404


@login_required(login_url='/')
def change_school(request):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.change_school():
                    m = 'Old school successfully removed, you must still verify your new school.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:profile')

    raise Http404


@login_required(login_url='/')
def request_new_school(request):
    if request.method == 'POST':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.request_new_school(request.POST.copy()):
                    m = 'New school request sent successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('student:profile')

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
