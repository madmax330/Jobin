from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from .forms import NewUserForm
from .forms import ForgetFormUSer
from .models import JobinSchool, Notification, JobinRequestedEmail, Message, JobinBlockedEmail,JobinInvalidUser
from student.models import Student
from company.models import Company
from django.views.generic import View
from datetime import datetime
from home.token import generate_confirmation_token, confirm_token
from home.email import send_email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import string
import random

#request = HttpRequest()
class IndexView(View):
    template_name = 'home/home.html'

    # not logged in
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='company_user').exists():
                    return redirect('company:index')
                elif user.groups.filter(name='student_user').exists():
                    return redirect('student:index')
                elif user.groups.filter(name='unvalid_user').exists():
                    infos = 'Your account is not verified yet, please confirm your account with the link sent to you by mail'
                    return redirect('home:invalid_user', Infos=infos)
                else:
                    return redirect('home:index')
        return render(request, self.template_name, {'error': 'Username or password is incorrect.'})


class RegisterView(View):
    form_class = NewUserForm
    template_name = 'home/register.html'

    # blank form
    def get(self, request, utype):
        form = self.form_class(None)
        context = {
            'form': form,
            'type': utype
        }
        return render(request, self.template_name, context)


    # process form data
    def post(self, request, utype):
        form = self.form_class(request.POST, utype=utype)

        if form.is_valid():
            user = form.save(commit=False)
            # clean data
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            if utype == 'company':
                g = Group.objects.get(name='company_user')
                g.user_set.add(user)
                return redirect('home:index')
            elif utype == 'student':
                g = Group.objects.get(name='student_user')
                g.user_set.add(user)
                ext = user.email.split('@', 1)[1]
                ems = JobinSchool.objects.filter(email=ext.lower())
                if ems.count() == 0:
                    x = JobinRequestedEmail()
                    x.extension = ext.lower()
                    x.save()
                return redirect('home:index')
        return render(request, self.template_name, {'form': form})

            #Temp user create
            #temp_user =  JobinInvalidUser()

            #if utype == 'company':
             #   temp_user.user = user
              #  temp_user.category = 'company'
               # temp_user.date = datetime.now()
                #temp_user.save()
                #token = generate_confirmation_token(user.email)
                #url = request.build_absolute_uri()
                #confirm_url = url + 'confirm_email/' + token
                #html = render_to_string('home/active.html', {'confirm_url': confirm_url})
                #text_content = strip_tags(html)
                #subject = "Please confirm your email"
                #send_email(user.email, subject, html, text_content)
                #g = Group.objects.get(name='invalid_user')
                #g.user_set.add(user)

            #elif utype == 'student':
             #   temp_user.user = user
              #  temp_user.category ='student'
               # temp_user.date = datetime.now()
                #temp_user.save()
                #token = generate_confirmation_token(user.email)
                #url = request.build_absolute_uri()
                #confirm_url = url + 'confirm_email/' + token
                #html = render_to_string('home/active.html', {'confirm_url': confirm_url})
                #text_content = strip_tags(html)
                #subject = "Please confirm your email"
                #send_email(user.email, subject, html,text_content )
                #g = Group.objects.get(name='invalid_user')
                #g.user_set.add(user)

            #else:
             #   return redirect('home:index')
            #return redirect('home:verify')



class ChangeUserInfo(View):
    template_name = 'home/user_info_change.html'

    def get(self, request, utype):
        if utype == 'company':
            return render(request, self.template_name,
                          {
                              'user': self.request.user,
                              'type': utype,
                          })
        elif utype == 'student':
            return render(request, self.template_name,
                          {
                              'user': self.request.user,
                              'type': utype,
                          })
        else:
            return redirect('home:index')

    def post(self, request, utype):
        user = self.request.user
        email = request.POST.get('email')
        cemail = request.POST.get('cemail')
        password = request.POST.get('pass')
        cpassword = request.POST.get('cpass')
        context = {
            'user': user,
            'type': utype
        }
        if email and password:
            context['error'] = 'You cannot change email and password at the same time.'
            return render(request, self.template_name, context)
        if email:
            if not email == cemail:
                context['error'] = 'Email fields do not match.'
                return render(request, self.template_name, context)
            if utype == 'company':
                company = Company.objects.get(user=user)
                company.email = email
                company.save()
            if utype == 'student':
                ext = email.split('@', 1)[1]
                ems = JobinBlockedEmail.objects.filter(extension=ext.lower())
                if ems.count() > 0:
                    context['error'] = 'This email is not a valid email.'
                    return render(request, self.template_name, context)
                student = Student.objects.get(user=user)
                es = JobinSchool.objects.filter(email=ext.lower())
                if es.count() == 0:
                    jre = JobinRequestedEmail()
                    jre.extension = ext.lower()
                    jre.save()
                elif es.count() > 0:
                    school = es.first().name
                    student.school = school
                student.email = email
                student.save()
            user.email = email
            user.username = email
            user.save()
            logout(request)
            return redirect('home:verify')
        if password:
            if not password == cpassword:
                context['error'] = 'Password fields do not match.'
                return render(request, self.template_name, context)
            user.set_password(password)
            user.save()
            x = Message()
            x.code = 'info'
            x.message = 'Your password was successfully changed.'
            xx = Notification()
            xx.code = 0
            xx.message = 'You password was successfully changed.'
            if utype == 'company':
                company = Company.objects.get(user=user)
                x.company = company
                xx.company = company
                x.save()
                xx.save()
                logout(request)
                new_user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, new_user)
                    return redirect('company:index')
            elif utype == 'student':
                student = Student.objects.get(user=user)
                x.student = student
                xx.student = student
                x.save()
                xx.save()
                logout(request)
                new_user = authenticate(username=user.username, password=password)
                if user is not None:
                    login(request, new_user)
                    return redirect('student:index')
        context['error'] = 'Fields cannot be left blank.'
        return render(request, self.template_name, context)


class VerifyView(View):
    template_name = 'home/verify.html'

    def get(self, request):
        return render(request, self.template_name)

class UnvalidUser(View):
    template_name = 'home/invalid_user.html'

    def get(self, request,Infos):
        return render(request, self.template_name, {'Infos': Infos})

class NotOpenView(View):
    template_name = 'home/notopen.html'

    def get(self, request):
        return render(request, self.template_name)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home:index')


class CloseNotification(View):

    def get(self, request, u, pk):
        n = Notification.objects.get(pk=pk)
        n.opened = True
        n.save()
        if u == 'company':
            return redirect('company:index')
        elif u == 'student':
            return redirect('student:index')
        logout(request)
        return redirect('home:index')


class CloseAllNotifications(View):

    def get(self, request, u):
        if u == 'company':
            ns = Notification.objects.filter(company=Company.objects.filter(user=self.request.user).first())
            for x in ns:
                x.opened = True
                x.save()
            return redirect('company:index')
        elif u == 'student':
            ns = Notification.objects.filter(student=Student.objects.filter(user=self.request.user).first())
            for x in ns:
                x.opened = True
                x.save()
            return redirect('student:index')
        logout(request)
        return redirect('home:index')

def Reset_password(request):
    template_name = 'home/password_forget.html'

    return render(request,template_name,)


class Change_password(View):
    form_class = ForgetFormUSer
    template_name = 'home/invalid_user.html'
    def post(self, request):
        form = self.form_class(request.POST)
        Infos = 'Error with the form'
        if form.is_valid():
            # clean data
            email = form.data['email']
            user_auth = User.objects.get(username=email)
            Infos = 'An email has been send with a new password. Note you can change it afterwards'
            if user_auth.groups.filter(name='student_user').exists() or user_auth.groups.filter(name='company_user').exists() :
                # Just alphanumeric characters
                chars = string.ascii_letters + string.digits

                sizeOfPass = 10
                password = ''.join((random.choice(chars)) for x in range(sizeOfPass))
                user_auth.set_password(password)
                user_auth.save()
                Infos_email =  password
                html = render_to_string('home/password_changed_confirmation.html', {'Infos': Infos_email})
                text_content = strip_tags(html)
                subject = "Password change request"
                send_email(email, subject, html,text_content)
            else:
                Infos = 'The email entered does not appear in our database'

        return render(request,self.template_name,{'Infos': Infos})

def confirm_email(request,token):
    try:
        email = confirm_token(token)
    except:
        infos = 'The confirmation link is invalid or has expired.'
        return redirect('home:invalid_user', Infos=infos)
    user_auth = User.objects.get(username=email)
    if not user_auth.groups.filter(name='invalid_user').exists():
        infos = 'Account already confirmed. Please login.'
        return redirect('home:invalid_user', Infos=infos)
    else:

        try:
          user = JobinInvalidUser.objects.get(user=email)
        except:
            infos = 'User cannot be found!'
            return redirect('home:invalid_user', Infos=infos)

        if user.category == 'company':
         g = Group.objects.get(name='company_user')
         g.user_set.add(user_auth)
        elif user.category == 'student':
            g = Group.objects.get(name='student_user')
            g.user_set.add(user_auth)
            ext = user_auth.email.split('@', 1)[1]
            ems = JobinSchool.objects.filter(email=ext.lower())
            if ems.count() == 0:
                x = JobinRequestedEmail()
                x.extension = ext.lower()
                x.save()
        g = Group.objects.get(name='invalid_user')
        g.user_set.remove(user_auth)
        infos = 'You have confirmed your account. Thanks!'

    return redirect('home:invalid_user', Infos=infos)


