from .models import Message, Notification
from student.models import Student
from company.models import Company


def new_message(t, u, code, message):
    m = Message()
    m.code = code
    m.message = message
    if t == 'student':
        m.student = u
    elif t == 'company':
        m.company = u
    m.save()


def get_messages(t, u):
    if t == 'student':
        return Message.objects.filter(student=u)
    elif t == 'company':
        return Message.objects.filter(company=u)


def clear_msgs(msgs):
    for x in msgs:
        x.delete()


def new_notification(t, u, code, message):
    n = Notification()
    n.code = code
    n.message = message
    if t == 'student':
        n.student = u
    elif t == 'company':
        n.company = u
    n.save()


def get_notifications(t, u):
    if t == 'student':
        return Notification.objects.filter(student=u, opened=False)
    if t == 'company':
        return Notification.objects.filter(company=u, opened=False)
