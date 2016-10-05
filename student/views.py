from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Student
from post.models import Application
from home.models import Message, Notification, JobinSchool
from .forms import NewStudentForm
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    template_name = 'student/student_home.html'

    def get(self, request):
        res = Student.objects.filter(user=request.user)
        if res.count() > 0:
            apps = Application.objects.filter(student=res.first()).filter(status='active')
            msgs = Message.objects.filter(student=res.first())
            notifications = Notification.objects.filter(student=res.first()).filter(opened=False)
            context = {
                'student': res.first(),
                'apps': apps,
                'msgs': msgs,
                'notifications': notifications,
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        else:
            return redirect('student:new')


class NewStudentView(CreateView):
    model = Student
    form_class = NewStudentForm

    def form_valid(self, form):
        student = form.save(commit=False)
        student.user = self.request.user
        student.email = self.request.user.email
        ext = student.email.split('@', 1)
        student.school = JobinSchool.objects.filter(email=ext[1].lower())
        x = Message()
        x.code = 'info'
        x.message = 'Your profile was created successfully. Welcome to Jobin!'
        x.student = student
        return super(NewStudentView, self).form_valid(form)


class UpdateStudentView(UpdateView):
    model = Student
    form_class = NewStudentForm

    def get_context_data(self, **kwargs):
        context = super(UpdateStudentView, self).get_context_data(**kwargs)
        context['update'] = 'True'
        return context

    def form_valid(self, form):
        student = Student.objects.get(user=self.request.user)
        x = Message()
        x.code = 'info'
        x.message = 'Your profile was successfully updated.'
        x.student = student
        return super(UpdateStudentView, self).form_valid(form)


class DetailsView(generic.DetailView):
    model = Student
    template_name = 'student/student_details.html'


class ActivityView(View):
    template_name = 'student/student_activity.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            apps = Application.objects.filter(student=student)
            notes = Notification.objects.filter(student=student)
            context = {
                'notifications': notes,
                'applications': apps
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')


class ProfileView(View):
    template_name = 'student/student_profile.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            return render(request, self.template_name, {'student': student, 'user': student.user})
        except ObjectDoesNotExist:
            return redirect('student:new')

