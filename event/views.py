from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from django.views.generic import View
from django.shortcuts import redirect
from .models import Event, EventInterest
from home.models import Message
from home.utils import new_message, get_messages
from .forms import NewEventForm
from company.models import Company
from student.models import Student


class CompanyEvents(generic.ListView):
    template_name = 'event/company_events.html'
    context_object_name = 'list'

    def get_queryset(self):
        return Event.objects.filter(company=Company.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super(CompanyEvents, self).get_context_data(**kwargs)
        msgs = Message.objects.filter(company=Company.objects.get(user=self.request.user))
        context['msgs'] = msgs
        for x in msgs:
            x.delete()
        return context


class NewEventView(CreateView):
    model = Event
    form_class = NewEventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        event.company = Company.objects.get(user=self.request.user)
        msg = 'Your event was created successfully.'
        new_message('company', event.company, 'info', msg)
        return super(NewEventView, self).form_valid(form)


class EventUpdateView(UpdateView):
    model = Event
    form_class = NewEventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        msg = 'Your event was updated successfully.'
        new_message('company', event.company, 'info', msg)
        return super(EventUpdateView, self).form_valid(form)


class CompanyEvent(generic.DetailView):
    model = Event
    template_name = 'event/company_event.html'


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
        student = Student.objects.filter(user=self.request.user)
        context = super(StudentEvents, self).get_context_data(**kwargs)
        context['count'] = Event.objects.count()
        msgs = get_messages('student', student)
        context['msgs'] = msgs
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


