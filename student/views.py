from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Student
from post.models import Application
from event.models import EventInterest
from home.models import Message, Notification, JobinSchool, JobinTerritory, JobinProgram, JobinMajor
from home.utils import new_message
from .forms import NewStudentForm
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
import simplejson
from django.http import HttpResponse


class IndexView(View):
    template_name = 'student/student_home.html'

    def get(self, request):
        res = Student.objects.filter(user=request.user)
        if res.count() > 0:
            events = EventInterest.objects.filter(student=res.first(), active=True)
            apps = Application.objects.filter(student=res.first()).filter(status='active')
            msgs = Message.objects.filter(student=res.first())
            notifications = Notification.objects.filter(student=res.first()).filter(opened=False)
            context = {
                'student': res.first(),
                'apps': apps,
                'events': events,
                'msgs': msgs,
                'notifications': notifications,
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        else:
            ext = self.request.user.email.split('@', 1)
            s = JobinSchool.objects.filter(email=ext[1].lower())
            if s.count() == 0:
                logout(request)
                return redirect('home:closed')
            return redirect('student:new')


class NewStudentView(CreateView):
    model = Student
    form_class = NewStudentForm

    def get_context_data(self, **kwargs):
        context = super(NewStudentView, self).get_context_data(**kwargs)
        ext = self.request.user.email.split('@', 1)
        school = JobinSchool.objects.filter(email=ext[1].lower())
        context['school'] = school.first()
        return context

    def form_valid(self, form):
        student = form.save(commit=False)
        student.user = self.request.user
        student.email = self.request.user.email
        ext = student.email.split('@', 1)
        school = JobinSchool.objects.filter(email=ext[1].lower())
        if school.count() == 0:
            logout(self.request)
            return redirect('home:index')
        elif school.count() > 0:
            student.school = school.first().name
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
        msg = 'Your profile was successfully updated.'
        new_message('student', student, 'info', msg)
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

def get_states(request, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')

def get_states_update(request,pk, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')


def get_majors(request, program_id):
    program = JobinProgram.objects.get(name=program_id)
    majors = JobinMajor.objects.filter(program=program)
    major_dic = {}
    for major in majors:
        major_dic[major.name] = major.name
    return HttpResponse(simplejson.dumps(major_dic), content_type='application/json')


def get_majors_update(request,pk, program_id):
    program = JobinProgram.objects.get(name=program_id)
    majors = JobinMajor.objects.filter(program=program)
    major_dic = {}
    for major in majors:
        major_dic[major.name] = major.name
    return HttpResponse(simplejson.dumps(major_dic), content_type='application/json')
