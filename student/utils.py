from event.models import SavedEvent
from post.models import Application
from resume.models import Resume
from home.utils import Pagination


class StudentUtil:

    @staticmethod
    def get_home_context(student, apage, epage):
        events = SavedEvent.objects.filter(student=student, active=True)
        apps = []
        rq_apps = Application.objects.filter(student=student, status='active', cover_requested=True)
        apps.extend(rq_apps)
        rs_apps = Application.objects.filter(student=student, status='active', cover_submitted=True)
        apps.extend(rs_apps)
        r_apps = Application.objects.filter(student=student, status='active', cover_requested=False)
        apps.extend(r_apps)
        old_apps = Application.objects.filter(student=student, status='hold', post__status='open')
        resumes = Resume.objects.filter(student=student, is_complete=True)
        apages = Pagination.get_pages(apps, apage, 10)
        epages = Pagination.get_pages(events, epage, 10)
        context = {
            'nav_student': student,
            'apps': Pagination.get_page_items(apps, apage, 10),
            'old_apps': old_apps,
            'events': Pagination.get_page_items(events, epage, 10),
            'resumes': resumes,
            'apages': apages,
            'apage': apage + 1,
            'epages': epages,
            'epage': epage + 1,
        }
        return context









