from django.views.generic.edit import CreateView, UpdateView
from django.views import generic
from .models import Event
from home.models import Message
from home.utils import new_message
from .forms import NewEventForm
from company.models import Company


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
        l = []
        es = Event.objects.all()
        for x in es:
            xx = CustomEvent(x, x.company)
            l.append(xx)
        return l

    def get_context_data(self, **kwargs):
        context = super(StudentEvents, self).get_context_data(**kwargs)
        context['count'] = Event.objects.count()
        return context


class CustomEvent:

    def __init__(self, e, c):
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


