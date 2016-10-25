from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import NewUserForm
from .models import JobinSchool, Notification, JobinRequestedEmail, Message, JobinBlockedEmail
from student.models import Student
from company.models import Company
from django.views.generic import View


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
            elif utype == 'student':
                g = Group.objects.get(name='student_user')
                g.user_set.add(user)
                ext = user.email.split('@', 1)[1]
                ems = JobinSchool.objects.filter(email=ext.lower())
                if ems.count() == 0:
                    x = JobinRequestedEmail()
                    x.extension = ext.lower()
                    x.save()
            else:
                return redirect('home:index')
            return redirect('home:verify')
        return render(request, self.template_name, {'form': form})


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
                elif es.count > 0:
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
