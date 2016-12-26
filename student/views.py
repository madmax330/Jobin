from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Student
from .utils import StudentUtil
from post.models import Application
from event.models import EventInterest
from event.utils import EventUtil
from resume.models import Resume
from home.models import JobinSchool, JobinTerritory, JobinProgram, JobinMajor, Notification
from home.utils import MessageCenter, Pagination
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
            student = res.first()
            msgs = MessageCenter.get_messages('student', student)
            notifications = MessageCenter.get_notifications('student', student)
            if len(student.email) > 30:
                student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
            context = StudentUtil.get_home_context(student, 0, 0)
            context['msgs'] = msgs
            context['notifications'] = notifications
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

    def post(self, request):
        student = Student.objects.get(user=self.request.user)
        app_page = int(request.POST.get('app_page'))
        event_page = int(request.POST.get('event_page'))
        msgs = MessageCenter.get_messages('student', student)
        notifications = MessageCenter.get_notifications('student', student)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = StudentUtil.get_home_context(student, app_page, event_page)
        context['msgs'] = msgs
        context['notifications'] = notifications
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


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
        MessageCenter.student_updated(student)
        return super(UpdateStudentView, self).form_valid(form)


class DetailsView(generic.DetailView):
    model = Student
    template_name = 'student/student_details.html'


class HistoryView(View):
    template_name = 'student/student_activity.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            apps = Application.objects.filter(student=student)
            es = EventInterest.objects.filter(student=student)
            events = []
            for x in es:
                events.append(x.event)
            notes = Notification.objects.filter(student=student)
            npages = Pagination.get_pages(notes)
            apages = Pagination.get_pages(apps)
            epages = Pagination.get_pages(events)
            if len(student.email) > 30:
                student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
            context = {
                'nav_student': student,
                'all_notifications': Pagination.get_page_items(notes),
                'notifications': notes.filter(opened=False),
                'applications': Pagination.get_page_items(apps),
                'events': Pagination.get_page_items(events),
                'ncount': notes.count(),
                'acount': apps.count(),
                'ecount': len(events),
                'npages': npages,
                'apages': apages,
                'epages': epages,
                'npage': 1,
                'apage': 1,
                'epage': 1,
            }
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')

    def post(self, request):
        student = Student.objects.get(user=self.request.user)
        note_page = int(request.POST.get('note_page'))
        app_page = int(request.POST.get('app_page'))
        event_page = int(request.POST.get('event_page'))
        apps = Application.objects.filter(student=student)
        es = EventInterest.objects.filter(student=student)
        events = []
        for x in es:
            events.append(x.event)
        notes = Notification.objects.filter(student=student)
        npages = Pagination.get_pages(notes, note_page)
        apages = Pagination.get_pages(apps, app_page)
        epages = Pagination.get_pages(events, event_page)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'nav_student': student,
            'all_notifications': Pagination.get_page_items(notes, note_page),
            'notifications': notes.filter(opened=False),
            'applications': Pagination.get_page_items(apps, app_page),
            'events': Pagination.get_page_items(events, event_page),
            'ncount': notes.count(),
            'acount': apps.count(),
            'ecount': len(events),
            'npages': npages,
            'apages': apages,
            'epages': epages,
            'npage': note_page + 1,
            'apage': app_page + 1,
            'epage': event_page + 1,
        }

        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = 'student/student_profile.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            notes = MessageCenter.get_notifications('student', student)
            return render(request, self.template_name, {'student': student, 'user': student.user, 'notifications': notes})
        except ObjectDoesNotExist:
            return redirect('student:new')


def get_states(request, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    state_dic = sorted(state_dic)
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')


def get_states_update(request, pk, country_name, state):
    current_state = JobinTerritory.objects.get(name=state)
    states = JobinTerritory.objects.filter(country=current_state.country)
    state_list = [current_state.name]
    state_dic = {}
    for x in states:
        if not x.name == current_state.name:
            state_dic[x.name] = x.name
    state_dic = sorted(state_dic)
    state_list.extend(state_dic)
    return HttpResponse(simplejson.dumps(state_list), content_type='application/json')


def get_majors(request, program_id):
    program = JobinProgram.objects.get(name=program_id)
    majors = JobinMajor.objects.filter(program=program)
    major_dic = {}
    for major in majors:
        major_dic[major.name] = major.name
    major_dic = sorted(major_dic)
    return HttpResponse(simplejson.dumps(major_dic), content_type='application/json')


def get_majors_update(request, pk, program_id, major):
    current_major = JobinMajor.objects.get(name=major)
    majors = JobinMajor.objects.filter(program=current_major.program)
    major_list = [current_major.name]
    major_dic = {}
    for x in majors:
        if not x.name == current_major.name:
            major_dic[x.name] = x.name
    major_dic = sorted(major_dic)
    major_list.extend(major_dic)
    return HttpResponse(simplejson.dumps(major_list), content_type='application/json')
