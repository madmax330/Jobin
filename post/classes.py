

class ExtendedPost:

    def __init__(self, post, company, applied):
        self.id = post.id
        self.name = company.name
        self.address = company.address + ', ' + company.city + ', ' + company.state + ', ' + company.zipcode
        self.website = company.website
        self.logo = company.logo
        self.title = post.title
        self.start_date = post.start_date
        self.end_date = post.end_date
        self.deadline = post.deadline
        self.wage = post.wage
        self.wage_interval = post.wage_interval
        self.openings = post.openings
        self.requirements = post.requirements
        self.description = post.description
        self.applied = applied


class HomePagePost:

    def __init__(self, post, count):
        self.id = post.id
        self.title = post.title
        self.deadline = post.deadline
        self.start_date = post.start_date
        self.openings = post.openings
        self.notified = post.notified
        self.new_apps = post.new_apps
        self.app_count = count


class ExtendedApplication:

    def __init__(self, app, stu, resume):
        self.id = app.id
        self.name = stu.name
        self.email = stu.email
        self.phone = stu.phone
        self.address = stu.address + ' ' + stu.city + ' ' + stu.state + ' ' + stu.zipcode
        self.school = stu.school
        self.program = stu.program
        self.major = stu.major
        self.resume = resume
        self.gpa = app.resume.gpa
        self.post = app.post
        self.cover = app.cover
        self.cover_requested = app.cover_requested
        self.cover_submitted = app.cover_submitted
        self.cover_opened = app.cover_opened
        self.date_applied = app.date
        self.app_opened = app.opened
        self.resume_notified = app.resume_notified
        self.saved = app.saved
