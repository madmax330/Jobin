from event.models import EventInterest
from post.models import Application
from resume.models import Resume
from home.utils import Pagination


class StudentUtil:

    @staticmethod
    def get_home_context(student, apage, epage):
        events = EventInterest.objects.filter(student=student, active=True)
        apps = Application.objects.filter(student=student, status='active')
        old_apps = Application.objects.filter(student=student, status='hold', post__status='open')
        resumes = Resume.objects.filter(student=student, is_complete=True)
        apages = Pagination.get_pages(apps, apage, 15)
        epages = Pagination.get_pages(events, epage, 15)
        context = {
            'nav_student': student,
            'apps': apps,
            'old_apps': old_apps,
            'events': events,
            'resumes': resumes,
            'apages': apages,
            'apage': apage + 1,
            'epages': epages,
            'epage': epage + 1,
        }
        return context









