from .models import EventInterest, Event
from home.utils import MessageCenter
import datetime


class EventUtil:

    @staticmethod
    def do_upcoming_notifications(student):
        events = EventInterest.objects.filter(student=student)
        today = datetime.datetime.now().date()
        rem_date = (datetime.datetime.now() + datetime.timedelta(days=4)).date()
        for x in events:
            if today < x.date < rem_date:
                msg = 'Event ' + x.event_name + ' is coming up soon!'
                MessageCenter.new_notification('student', student, 100, msg)












