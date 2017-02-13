import datetime
from random import randint, uniform
from django.contrib.auth.models import User
from django.db.models import Q
from home.models import *
from student.models import *
from company.models import *
from resume.models import *
from post.models import *
from event.models import *


class ContentGen:
    schools = JobinSchool.objects.all()
    countries = ['Canada', 'United States']
    states = JobinTerritory.objects.all()
    majors = JobinMajor.objects.all()
    programs = JobinProgram.objects.all()
    job_types = ['intership', 'parttime', 'volunteer', 'newgrad']

    pw = 'pass'

    @staticmethod
    def create_company(u, i):
        c = Company()
        c.user = u
        c.name = 'Company' + str(i)
        c.email = u.email
        c.address = '111 company address'
        c.city = 'Company City'
        c.state = ContentGen.states[randint(0, ContentGen.states.count() - 1)].name
        c.country = ContentGen.countries[randint(0, 1)]
        c.zipcode = '33801'
        c.phone = '800 111 1111'
        c.website = 'www.company.com'
        c.is_startup = bool(randint(0, 1))
        c.save()
        ContentGen.create_company_posts(c)
        ContentGen.create_company_events(c)

    @staticmethod
    def create_company_posts(company):
        start = (datetime.datetime.now() + datetime.timedelta(days=15)).date()
        end = (datetime.datetime.now() + datetime.timedelta(days=30)).date()
        dead = (datetime.datetime.now() + datetime.timedelta(days=10)).date()

        for i in range(0, 5):
            p = Post()
            p.company = company
            p.title = company.name + 'Post' + str(i)
            p.wage = i
            p.openings = i
            p.start_date = start
            p.end_date = end
            p.deadline = dead
            p.description = 'Integer consectetur id arcu eu euismod. In viverra odio ut nisi tempus,' \
                            ' non rhoncus magna commodo. Fusce nec leo vel mi consectetur cursus in vitae nibh.' \
                            ' In ac libero eros. Aenean elementum, diam nec dictum dapibus, nisl tellus tempor lacus,' \
                            ' efficitur pharetra ipsum sem vel odio. Fusce metus magna, posuere at pharetra in,' \
                            ' commodo in lacus. Etiam cursus risus est, ac vestibulum turpis sollicitudin eu.'
            p.requirements = p.description
            if bool(randint(0, 1)):
                p.programs = ContentGen.programs[randint(0, ContentGen.programs.count() - 1)]
            else:
                p.programs = ContentGen.programs.filter(name='All Programs').first()
            p.type = ContentGen.job_types[randint(0, len(ContentGen.job_types) - 1)]
            p.is_startup_post = company.is_startup
            p.save()

    @staticmethod
    def create_company_events(company):
        date = (datetime.datetime.now() + datetime.timedelta(days=30)).date()
        time = datetime.datetime.now().time()

        for i in range(0, 5):
            e = Event()
            e.company = company
            e.title = company.name + 'Event' + str(i)
            e.date = date
            e.time = time
            e.website = 'www.eventwebsite.com'
            e.address = ' 111 event address'
            e.city = 'Event City'
            e.state = ContentGen.states[0].name
            e.zipcode = '11 222'
            e.country = ContentGen.countries[0]
            e.description = 'Integer consectetur id arcu eu euismod. In viverra odio ut nisi tempus,' \
                            ' non rhoncus magna commodo. Fusce nec leo vel mi consectetur cursus in vitae nibh.' \
                            ' In ac libero eros. Aenean elementum, diam nec dictum dapibus, nisl tellus tempor lacus,' \
                            ' efficitur pharetra ipsum sem vel odio. Fusce metus magna, posuere at pharetra in,' \
                            ' commodo in lacus. Etiam cursus risus est, ac vestibulum turpis sollicitudin eu.'
            e.save()

    @staticmethod
    def create_student(u, i, sch):
        s = Student()
        s.user = u
        s.firstname = 'Student' + str(i)
        s.lastname = 'Last0' + str(i)
        s.dob = datetime.datetime.now().date()
        s.address = '111 student address'
        s.city = 'Student City'
        s.state = ContentGen.states[randint(0, ContentGen.states.count() - 1)].name
        s.country = ContentGen.countries[randint(0, 1)]
        s.zipcode = 'J1M1Z7'
        s.phone = '555 444 2222'
        s.email = u.email
        s.school = sch
        p = ContentGen.programs[randint(0, ContentGen.programs.count() - 1)]
        while p.name == 'All Programs':
            p = ContentGen.programs[randint(0, ContentGen.programs.count() - 1)]
        s.program = p.name
        majors = ContentGen.majors.filter(program=p)
        s.major = majors[randint(0, majors.count() - 1)].name
        s.save()
        ContentGen.create_student_resumes(s)

    @staticmethod
    def create_student_resumes(s):

        for i in range(0, 3):
            r = Resume()
            r.student = s
            r.gpa = float("{0:.2f}".format(uniform(2, 4)))
            if i == 0:
                r.is_active = True
            else:
                r.is_active = False
            r.is_complete = True
            r.name = 'Resume' + str(i)
            r.save()
            ContentGen.create_resume_schools(r, i)
            ContentGen.create_resume_languages(r, i)
            ContentGen.create_resume_experience(r, i)
            ContentGen.create_resume_awards(r, i)
            ContentGen.create_resume_skills(r, i)

    @staticmethod
    def create_resume_schools(r, i):
        start = (datetime.datetime.now() - datetime.timedelta(days=15)).date()
        end = (datetime.datetime.now() + datetime.timedelta(days=30)).date()

        sls = School.objects.filter(student=r.student)
        if sls.count() > 0:
            for x in sls:
                xx = SchoolLink()
                xx.school = x
                xx.resume = r
                xx.save()

        s = School()
        s.student = r.student
        s.name = 'School' + r.name + str(i)
        s.start = start
        s.end = end
        s.level = 'University'
        s.program = 'student Program'
        s.rkey = r.pk
        s.rname = r.name
        s.save()

        sl = SchoolLink()
        sl.school = s
        sl.resume = r
        sl.save()

    @staticmethod
    def create_resume_languages(r, i):

        langs = Language.objects.filter(student=r.student)
        if langs.count() > 0:
            for x in langs:
                xx = LanguageLink()
                xx.language = x
                xx.resume = r
                xx.save()

        l = Language()
        l.student = r.student
        l.name = 'Language' + r.name + str(i)
        l.level = 'native'
        l.rkey = r.pk
        l.rname = r.name
        l.save()

        ll = LanguageLink()
        ll.language = l
        ll.resume = r
        ll.save()

    @staticmethod
    def create_resume_experience(r, i):
        start = (datetime.datetime.now() - datetime.timedelta(days=15)).date()
        end = (datetime.datetime.now() + datetime.timedelta(days=30)).date()

        exp = Experience.objects.filter(student=r.student)
        if exp.count() > 0:
            for x in exp:
                xx = ExperienceLink()
                xx.experience = x
                xx.resume = r
                xx.start = x.start
                xx.save()

        e = Experience()
        e.student = r.student
        e.title = 'Experience' + r.name + str(i)
        e.start = start
        e.end = end
        e.description = 'Integer consectetur id arcu eu euismod. In viverra odio ut nisi tempus,' \
                        ' non rhoncus magna commodo. Fusce nec leo vel mi consectetur cursus in vitae nibh.' \
                        ' In ac libero eros. Aenean elementum, diam nec dictum dapibus, nisl tellus tempor lacus,' \
                        ' efficitur pharetra ipsum sem vel odio. Fusce metus magna, posuere at pharetra in,' \
                        ' commodo in lacus. Etiam cursus risus est, ac vestibulum turpis sollicitudin eu.'
        e.company = 'Company'
        e.experience_type = 'Experience Type'
        e.rkey = r.pk
        e.rname = r.name
        e.save()

        el = ExperienceLink()
        el.experience = e
        el.resume = r
        el.start = e.start
        el.save()

    @staticmethod
    def create_resume_awards(r, i):
        date = (datetime.datetime.now() - datetime.timedelta(days=15)).date()

        aws = Award.objects.filter(student=r.student)
        if aws.count() > 0:
            for x in aws:
                xx = AwardLink()
                xx.award = x
                xx.resume = r
                xx.save()

        a = Award()
        a.student = r.student
        a.title = 'Award' + r.name + str(i)
        a.date = date
        a.description = 'Integer consectetur id arcu eu euismod. In viverra odio ut nisi tempus,' \
                        ' non rhoncus magna commodo. Fusce nec leo vel mi consectetur cursus in vitae nibh.' \
                        ' In ac libero eros. Aenean elementum, diam nec dictum dapibus, nisl tellus tempor lacus,' \
                        ' efficitur pharetra ipsum sem vel odio. Fusce metus magna, posuere at pharetra in,' \
                        ' commodo in lacus. Etiam cursus risus est, ac vestibulum turpis sollicitudin eu.'
        a.award_type = 'Award Type'
        a.rkey = r.pk
        a.rname = r.name
        a.save()

        al = AwardLink()
        al.award = a
        al.resume = r
        al.save()

    @staticmethod
    def create_resume_skills(r, i):

        sks = Skill.objects.filter(student=r.student)
        if sks.count() > 0:
            for x in sks:
                xx = SkillLink()
                xx.skill = x
                xx.resume = r
                xx.save()

        s = Skill()
        s.student = r.student
        s.name = 'Skill' + r.name + str(i)
        s.level = 'Skill Level'
        s.rkey = r.pk
        s.rname = r.name
        s.save()

        sl = SkillLink()
        sl.skill = s
        sl.resume = r
        sl.save()

    @staticmethod
    def gen_test_content(val):

        # Create company users and companies and student users and students
        for i in range(0, val):
            # Companies
            cuname = 'user' + str(i) + '@gmail.com'
            cu = User.objects.create_user(username=cuname, email=cuname, password=ContentGen.pw)
            ContentGen.create_company(cu, i)

        for i in range(0, val):
            # Students
            sch = ContentGen.schools[randint(0, ContentGen.schools.count() - 1)]
            suname = 'student00' + str(i) + '@' + sch.email
            su = User.objects.create_user(username=suname, email=suname, password=ContentGen.pw)
            ContentGen.create_student(su, i, sch)

        ContentGen.create_event_interests()
        ContentGen.create_post_applications()

    @staticmethod
    def create_event_interests():
        students = Student.objects.all()
        events = Event.objects.all()
        for x in students:
            for i in range(0, 5):
                event = events[randint(0, events.count() - 1)]
                ei = SavedEvent()
                ei.student = x
                ei.event = event
                ei.date = event.date
                ei.event_name = event.title
                ei.save()

    @staticmethod
    def create_post_applications():
        students = Student.objects.filter(firstname__contains='Student')
        for x in students:
            resumes = Resume.objects.filter(student=x)
            posts = Post.objects.filter(Q(programs='All Programs') | Q(programs=x.program))
            for p in posts:
                a = Application()
                a.post = p
                a.student = x
                a.resume = resumes[randint(0, resumes.count() - 1)]
                a.date = datetime.datetime.now().date()
                a.status = 'active'
                a.post_title = p.title
                a.student_name = x.firstname + ' ' + x.lastname
                a.save()

    @staticmethod
    def clear_test_content():
        languages = Language.objects.all()
        schools = School.objects.all()
        experience = Experience.objects.all()
        skills = Skill.objects.all()
        awards = Award.objects.all()
        resumes = Resume.objects.all()
        students = Student.objects.all()

        apps = Application.objects.all()
        saved = SavedEvent.objects.all()
        events = Event.objects.all()
        posts = Post.objects.all()
        companies = Company.objects.all()

        for x in languages:
            if 'language' in x.name.lower():
                x.delete()
        for x in schools:
            if 'school' in x.name.lower():
                x.delete()
        for x in experience:
            if 'experience' in x.title.lower():
                x.delete()
        for x in skills:
            if 'skill' in x.name.lower():
                x.delete()
        for x in awards:
            if 'award' in x.title.lower():
                x.delete()

        for x in apps:
            if 'student' in x.student_name.lower():
                x.delete()
        for x in saved:
            if 'student' in x.student.firstname.lower():
                x.delete()

        for x in resumes:
            if 'resume' in x.name.lower()[0:6]:
                x.delete()
        for x in students:
            if 'student' in x.firstname.lower():
                x.delete()

        for x in events:
            if 'event' in x.title.lower():
                x.delete()
        for x in posts:
            if 'post' in x.title.lower():
                x.delete()
        for x in companies:
            if 'company' in x.name.lower():
                x.delete()

        users = User.objects.all()
        for x in users:
            if 'user' in x.email or 'student' in x.email:
                x.delete()
























