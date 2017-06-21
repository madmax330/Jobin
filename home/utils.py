from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.exceptions import ObjectDoesNotExist

from .models import Message, Notification
import datetime


class Pagination(Paginator):

    def get_page(self, page):
        try:
            return self.page(page)
        except PageNotAnInteger:
            return self.page(1)
        except EmptyPage:
            return self.page(self.num_pages)


class MessageCenter:

    @staticmethod
    def new_message(t, u, code, message):
        m = Message()
        m.code = code
        m.message = message
        if t == 'student':
            m.student = u
        elif t == 'company':
            m.company = u
        m.save()

    @staticmethod
    def get_messages(t, u):
        if t == 'student':
            return Message.objects.filter(student=u)
        elif t == 'company':
            return Message.objects.filter(company=u)

    @staticmethod
    def clear_msgs(msgs):
        for x in msgs:
            x.delete()

    @staticmethod
    def new_notification(t, u, code, message):
        n = Notification()
        n.code = code
        n.message = message
        if t == 'student':
            n.student = u
        elif t == 'company':
            n.company = u
        n.save()

    @staticmethod
    def get_notifications(t, u):
        if t == 'student':
            return Notification.objects.filter(student=u, opened=False)
        if t == 'company':
            return Notification.objects.filter(company=u, opened=False)

    @staticmethod
    def get_all_notifications(t, u):
        if t == 'student':
            return Notification.objects.filter(student=u).order_by('-id')
        if t == 'company':
            return Notification.objects.filter(company=u).order_by('-id')

    @staticmethod
    def close_notification(pk):
        try:
            Notification.objects.get(pk=pk).delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def close_all_notifications(t, u):
        notifications = []
        if t == 'company':
            notifications = list(Notification.objects.filter(company=u, opened=False))
        if t == 'student':
            notifications = list(Notification.objects.filter(student=u, opened=False))
        if notifications:
            for x in notifications:
                x.opened = True
                x.save()
        return True

    #
    #   COMPANY APP MESSAGES
    #
    @staticmethod
    def company_created(company):
        msg = 'Your profile was successfully created. Welcome to Jobin!'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def company_updated(company):
        msg = 'Your profile was successfully updated.'
        MessageCenter.new_message('company', company, 'info', msg)

    #
    #   STUDENT APP MESSAGES
    #
    @staticmethod
    def student_created(student):
        msg = 'Your profile was successfully created. Welcome to Jobin!'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def student_updated(student):
        msg = 'Your profile was successfully updated.'
        MessageCenter.new_message('student', student, 'info', msg)

    #
    #   EVENT APP MESSAGES
    #
    @staticmethod
    def event_created(company, title):
        msg = 'Event ' + title + ' was created successfully.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def event_updated(company, title):
        msg = 'Event ' + title + ' was successfully updated.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def saved_event_notice(student, title):
        msg = 'Event: ' + title + ' saved, you can view this event in your "Saved Events"' \
              ' in the Home page.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def event_reactivate_info_message(company):
        msg = 'Please update the event information and save it to reactivate the event.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def event_reactivated(company, title):
        msg = 'Event ' + title + ' successfully re-opened, students will now be able to view it in their ' \
                'upcoming events'
        MessageCenter.new_message('company', company, 'info', msg)

    #
    #   RESUME APP MESSAGES
    #
    @staticmethod
    def resume_object_created(student, obj, title):
        msg = obj + ' ' + title + ' was created successfully.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_walkthrough_completion_message(student):
        msg = 'Your resume was successfully created and is ready to be used in an application.'
        msg += 'You can upload a file resume as well by going to edit resume.'
        msg += 'Fill in the rest of your resume information (Schools, Languages, Skills, Awards and Work' \
               ' Experience) using the manage button.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_object_updated(student, obj, title):
        msg = obj + ' ' + title + ' was successfully updated.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_object_deleted(student, obj, title):
        msg = obj
        if title:
            msg += ' ' + title + ' was deleted successfully.'
        else:
            msg += ' was deleted successfully.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_copied(student, title):
        msg = 'Your new resume was successfully created based on ' + title + '. You can now taylor it to your needs.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_items_auto_copied(student):
        msg = 'Since this is not your first resume, your School and Language items were imported automatically.'
        MessageCenter.new_message('student', student, 'warning', msg)

    @staticmethod
    def resume_activated(student, title):
        msg = 'Resume ' + title + ' set to active resume.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_app_resume_changed(student, app, resume):
        msg = 'Resume for ' + app + ' has been changed to ' + resume + '.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def resume_app_resume_already_on_file(student, resume):
        msg = resume + ' is already the resume on file for this application.'
        MessageCenter.new_message('student', student, 'warning', msg)

    @staticmethod
    def resume_error_creating_record(student):
        msg = 'Error creating your record, please try again.'
        MessageCenter.new_message('student', student, 'danger', msg)

    @staticmethod
    def resume_no_school(student):
        msg = "You must add at least one school entry before continuing."
        MessageCenter.new_message('student', student, 'danger', msg)

    @staticmethod
    def resume_no_language(student):
        msg = "You must add at least one language entry before continuing."
        MessageCenter.new_message('student', student, 'danger', msg)

    @staticmethod
    def resume_used_in_active_applications_error(student):
        msg = """This resume is used in active applications.
                Make sure it is not used in any active applications before deleting it."""
        MessageCenter.new_message('student', student, 'warning', msg)

    #
    #   POST APP MESSAGES
    #
    @staticmethod
    def post_created(company, title):
        msg = 'Post ' + title + ' created successfully.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def post_updated(company, title):
        msg = 'Post ' + title + ' updated successfully.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def post_closed(company, title):
        msg = 'Post ' + title + ' closed successfully'
        MessageCenter.new_message('company', company, 'warning', msg)

    @staticmethod
    def post_closed_notification(company, title):
        msg = 'Post ' + title + ' closed on ' + str(datetime.datetime.now().date()) + '.'
        MessageCenter.new_notification('company', company, 0, msg)

    @staticmethod
    def post_closed_student_notification(student, title):
        msg = 'The position ' + title + ' has been closed.'
        MessageCenter.new_notification('student', student, 100, msg)

    @staticmethod
    def new_applicants_message(company, posts):
        msg = 'There are new applications for the following posts: '
        for x in posts:
            msg += x
            msg += ', '
        MessageCenter.new_message('company', company, 'info', msg[:-2])

    @staticmethod
    def no_applicants_left(company):
        msg = 'There are no more active applicants for this post.'
        MessageCenter.new_message('company', company, 'warning', msg)

    @staticmethod
    def incoming_deadline(company, title):
        msg = 'The post ' + title + "'s deadline is coming up soon. After the deadline, the post will not" \
                " be visible to students anymore, therefore you will not get any new application, but you will " \
                "continue to be able to manage applicants."
        MessageCenter.new_message('company', company, 'warning', msg)

    @staticmethod
    def applicant_removed(company, student):
        msg = 'The applicant ' + student + ' was successfully removed.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def application_discontinued(student, title):
        msg = 'Your application for the ' + title + ' opportunity was discontinued.'
        MessageCenter.new_notification('student', student, 100, msg)

    @staticmethod
    def apply_message(student, title):
        msg = 'You successfully applied for the post: ' + title
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def already_applied(student, title):
        msg = 'You have already applied for the post ' + title
        MessageCenter.new_message('student', student, 'warning', msg)

    @staticmethod
    def apply_no_resume(student):
        msg = 'You need to have at least one active resume to apply for posts. Activate one and try again.'
        MessageCenter.new_message('student', student, 'warning', msg)

    @staticmethod
    def cover_letter_request(company, student):
        msg = 'Cover letter request was successfully sent to ' + student
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def cover_letter_notification(student, company, title):
        msg = company + ' requests a cover letter for your application to the ' \
              + title + ' position. Go to the application details to submit your cover letter'
        MessageCenter.new_notification('student', student, 100, msg)

    @staticmethod
    def cover_letter_already_requested(company):
        msg = 'A cover letter was already sent to this applicant; you will be' \
              ' notified when a cover letter is received'
        MessageCenter.new_message('company', company, 'warning', msg)

    @staticmethod
    def cover_letter_submitted(student, title):
        msg = 'Cover letter successfully submitted for post: ' + title
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def cover_letter_received(company, title, student):
        msg = 'Cover letter submitted by applicant (' + student + ') for post ' + title
        MessageCenter.new_notification('company', company, 100, msg)

    @staticmethod
    def cover_letter_blank(student):
        msg = 'Cover letter cannot be left blank.'
        MessageCenter.new_message('student', student, 'danger', msg)

    @staticmethod
    def post_reactivated(company, title):
        msg = 'Post ' + title + ' successfully re-opened, you will be able to view all ' \
              'the applicants that you kept from last time,' \
              ' you will also be able to view their old cover letters, or request new ones.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def post_reactivated_notification(student, title, company):
        msg = 'The post ' + title + ' by' + str(company) + ' has been re-opened.' \
              ' Since your application was not discarded your candidacy is automatically renewed, but ' \
              'you can remove it in your home screen.'
        MessageCenter.new_notification('student', student, 100, msg)

    @staticmethod
    def application_withdrew(student, title):
        msg = 'Application for post ' + title + ' successfully closed.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def application_continued(student, title):
        msg = 'Application for post ' + title + ' successfully continued.'
        MessageCenter.new_message('student', student, 'info', msg)

    @staticmethod
    def post_reactivate_info_message(company):
        msg = 'Please update the post information and save it to reactivate the post.'
        MessageCenter.new_message('company', company, 'info', msg)

    @staticmethod
    def make_filter_message(sf, mf, gf, post):
        msg = 'Results for filter; Schools: '
        if sf:
            msg += sf
        else:
            msg += 'No filter'
        if mf:
            msg += '; Majors: ' + mf
        else:
            msg += '; Majors: No filter'
        if gf:
            msg += '; GPA: ' + gf
        else:
            msg += '; GPA: No filter'
        MessageCenter.new_message('company', post.company, 'info', msg)



