from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from home.base_classes import BaseContainer

from .models import Application
from .forms import NewApplicationForm, AddCoverLetterForm, ChangeResumeForm
from .classes import ExtendedPost

from .models import Post
from .forms import NewPostForm, EditPostForm

import datetime


class StudentPostContainer(BaseContainer):
    TODAY = datetime.datetime.now().date()

    def __init__(self, student):
        super(StudentPostContainer, self).__init__()
        self._container_name = 'Student Post Container'
        self.__student = student
        self.__post = None
        self.__application = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_application(self, post, resume):
        info = {
            'student': self.__student.id,
            'post': post.id,
            'resume': resume.id,
            'date': datetime.datetime.now().date(),
            'post_title': post.title,
            'student_name': self.__student.name,
            'status': 'active',
        }
        self._form = NewApplicationForm(info)
        if self._form.is_valid():
            self.__application = self._form.save()
            if not post.new_apps:
                post.new_apps = True
                post.save()
            return True
        else:
            self.add_form_errors()
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    def get_post(self, pk=None):
        if pk:
            try:
                self.__post = Post.objects.get(pk=pk)
                return self.__post
            except ObjectDoesNotExist:
                self.add_error('Post not found.')
                return False
        else:
            return self.__post

    def get_posts(self, cat, pk, filters):
        ops = [Q(programs='All Programs'), Q(programs=self.__student.program)]
        ads = [Q(status='open'), Q(deadline__gte=self.TODAY)]
        fls = []
        if filters:
            if filters['location']:
                fls.append(Q(location__icontains=filters['location']))
            if filters['keyword']:
                fls.append(Q(title__icontains=filters['keyword']))
        if cat == 'startup':
            ads.append(Q(is_startup_post=True))
        else:
            ads.append(Q(type=cat))
        op = Q()
        for x in ops:
            op |= x
        ad = Q()
        for x in ads:
            ad &= x
        if filters:
            f = Q()
            for x in fls:
                f |= x
            op &= f
        op &= ad
        posts = Post.objects.filter(op)
        if posts.count() > 0:
            l = []
            temp = []
            flag = False
            for x in posts:
                if int(x.id) == int(pk) > 0:
                    flag = True
                self.__post = x
                y = ExtendedPost(x, x.company, self.already_applied())
                if flag:
                    l.append(y)
                else:
                    temp.append(y)
            l.extend(temp)
            return l
        else:
            self.add_error('No posts found.')
            return []

    def get_post_count(self, category, filters=None):
        ops = [Q(programs='All Programs'), Q(programs=self.__student.program)]
        ads = [
            (Q(is_startup_post=True) if category == 'startup' else Q(type=category)),
            Q(deadline__gte=self.TODAY),
            Q(status='open')
        ]
        fls = []
        if filters:
            if filters['location']:
                fls.append(Q(location__icontains=filters['location']))
            if filters['keyword']:
                fls.append(Q(title__icontains=filters['keyword']))
        op = Q()
        for x in ops:
            op |= x
        ad = Q()
        for x in ads:
            ad &= x
        if filters:
            f = Q()
            for x in fls:
                f |= x
            op &= f
        op &= ad
        return Post.objects.filter(op).count()

    def get_newest_posts(self):
        ops = [Q(programs='All Programs'), Q(programs=self.__student.program)]
        ads = [Q(deadline__gte=self.TODAY), Q(status='open')]
        op = Q()
        for x in ops:
            op |= x
        ad = Q()
        for x in ads:
            ad &= x
        op &= ad
        posts = Post.objects.filter(op).order_by('-id')[:15]
        if posts.count() > 0:
            return list(posts)
        return []

    def get_application(self, pk):
        try:
            self.__application = Application.objects.get(pk=pk)
            return self.__application
        except ObjectDoesNotExist:
            self.add_error('Application not found.')
            return None

    def get_applications(self):
        first_apps = Application.objects.filter(student=self.__student, status='active', cover_requested=True)
        last_apps = Application.objects.filter(
            student=self.__student,
            status='active',
            cover_requested=False
        ).order_by('-id')
        if first_apps.count() > 0 or last_apps.count() > 0:
            l = []
            l.extend(list(first_apps))
            l.extend(list(last_apps))
            return l
        self.add_error('No applications found.')
        return []

    def get_old_applications(self):
        apps = Application.objects.filter(student=self.__student, status='hold', post__status='open')
        if apps.count() > 0:
            return list(apps)
        self.add_error('No old applications found.')
        return []

    def get_all_applications(self):
        apps = Application.objects.filter(student=self.__student).order_by('-id')
        if apps.count() > 0:
            return list(apps)
        self.add_error('No applications found.')
        return []

    def already_applied(self):
        return Application.objects.filter(post=self.__post, student=self.__student).count() > 0

    def in_apps(self, r):
        return Application.objects.filter(student=self.__student, resume=r).count() > 0

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def increment_view_count(self):
        self.__post.views = self.__post.views + 1
        self.__post.save()
        return True

    def submit_cover_letter(self, letter):
        info = {
            'cover': letter,
            'cover_submitted': True,
        }
        self._form = AddCoverLetterForm(info, instance=self.__application)
        if self._form.is_valid():
            self.__application = self._form.save()
            post = self.__application.post
            if not post.notified:
                post.notified = True
                post.save()
            m = 'Cover letter for "' + self.__application.post_title + '" successfully submitted.'
            if self.new_message(True, self.__student, m, 0):
                m = 'Cover letter received from ' + self.__student.name + ' for post '
                m += self.__application.post.title + '.'
                if self.new_notification(False, self.__application.post.company, m, 100):
                    return True
            return False
        else:
            self.add_form_errors()
            return False

    def change_application_resume(self, r):
        if self.__application.resume == r:
            self.add_error(r.name + ' is already the resume for this application.' + self.__application.post_title)
            return False
        self._form = ChangeResumeForm({'resume': r.id}, instance=self.__application)
        if self._form.is_valid():
            self._form.save()
            self.__application.resume_notified = True
            self.__application.save()
            return True
        else:
            self.add_form_errors()
            return False

    def withdraw_application(self):
        self.__application.status = 'closed'
        self.__application.save()
        return True

    def activate_application(self):
        self.__application.status = 'active'
        self.__application.save()
        return True


class CompanyPostContainer(BaseContainer):

    def __init__(self, company):
        super(CompanyPostContainer, self).__init__()
        self._container_name = 'Company Post Container'
        self.__company = company
        self.__post = None
        self.__application = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_post(self, post_info):
        info = {
            'company': self.__company.id,
            'is_startup_post': self.__company.is_startup,
            'location': self.__company.city + ' ' + self.__company.state + ' ' + self.__company.country,
            'title': post_info['title'],
            'wage': post_info['wage'],
            'wage_interval': post_info['wage_interval'],
            'openings': post_info['openings'],
            'start_date': post_info['start_date'],
            'end_date': post_info['end_date'],
            'deadline': post_info['deadline'],
            'description': post_info['description'],
            'requirements': post_info['requirements'],
            'programs': post_info['programs'],
            'type': post_info['type'],
            'cover_instructions': post_info['cover_instructions'],
        }
        self._form = NewPostForm(info)
        if self._form.is_valid():
            self.__post = self._form.save()
            m = 'New Post: ' + self.__post.title + ' successfully created.'
            if self.new_message(False, self.__company, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def edit_post(self, post_info):
        info = {
            'title': post_info['title'],
            'wage': post_info['wage'],
            'wage_interval': post_info['wage_interval'],
            'openings': post_info['openings'],
            'start_date': post_info['start_date'],
            'end_date': post_info['end_date'],
            'deadline': post_info['deadline'],
            'description': post_info['description'],
            'requirements': post_info['requirements'],
            'programs': post_info['programs'],
            'type': post_info['type'],
            'cover_instructions': post_info['cover_instructions'],
        }
        self._form = EditPostForm(info, instance=self.__post)
        if self._form.is_valid():
            self.__post = self._form.save()
            m = 'Post: ' + self.__post.title + ' edited successfully.'
            if self.new_message(False, self.__company, m, 0):
                return True
            else:
                return False
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def close_post(self):
        self.__post.status = 'closed'
        self.__post.notified = False
        self.__post.save()
        m = 'Post "' + self.__post.title + '" closed on ' + str(datetime.datetime.now().date()) + '.'
        if self.new_message(False, self.__company, m, 2) and self.new_notification(False, self.__company, m, 100):
            apps = self.get_applications()
            if apps:
                for x in apps:
                    if not self.new_notification(True, x.student, m, 100):
                        x.status = 'hold'
                        x.save()
                        return False
            return True
        else:
            return False

    def recover_post(self, post_info):
        info = {
            'title': post_info['title'],
            'wage': post_info['wage'],
            'wage_interval': post_info['wage_interval'],
            'openings': post_info['openings'],
            'start_date': post_info['start_date'],
            'end_date': post_info['end_date'],
            'deadline': post_info['deadline'],
            'description': post_info['description'],
            'requirements': post_info['requirements'],
            'programs': post_info['programs'],
            'type': post_info['type'],
            'cover_instructions': post_info['cover_instructions'],
        }
        self._form = EditPostForm(info, instance=self.__post)
        if self._form.is_valid():
            self.__post = self._form.save(commit=False)
            self.__post.status = 'open'
            self.__post.save()
            m = 'Post: ' + self.__post.title + ' recovered successfully.'
            if self.new_message(False, self.__company, m, 0):
                apps = self.get_held_applications()
                if apps:
                    for x in apps:
                        m = 'The post "' + self.__post.title + '" that you had previously applied to was re-opened.'
                        if not self.new_notification(True, x.student, m, 100):
                            return False
                        x.cover_requested = False
                        x.save()
                return True
            else:
                return False
        else:
            self.add_form_errors()
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    @staticmethod
    def fetch_post(pk):
        try:
            return Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get_post(self, pk=None):
        if pk:
            try:
                self.__post = Post.objects.get(pk=pk)
                if self.__post.company == self.__company:
                    return self.__post
                else:
                    self.add_error('Post not found.')
                    return None
            except ObjectDoesNotExist:
                self.add_error('Post not found.')
                return None
        else:
            return self.__post

    def get_posts(self):
        posts = Post.objects.filter(company=self.__company, status='open')
        if posts.count() > 0:
            return list(posts)
        else:
            self.add_error('No posts found.')
            return []

    def get_expired_posts(self):
        posts = Post.objects.filter(company=self.__company, status='closed')
        if posts.count() > 0:
            return list(posts)
        else:
            self.add_error('No expired posts found.')
            return []

    def get_application(self, pk=None):
        if pk:
            try:
                self.__application = Application.objects.get(pk=pk)
                if self.__application.post.company == self.__company:
                    return self.__application
                else:
                    self.add_error('Application not found.')
                    return False
            except ObjectDoesNotExist:
                self.add_error('Application not found.')
                return False
        else:
            return self.__application

    def get_applications(self, ak='0', post=None, filters=None):
        if post:
            self.__post = post
        if filters:
            all_apps = Application.objects.filter(Q(status='active') | Q(status='hold'), post=self.__post)
            apps = self.__filter_applications(all_apps, filters)
            if int(ak) > 0:
                l = []
                temp = []
                flag = False
                for x in apps:
                    if int(x.id) == int(ak):
                        flag = True
                    if flag:
                        l.append(x)
                    else:
                        temp.append(x)
                l.extend(temp)
                apps = l
            if filters['keep']:
                return apps
            else:
                l = [x for x in all_apps if x not in apps]
                for x in l:
                    self.close_application(x)
                if len(l) > 0:
                    m = 'The applications (' + str(len(l)) + ') outside the filter were closed successfully.'
                    if self.new_message(False, self.__company, m, 2):
                        return apps
                    else:
                        return apps
        else:
            apps = []
            all_apps = Application.objects.filter(Q(status='active') | Q(status='hold'), post=self.__post)
            covered = all_apps.filter(cover_submitted=True)
            rest = all_apps.filter(cover_submitted=False)
            if covered.count() > 0:
                apps.extend(list(covered))
            if rest.count() > 0:
                apps.extend(list(rest))
            if len(apps) > 0:
                return apps
            else:
                self.add_error('No applications found.')
                return []

    def application_count(self, post=None):
        if post:
            self.__post = post
        return Application.objects.filter(Q(status='active') | Q(status='hold'), post=self.__post).count()

    def get_held_applications(self, post=None):
        if post:
            self.__post = post
        apps = Application.objects.filter(post=self.__post, status='hold')
        if apps.count() > 0:
            return list(apps)
        else:
            self.add_error('No held applications found.')
            return []

    def __filter_applications(self, all_apps, filters):

        ops = []
        if filters['schools']:
            ops.append(Q(student__school__in=filters['schools'].split(',')))
        if filters['majors']:
            ops.append(Q(student__major__in=filters['majors'].split(',')))
        if filters['gpa']:
            ops.append(Q(resume__gpa__gte=filters['gpa']))
        if filters['saved']:
            ops.append(Q(saved=True))

        if len(ops) > 0:
            op = Q()
            for x in ops:
                op &= x
            apps = all_apps.filter(op)
            if apps.count() > 0:
                return list(apps)
            else:
                self.add_error('No applications found.')
                return []
        else:
            return self.get_applications()

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def save_application(self):
        if self.__application.saved:
            self.add_error('Application already saved.')
            return False
        self.__application.saved = True
        self.__application.save()
        return True

    def remove_application_save(self):
        if self.__application.saved:
            self.__application.saved = False
            self.__application.save()
            return True
        self.add_error('Application not saved.')
        return False

    def request_cover(self):
        if self.__application.cover_requested:
            self.add_error('Cover letter request already sent.')
            return False
        self.__application.cover_requested = True
        self.__application.save()
        m = 'A cover letter was requested for your application to the post: "' + self.__application.post.title + '".'
        if self.new_notification(True, self.__application.student, m, 100):
            return True
        return False

    def close_application(self, app=None):
        if app:
            self.__application = app
        self.__application.status = 'closed'
        self.__application.save()
        m = 'Your application for the post "' + self.__application.post.title + '" was closed.'
        if self.new_notification(True, self.__application.student, m, 100):
            return True
        return False

    def app_opened(self, app=None):
        if app:
            self.__application = app
        edited = False
        if not self.__application.opened:
            self.__application.opened = True
            edited = True
        if self.__application.cover_submitted and not self.__application.cover_opened:
            self.__application.cover_opened = True
            edited = True
        if edited:
            self.__application.save()

    def no_new_apps(self, post=None):
        if post:
            self.__post = post
        if self.__post.new_apps:
            self.__post.new_apps = False
            self.__post.save()

