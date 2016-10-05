from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import NewUserForm, StudentInfoForm, CompanyInfoForm
from .models import JobinSchool, Notification
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
        form = self.form_class(request.POST)

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
            else:
                return redirect('home:index')
            return redirect('home:verify')
        return render(request, self.template_name, {'form': form})


class ChangeUserInfo(View):
    template_name = 'home/user_info_change.html'
    student_form = StudentInfoForm
    company_form = CompanyInfoForm

    def get(self, request, utype):
        if utype == 'company':
            return render(request, self.template_name,
                          {
                              'user': self.request.user,
                              'type': utype,
                              'form': self.company_form
                          })
        elif utype == 'student':
            return render(request, self.template_name,
                          {
                              'user': self.request.user,
                              'type': utype,
                              'form': self.student_form
                          })
        else:
            return redirect('home:index')

    def post(self, request, utype):
        form = None
        if utype == 'company':
            form = self.company_form(request.POST)
        elif utype == 'student':
            form = self.student_form(request.POST)
        if form.is_valid():
            user = self.request.user
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if email:
                user.email = email
                user.save()
            elif password:
                user.set_password(password)
                user.save()
                return redirect('home:verify')
            if utype == 'student':
                return redirect('student:index')
            elif utype == 'company':
                return redirect('company:index')
        return render(request, self.template_name, {'user': self.request.user, 'type': utype, 'form': form})


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
