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


def index_view(request):
    if request.method == 'GET':
        user = UserUtil(request.user)
        if user.is_logged_in():
            if user.get_user_type() == 'company':
                return redirect('company:index')
            elif user.get_user_type() == 'student':
                return redirect('student:index')
            else:
                user.log_user_out(request)

        return render(request, 'home/index.html')

    raise Http404


def login_student(request):
    if request.method == 'POST':
        user = UserUtil(request.user)
        errors = []
        info = request.POST.copy()

        t = user.log_user_in(request, info)
        if t > 0:
            return redirect('student:index')
        elif t < 0:
            return render(request, 'home/utils/email/verify.html', {'email': info['email']})
        else:
            errors.append({
                'code': 'danger',
                'message': str(user.get_errors())
            })
            return render(request, 'home/index.html',
                          {'messages': errors, 'student_email': info['email'], 'panel': 'student'})

    raise Http404


def login_company(request):
    if request.method == 'POST':
        user = UserUtil(request.user)
        errors = []
        info = request.POST.copy()

        t = user.log_user_in(request, info)
        if t > 0:
            return redirect('company:index')
        elif t < 0:
            return render(request, 'home/utils/email/verify.html', {'email': info['email']})
        else:
            errors.append({
                'code': 'danger',
                'message': str(user.get_errors())
            })
            return render(request, 'home/index.html',
                          {'messages': errors, 'company_email': info['email'], 'panel': 'company'})

    raise Http404


def user_logout(request):
    if request.method == 'GET':
        user = UserUtil(request.user)
        if user.log_user_out(request):
            return redirect('home:index')
        return redirect('home:index')

    raise Http404


def register_company(request):
    if request.method == 'POST':
        user = UserUtil(request.user)
        info = request.POST.copy()
        info['username'] = info['email']
        errors = []
        context = {
            'panel': 'company',
            'company_register_email': info['email']
        }

        try:
            with transaction.atomic():
                if user.new_user(info, False):
                    return render(request, 'home/utils/email/verify.html', {'new': True})
                else:
                    raise IntegrityError
        except IntegrityError:
            errors.append({
                'code': 'danger',
                'message': str(user.get_errors())
            })
            context['messages'] = errors
            return render(request, 'home/index.html', context)


def register_student(request):
    if request.method == 'POST':
        user = UserUtil(request.user)
        info = request.POST.copy()
        info['username'] = info['email']
        errors = []
        context = {
            'panel': 'student',
            'student_register_email': info['email']
        }

        try:
            with transaction.atomic():
                if user.new_user(info, True):
                    if user.log_user_in(request, info):
                        return redirect('student:new')
                raise IntegrityError
        except IntegrityError:
            errors.append({
                'code': 'danger',
                'message': str(user.get_errors())
            })
            context['messages'] = errors
            return render(request, 'home/index.html', context)


def verify(request):
    if request.method == 'GET':
        return render(request, 'home/utils/email/verify.html')

    raise Http404


def activate_company(request, key):
    if request.method == 'GET':
        user = UserUtil(request.user)

        try:
            with transaction.atomic():
                if user.activate_company(key):
                    return render(request, 'home/utils/email/activate.html')
                else:
                    raise IntegrityError
        except IntegrityError:
            errs = str(user.get_errors())
            return render(request, 'home/utils/email/activate.html', {'errors': errs})

    raise Http404


def activate_student(request, key):
    if request.method == 'GET':
        user = UserUtil(request.user)

        try:
            with transaction.atomic():
                if user.activate_student(key):
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
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if user.new_activation_key(info):
                    return render(request, 'home/utils/email/verify.html', {'msg': 'New link sent successfully.', 'email': info['email']})
                else:
                    raise IntegrityError
        except IntegrityError:
            return render(request, 'home/utils/email/verify.html', {'errors': str(user.get_errors()), 'email': info['email']})

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
                                    return render(request, 'home/utils/email/verify.html', {'email': i['email']})
                                else:
                                    raise IntegrityError
                            elif ut == 'company':
                                company = CompanyContainer(user.get_user())
                                if user.change_user_email(i, company=company.get_company()):
                                    if user.log_user_out(request):
                                        return render(request, 'home/utils/email/verify.html', {'email': i['email']})
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
                                            return redirect('student:profile')
                                        elif ut == 'company':
                                            company = CompanyContainer(user.get_user())
                                            MessageCenter.new_notification('company', company.get_company(), 100, m)
                                            MessageCenter.new_message('company', company.get_company(), 'success', m)
                                            return redirect('company:profile')
                                        else:
                                            return redirect('home:index')
                            raise IntegrityError

                except IntegrityError:
                    return render(request, self.template_name, {'error': str(user.get_errors())})
            else:
                return render(request, self.template_name, {'error': 'Incorrect password.'})

        else:
            return render(request, self.template_name, {'error': str(rq.get_errors())})


def new_password_view(request, ut):
    if request.method == 'POST':
        user = UserUtil(request.user)
        info = request.POST.copy()
        errors = []
        if ut == 'student':
            student = StudentContainer(user.get_user(email=info['email']))
            if student.get_student():
                if not student.get_student().dob == info['dob']:
                    errors.append({
                        'code': 'danger',
                        'message': 'Unable to verify user, double check the information you provided.'
                    })
            else:
                errors.append({
                    'code': 'danger',
                    'message': 'User not found, double check the information you provided.'
                })
        elif ut == 'company':
            company = CompanyContainer(user.get_user(email=info['email']))
            if company.get_company():
                if not company.get_company().zipcode == info['zipcode']:
                    errors.append({
                        'code': 'danger',
                        'message': 'Unable to verify user, double check the information you provided.'
                    })
            else:
                errors.append({
                    'code': 'danger',
                    'message': 'User not found, double check the information you provided.'
                })
        else:
            errors.append({
                'code': 'danger',
                'message': 'Invalid user type found.'
            })
        if errors:
            return render(request, 'home/index.html', {'messages': errors})
        else:
            try:
                with transaction.atomic():
                    if user.new_password(info['email']):
                        return render(
                            request,
                            'home/index.html',
                            {'messages': [{'code': 'success', 'message': 'Password changed successfully.'}]}
                        )
                    else:
                        raise IntegrityError
            except IntegrityError:
                for x in user.get_errors():
                    errors.append({'code': 'danger', 'message': x})
                return render(request, 'home/index.html', {'messages': errors})


def terms_and_conditions(request):
    if request.method == 'GET':
        return render(request, 'home/terms_and_conditions.html')

    raise Http404


def privacy_policy(request):
    if request.method == 'GET':
        return render(request, 'home/privacy_policy.html')

    raise Http404


def create_test_content(request, n):
    if request.method == 'GET':
        try:
            with transaction.atomic():
                ContentGen.gen_test_content(int(n), company=False)
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
