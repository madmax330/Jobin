from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Student
from post.models import Application
from event.models import EventInterest
from resume.models import Resume
from home.models import JobinSchool, JobinTerritory, JobinProgram, JobinMajor, Notification
from home.utils import MessageCenter
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
            events = EventInterest.objects.filter(student=student, active=True)
            apps = Application.objects.filter(student=student, status='active')
            old_apps = Application.objects.filter(student=student, status='hold', post__status='open')
            resumes = Resume.objects.filter(student=student, is_complete=True)
            msgs = MessageCenter.get_messages('student', student)
            notifications = MessageCenter.get_notifications('student', student)
            if len(student.email) > 30:
                student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
            context = {
                'nav_student': student,
                'apps': apps,
                'old_apps': old_apps,
                'events': events,
                'resumes': resumes,
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
            npages = list(range(1, 2))
            ncount = notes.count()
            if (ncount/10) >= 1:
                npages = list(range(1, int(ncount/10) + 1))
            if len(npages) > 10:
                npages = npages[0:10]
            apages = list(range(1, 2))
            acount = apps.count()
            if (acount / 10) >= 1:
                apages = list(range(1, int(acount / 10) + 1))
            if len(apages) > 10:
                apages = apages[0:10]
            epages = list(range(1, 2))
            ecount = len(events)
            if (ecount / 10) >= 1:
                epages = list(range(1, int(ecount / 10) + 1))
            if len(epages) > 10:
                epages = epages[0:10]
            context = {
                'nav_student': student,
                'all_notifications': notes[0:10],
                'notifications': notes.filter(opened=False),
                'applications': apps[0:10],
                'events': events[0:10],
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
        note_start = int(note_page) * 10
        app_start = int(app_page) * 10
        event_start = int(event_page) * 10
        npages = list(range(1, 2))
        ncount = notes.count()
        nval = int(ncount / 10)
        if nval > 0:
            npages = list(range(1, nval + 1))
            if note_page - 5 > 0:
                if note_page + 5 < nval:
                    npages = npages[note_page - 5: note_page + 5]
                else:
                    npages = npages[note_page - 5:]
            else:
                if len(npages) > 10:
                    npages = npages[0:10]
        apages = list(range(1, 2))
        acount = apps.count()
        aval = int(acount / 10)
        if aval > 0:
            apages = list(range(1, aval + 1))
            if app_page - 5 > 0:
                if app_page + 5 < aval:
                    apages = apages[app_page - 5: app_page + 5]
                else:
                    apages = apages[app_page - 5:]
            else:
                if len(apages) > 10:
                    apages = apages[0:10]
        epages = list(range(1, 2))
        ecount = len(events)
        e_val = int(ecount / 10)
        if e_val > 0:
            epages = list(range(1, e_val + 1))
            if event_page - 5 > 0:
                if event_page + 5 < e_val:
                    epages = epages[event_page - 5: event_page + 5]
                else:
                    epages = epages[event_page - 5:]
            else:
                if len(epages) > 10:
                    epages = epages[0:10]

        context = {
            'nav_student': student,
            'all_notifications': notes[note_start: note_start+10],
            'notifications': notes.filter(opened=False),
            'applications': apps[app_start: app_start+10],
            'events': events[event_start: event_start+10],
            'ncount': notes.count(),
            'acount': apps.count(),
            'ecount': len(events),
            'npages': npages,
            'apages': apages,
            'epages': epages,
            'npage': note_page,
            'apage': app_page,
            'epage': event_page,
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
