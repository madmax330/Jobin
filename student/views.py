from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Student
from post.models import Application
from .forms import NewStudentForm
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    template_name = 'student/student_home.html'

    def get(self, request):
        res = Student.objects.filter(user=request.user)
        if res.count() > 0:
            apps = Application.objects.filter(student=res.first())
            return render(request, self.template_name, {'student': res.first(), 'apps': apps})
        else:
            return redirect('student:new')


class NewStudentView(CreateView):
    model = Student
    form_class = NewStudentForm

    def form_valid(self, form):
        student = form.save(commit=False)
        student.user = self.request.user
        student.email = self.request.user.email
        return super(NewStudentView, self).form_valid(form)


class UpdateStudentView(UpdateView):
    model = Student
    form_class = NewStudentForm


class DetailsView(generic.DetailView):
    model = Student
    template_name = 'student/student_details.html'


class ProfileView(View):
    template_name = 'student/student_profile.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            return render(request, self.template_name, {'student': student, 'user': student.user})
        except ObjectDoesNotExist:
            return redirect('student:new')

