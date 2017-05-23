from django.shortcuts import render, redirect, Http404, HttpResponse
from django.views.generic import View
from django.db import transaction, IntegrityError

from .content_gen import ContentGen
from .utils import MessageCenter
from .util_home import HomeUtil
from .util_user import UserUtil
from .util_request import RequestUtil
from company.util_company import CompanyContainer
from student.util_student import StudentContainer


class IndexView(View):
    template_name = 'home/index_page/home.html'

    def get(self, request):
        user = UserUtil(self.request.user)
        context = {}
        if user.is_logged_in():
            if user.get_user_type() == 'company':
                company = CompanyContainer(user.get_user())
                context['logged'] = 'company'
                context['user_name'] = company.get_company().name
            elif user.get_user_type() == 'student':
                student = StudentContainer(user.get_user())
                context['logged'] = 'student'
                context['user_name'] = student.get_student().name
        return render(request, self.template_name, context)

    def post(self, request):
        user = UserUtil(self.request.user)
        rq = RequestUtil()
        i = rq.get_login_info(self.request)
        if i:
            if user.log_user_in(self.request, i):
                if user.get_user_type() == 'company':
                    return redirect('company:index')
                elif user.get_user_type() == 'student':
                    if not HomeUtil.open_school(user.get_user().email):
                        return redirect('home:closed')
                    return redirect('student:index')
                else:
                    return render(request, self.template_name, {'error': 'Invalid user type.'})
            else:
                return render(request, self.template_name, {'error': str(user.get_errors())})
        else:
            return render(request, self.template_name, {'error': str(rq.get_errors())})


def user_logout(request):

    if request.method == 'GET':
        user = UserUtil(request.user)
        if user.log_user_out(request):
            return redirect('home:index')
        return redirect('home:index')

    raise Http404


class RegisterView(View):
    template_name = 'home/register.html'

    def get(self, request, ut):
        context = {
            'type': ut
        }
        return render(request, self.template_name, context)

    def post(self, request, ut):
        user = UserUtil(self.request.user)
        rq = RequestUtil()
        i = rq.get_user_info(self.request)
        if i:

            try:
                with transaction.atomic():
                    if user.new_user(i, ut == 'student'):
                        return redirect('home:verify')
                    else:
                        raise IntegrityError
            except IntegrityError:
                return render(request, self.template_name, {'error': str(user.get_errors())})

        else:
            return render(request, self.template_name, {'error': str(rq.get_errors())})


def verify(request):

    if request.method == 'GET':
        return render(request, 'home/verify.html')

    raise Http404


def school_closed(request):

    if request.method == 'GET':
        return render(request, 'home/school_not_open.html')

    raise Http404


class ChangeUserInfo(View):
    template_name = 'home/student_change_form.html'

    def get(self, request, ut):
        if ut == 'company':
            return render(request, 'home/company_change_form.html', {'user': self.request.user, 'type': ut})
        elif ut == 'student':
            return render(request, 'home/student_change_form.html', {'user': self.request.user, 'type': ut})
        else:
            return redirect('home:index')

    def post(self, request, ut):
        user = UserUtil(self.request.user)
        rq = RequestUtil()
        i = rq.get_user_change_info(self.request)
        if ut == 'company':
            self.template_name = 'home/company_change_form.html'
        elif ut == 'student':
            self.template_name = 'home/student_change_form.html'
        if i:

            if user.get_user().check_password(i['old_password']):
                try:
                    with transaction.atomic():
                        if i['email']:
                            if ut == 'student':
                                student = StudentContainer(user.get_user())
                                if user.change_user_email(i, student=student.get_student()):
                                    return redirect('home:verify')
                                else:
                                    raise IntegrityError
                            elif ut == 'company':
                                company = CompanyContainer(user.get_user())
                                if user.change_user_email(i, company=company.get_company()):
                                    return redirect('home:verify')
                                else:
                                    raise IntegrityError
                            else:
                                return render(request, self.template_name, {'error': 'Invalid request.'})
                        elif i['password']:
                            if user.change_user_password(i):
                                if user.log_user_out(self.request):
                                    if user.log_user_in(
                                            self.request,
                                            {
                                                'username': user.get_user().email,
                                                'password': i['password']
                                            }
                                    ):
                                        m = 'Password changed successfully.'
                                        if ut == 'student':
                                            student = StudentContainer(user.get_user())
                                            MessageCenter.new_notification('student', student.get_student(), 100, m)
                                            return redirect('student:index')
                                        elif ut == 'company':
                                            company = CompanyContainer(user.get_user())
                                            MessageCenter.new_notification('company', company.get_company(), 100, m)
                                            return redirect('company:index')
                                        else:
                                            return redirect('home:index')
                            raise IntegrityError

                except IntegrityError:
                    return render(request, self.template_name, {'error': str(user.get_errors())})
            else:
                return render(request, self.template_name, {'error': 'Incorrect password.'})

        else:
            return render(request, self.template_name, {'error': str(rq.get_errors())})


def close_notification(request, pk):

    if request.method == 'GET':

        try:
            with transaction.atomic():
                if MessageCenter.close_notification(pk):
                    return HttpResponse('Notification closed', status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            return HttpResponse('Invalid notification code.', status=400)

    raise Http404


def close_notifications(request, u):

    if request.method == 'GET':
        user = None
        if u == 'company':
            user = CompanyContainer(request.user).get_company()
        elif u == 'student':
            user = StudentContainer(request.user).get_student()

        if user:

            try:
                with transaction.atomic():
                    if MessageCenter.close_all_notifications(u, user):
                        return HttpResponse('Notifications closed.', status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                return HttpResponse('No notifications found.', status=400)

        return HttpResponse('Invalid user request.', status=400)

    raise Http404


def terms_and_conditions(request):

    if request.method == 'GET':
        user = UserUtil(request.user)
        context = {}
        if user.is_logged_in():
            if user.get_user_type() == 'company':
                company = CompanyContainer(user.get_user())
                context['logged'] = 'company'
                context['user_name'] = company.get_company().name
            elif user.get_user_type() == 'student':
                student = StudentContainer(user.get_user())
                context['logged'] = 'student'
                context['user_name'] = student.get_student().name
        return render(request, 'home/terms_and_conditions.html', context)

    raise Http404


def privacy_policy(request):

    if request.method == 'GET':
        user = UserUtil(request.user)
        context = {}
        if user.is_logged_in():
            if user.get_user_type() == 'company':
                company = CompanyContainer(user.get_user())
                context['logged'] = 'company'
                context['user_name'] = company.get_company().name
            elif user.get_user_type() == 'student':
                student = StudentContainer(user.get_user())
                context['logged'] = 'student'
                context['user_name'] = student.get_student().name
        return render(request, 'home/privacy_policy.html', context)

    raise Http404


def create_test_content(request, n):

    if request.method == 'GET':
        try:
            with transaction.atomic():
                ContentGen.gen_test_content(int(n))
                print('No error')
        except (IntegrityError, TypeError, ValueError) as e:
            print(str(e))
        return redirect('home:index')
    raise Http404


def clear_test_content(request):

    if request.method == 'GET':
        try:
            with transaction.atomic():
                ContentGen.clear_test_content()
                print('No error')
        except IntegrityError as e:
            print(str(e))
        return redirect('home:index')
    raise Http404



