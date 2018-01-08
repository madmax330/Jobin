from django.shortcuts import render, redirect, Http404, HttpResponse
from django.views.generic import View
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
        if user.is_logged_in():
            if user.get_user_type() == 'company':
                return redirect('company:index')
            elif user.get_user_type() == 'student':
                return redirect('student:index')
            else:
                user.log_user_out(self.request)

        return render(request, 'home/index.html')

    def post(self, request):
        user = UserUtil(self.request.user)
        rq = RequestUtil()
        i = rq.get_login_info(self.request)
        if i:
            t = user.log_user_in(self.request, i)
            if t > 0:
                if user.get_user_type() == 'company':
                    return redirect('company:index')
                elif user.get_user_type() == 'student':
                    if not HomeUtil.open_school(user.get_user().email):
                        return redirect('home:closed')
                    return redirect('student:index')
                else:
                    return render(request, self.template_name, {'login_error': 'Invalid user type.'})
            elif t < 0:
                return render(request, 'home/utils/email/verify.html', i)
            else:
                return render(request, self.template_name, {'login_error': str(user.get_errors())})
        else:
            return render(request, self.template_name, {'login_error': str(rq.get_errors())})


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
        context = {
            'type': ut
        }
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if user.new_user(info, ut == 'student'):
                    user.log_user_in(request, info)
                    if ut == 'student':
                        return redirect('student:new')
                    elif ut == 'company':
                        return redirect('company:new')
                    else:
                        return render(request, 'home/index.html', {'register_error': 'Unknown registration type.'})
                else:
                    raise IntegrityError

        except IntegrityError:
            context['register_error'] = str(user.get_errors())
            return render(request, self.template_name, context)


def verify(request):
    if request.method == 'GET':
        return render(request, 'home/utils/email/verify.html')

    raise Http404


def activate(request, key):
    if request.method == 'GET':
        user = UserUtil(request.user)

        try:
            with transaction.atomic():
                if user.activate_user(key):
                    return render(request, 'home/utils/email/activate.html')
                else:
                    raise IntegrityError
        except IntegrityError:
            errs = str(user.get_errors())
            return render(request, 'home/utils/email/activate.html', {'errors': errs})

    raise Http404


def new_verification(request):
    if request.method == 'POST':
        user = UserUtil(request.user)
        rq = RequestUtil()
        i = rq.get_login_info(request)
        if i:

            try:
                with transaction.atomic():
                    if user.new_activation_key(i):
                        return render(request, 'home/utils/email/verify.html', {'msg': 'New link sent successfully.'})
                    else:
                        raise IntegrityError
            except IntegrityError:
                return render(request, 'home/utils/email/verify.html', {'errors': str(user.get_errors())})

        else:
            return render(request, 'home/utils/email/verify.html', {'errors': str(rq.get_errors())})

    raise Http404


def school_closed(request):
    if request.method == 'GET':
        return render(request, 'home/school_not_open.html')

    raise Http404


class ChangeUserInfo(LoginRequiredMixin, View):
    template_name = 'home/student_change_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

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
                                    if user.log_user_out(request):
                                        return redirect('home:verify')
                                    raise IntegrityError
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
                                                'email': user.get_user().email,
                                                'password': i['password']
                                            }
                                    ):
                                        m = 'Password changed successfully.'
                                        if ut == 'student':
                                            student = StudentContainer(user.get_user())
                                            MessageCenter.new_notification('student', student.get_student(), 100, m)
                                            MessageCenter.new_message('student', student.get_student(), 'success', m)
                                            return redirect('student:index')
                                        elif ut == 'company':
                                            company = CompanyContainer(user.get_user())
                                            MessageCenter.new_notification('company', company.get_company(), 100, m)
                                            MessageCenter.new_message('company', company.get_company(), 'success', m)
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


class NewPasswordView(View):
    template_name = 'home/utils/email/change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = UserUtil(request.user)
        mail = request.POST.get('email')
        if mail:

            try:
                with transaction.atomic():
                    if user.new_password(mail):
                        return render(request, 'home/index_page/home.html',
                                      {'success_msg': 'Password changed successfully.'})
                    else:
                        raise IntegrityError
            except IntegrityError:
                return render(request, self.template_name, {'errors': user.get_errors()})

        else:
            return render(request, self.template_name, {'errors': 'Invalid email.'})


@login_required(login_url='/')
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


@login_required(login_url='/')
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


def students_about(request):
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
        return render(request, 'home/students_about.html', context)

    raise Http404


def company_about(request):
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
        return render(request, 'home/company_about.html', context)

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

#
#
#   API VIEWS
#
#
