from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Event, SavedEvent
from .forms import EventForm, NewSavedEventForm
from .classes import ExtendedEvent

from django.utils import timezone


class StudentEventContainer(BaseContainer):

    def __init__(self, student):
        super(StudentEventContainer, self).__init__()
        self._container_name = 'Student Event Container'
        self.__student = student
        self.__event = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def save_event(self, event):
        info = {
            'student': self.__student.id,
            'event': event.id,
            'start_date': event.start_date,
            'start_time': event.start_time,
            'end_date': event.end_date,
            'end_time': event.end_time,
            'event_name': event.title,
            'active': True,
        }
        self._form = NewSavedEventForm(info)
        if self._form.is_valid():
            self._form.save()
            event.times_saved += 1
            event.save()
            m = 'Event ' + event.title + ' successfully added to saved events.'
            if self.new_message(True, self.__student, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    def get_events(self, pk):
        es = Event.objects.filter(active=True)
        if es.count() > 0:
            all_events = [x for x in es if x.company.email.split('@', 1)[1].lower() == self.__student.user.email.split('@', 1)[1].lower()]
            rest_events = [x for x in es if x not in all_events]
            all_events.extend(rest_events)
            l = []
            temp = []
            flag = False
            for x in all_events:
                if int(x.id) == int(pk) > 0:
                    flag = True
                self.__event = x
                if flag:
                    l.append(ExtendedEvent(x, x.company, self.already_saved()))
                else:
                    temp.append(ExtendedEvent(x, x.company, self.already_saved()))
            l.extend(temp)
            return l
        else:
            self.add_error('No events found.')
            return []

    def get_saved_events(self):
        es = SavedEvent.objects.filter(student=self.__student, active=True)
        if es.count() > 0:
            l = []
            for x in es:
                l.append(x.event)
            return l
        self.add_error('No events found.')
        return []

    def get_all_saved_events(self):
        es = SavedEvent.objects.filter(student=self.__student).order_by('-id')
        if es.count() > 0:
            l = []
            for x in es:
                l.append(x.event)
            return l
        self.add_error('No events found.')
        return []

    def already_saved(self):
        return SavedEvent.objects.filter(event=self.__event, student=self.__student).count() > 0

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def remove_saved_event(self, pk):
        e = CompanyEventContainer.fetch_event(pk)
        if e:
            try:
                s = SavedEvent.objects.get(event=e, student=self.__student)
                s.active = False
                s.save()
                return True
            except ObjectDoesNotExist:
                self.add_error('Event not found.')
                return False
        self.add_error('Event not found.')
        return False


class CompanyEventContainer(BaseContainer):

    def __init__(self, company):
        super(CompanyEventContainer, self).__init__()
        self._container_name = 'Company Event Container'
        self.__company = company
        self.__event = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_event(self, info):
        info['company'] = self.__company.id
        self._form = EventForm(info)
        if self._form.is_valid():
            self.__event = self._form.save()
            m = 'New Event: ' + self.__event.title + ' successfully created.'
            if self.new_message(False, self.__company, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def edit_event(self, info):
        info['company'] = self.__company.id
        self._form = EventForm(info, instance=self.__event)
        if self._form.is_valid():
            self.__event = self._form.save()
            m = 'Event: ' + self.__event.title + ' edited successfully.'
            if self.new_message(False, self.__company, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def close_event(self):
        self.__event.active = False
        self.__event.save()
        m = 'Event "' + self.__event.title + '" closed on ' + str(timezone.now().date()) + '.'
        if self.new_message(False, self.__company, m, 2) and self.new_notification(False, self.__company, m, 100):
            return True
        else:
            return False

    def recover_event(self, info):
        info['company'] = self.__company.id
        self._form = EventForm(info, instance=self.__event)
        if self._form.is_valid():
            self.__event = self._form.save(commit=False)
            self.__event.active = True
            self.__event.save()
            m = 'Event: ' + self.__event.title + ' recovered successfully.'
            if self.new_message(False, self.__company, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    @staticmethod
    def fetch_event(pk):
        try:
            return Event.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get_event(self, pk=None):
        if pk:
            try:
                self.__event = Event.objects.get(pk=pk)
                if self.__event.company == self.__company:
                    return self.__event
                else:
                    self.add_error('Event not found.')
                    return None
            except ObjectDoesNotExist:
                self.add_error('Event not found.')
                return None
        else:
            return self.__event

    def get_events(self):
        events = Event.objects.filter(company=self.__company, active=True)
        if events.count() > 0:
            return list(events)
        else:
            self.add_error('No events found.')
            return []

    def get_expired_events(self):
        events = Event.objects.filter(company=self.__company, active=False)
        if events.count() > 0:
            return list(events)
        else:
            self.add_error('No expired events found.')
            return []

    #  DATA MODIFY FUNCTIONS (UPDATERS)


