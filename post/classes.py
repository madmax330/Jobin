from post.models import Application


class CustomPost:

    def __init__(self, post, company, student):
        self.pk = post.pk
        self.name = company.name
        self.address = company.address + ', ' + company.city + ', ' + company.state + ', ' + company.zipcode
        self.website = company.website
        self.logo = company.logo
        self.title = post.title
        self.start_date = post.start_date
        self.end_date = post.end_date
        self.deadline = post.deadline
        self.wage = post.wage
        self.openings = post.openings
        self.requirements = post.requirements
        self.description = post.description
        if Application.objects.filter(post=post, student=student).count() > 0:
            self.applied = True
        else:
            self.applied = False


class Applicant:

    def __init__(self, app, stu):
        self.pk = app.pk
        self.fname = stu.firstname
        self.lname = stu.lastname
        self.email = stu.email
        self.phone = stu.phone
        self.address = stu.address + ' ' + stu.city + ' ' + stu.state + ' ' + stu.zipcode
        self.school = stu.school
        self.program = stu.program
        self.major = stu.major
        self.resume = app.resume
        self.gpa = app.resume.gpa
        self.post = app.post
        self.cover = app.cover
        self.cover_requested = app.cover_requested
        self.cover_submitted = app.cover_submitted
        self.cover_opened = app.cover_opened
        self.date_applied = app.date
        self.app_opened = app.opened
        self.resume_notified = app.resume_notified