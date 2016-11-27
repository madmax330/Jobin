from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import redirect
from .models import Event, EventInterest
from home.utils import new_message, get_messages, get_notifications
from home.models import JobinTerritory
from .forms import NewEventForm
from company.models import Company
from student.models import Student
import simplejson
from django.http import HttpResponse


class CompanyEvents(generic.ListView):
    template_name = 'event/company_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(company=Company.objects.get(user=self.request.user), active=True)

    def get_context_data(self, **kwargs):
        company = Company.objects.get(user=self.request.user)
        context = super(CompanyEvents, self).get_context_data(**kwargs)
        msgs = get_messages('company', company)
        context['company'] = company
        context['expired_events'] = Event.objects.filter(company=company, active=False)
        context['msgs'] = msgs
        for x in msgs:
            x.delete()
        return context


class NewEventView(CreateView):
    model = Event
    form_class = NewEventForm

    def get_context_data(self, **kwargs):
        context = super(NewEventView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['company'] = company
        return context

    def form_valid(self, form):
        event = form.save(commit=False)
        event.company = Company.objects.get(user=self.request.user)
        msg = 'Your event was created successfully.'
        new_message('company', event.company, 'info', msg)
        return super(NewEventView, self).form_valid(form)


class EventUpdateView(UpdateView):
    model = Event
    form_class = NewEventForm

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['company'] = company
        return context

    def form_valid(self, form):
        event = form.save(commit=False)
        msg = 'Your event was updated successfully.'
        new_message('company', event.company, 'info', msg)
        return super(EventUpdateView, self).form_valid(form)


class CompanyEvent(generic.DetailView):
    model = Event
    template_name = 'event/company_event.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyEvent, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        context['company'] = company
        return context


class StudentEvents(generic.ListView):
    template_name = 'event/student_events.html'
    context_object_name = 'list'

    def get_queryset(self):
        student = Student.objects.filter(user=self.request.user).first()
        pk = self.kwargs['pk']
        l = []
        es = Event.objects.filter(active=True)
        templ = []
        flag = False
        for x in es:
            if int(x.pk) == int(pk) > 0:
                flag = True
            xx = x.company
            xxx = CustomEvent(x, xx, student)
            if flag:
                l.append(xxx)
            else:
                templ.append(xxx)
        l.extend(templ)
        return l

    def get_context_data(self, **kwargs):
        student = Student.objects.get(user=self.request.user)
        context = super(StudentEvents, self).get_context_data(**kwargs)
        context['count'] = Event.objects.count()
        msgs = get_messages('student', student)
        notes = get_notifications('student', student)
        context['msgs'] = msgs
        context['nav_student'] = student
        context['notifications'] = notes
        return context


class NewInterest(View):

    def get(self, request, pk):
        student = Student.objects.filter(user=self.request.user).first()
        event = Event.objects.get(pk=pk)
        interest = EventInterest()
        interest.student = student
        interest.event = event
        interest.save()
        msg = 'Your interest in event: ' + event.title + ' noted, you can view this event in your "Interested Events"' \
                                                         ' in the Home page.'
        new_message('student', student, 'info', msg)
        return redirect('event:studentevents', pk=pk)


def get_states(request, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    state_dic = sorted(state_dic)
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')


def get_states_update(request,pk, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    state_dic = sorted(state_dic)
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')


class CustomEvent:

    def __init__(self, e, c, s):
        self.pk = e.pk
        self.name = c.name
        self.cweb = c.website
        self.caddr = c.address + ', ' + c.city + ', ' + c.state + ', ' + c.zipcode
        self.logo = c.logo
        self.title = e.title
        self.address = e.address + ', ' + e.city + ', ' + e.state + ', ' + e.zipcode
        self.date = e.date
        self.time = e.time
        self.website = e.website
        self.desc = e.description
        if EventInterest.objects.filter(student=s, event=e).count() > 0:
            self.interested = True
        else:
            self.interested = False


