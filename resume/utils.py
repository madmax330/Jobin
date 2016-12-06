from .models import *
import datetime


class ResumeUtil:

    @staticmethod
    def update_resume(r):
        r.last_updated = datetime.datetime.now()
        r.save()

    @staticmethod
    def make_active(s, r):
        xx = Resume.objects.filter(student=s)
        for x in xx:
            if not x.pk == r.pk:
                x.is_active = False
                x.save()
        r.is_active = True
        r.save()

    @staticmethod
    def create_language_link(i, r):
        x = LanguageLink()
        x.language = i
        x.resume = r
        x.save()

    @staticmethod
    def create_school_link(i, r):
        x = SchoolLink()
        x.school = i
        x.resume = r
        x.save()

    @staticmethod
    def create_experience_link(i, r):
        x = ExperienceLink()
        x.experience = i
        x.resume = r
        x.start = i.start
        x.save()

    @staticmethod
    def create_award_link(i, r):
        x = AwardLink()
        x.award = i
        x.resume = r
        x.save()

    @staticmethod
    def create_skill_link(i, r):
        x = SkillLink()
        x.skill = i
        x.resume = r
        x.save()

    @staticmethod
    def get_other_language(r):
        l = Language.objects.filter(student=r.student)
        items = []
        for x in l:
            if LanguageLink.objects.filter(resume=r, language=x).count() == 0:
                items.append(x)
        return items

    @staticmethod
    def get_other_experience(r):
        l = Experience.objects.filter(student=r.student)
        items = []
        for x in l:
            if ExperienceLink.objects.filter(resume=r, experience=x).count() == 0:
                items.append(x)
        return items

    @staticmethod
    def get_other_award(r):
        l = Award.objects.filter(student=r.student)
        items = []
        for x in l:
            if AwardLink.objects.filter(resume=r, award=x).count() == 0:
                items.append(x)
        return items

    @staticmethod
    def get_other_school(r):
        l = School.objects.filter(student=r.student)
        items = []
        for x in l:
            if SchoolLink.objects.filter(resume=r, school=x).count() == 0:
                items.append(x)
        return items

    @staticmethod
    def get_other_skill(r):
        l = Skill.objects.filter(student=r.student)
        items = []
        for x in l:
            if SkillLink.objects.filter(resume=r, skill=x).count() == 0:
                items.append(x)
        return items

    @staticmethod
    def get_languages(r):
        l = LanguageLink.objects.filter(resume=r)
        items = []
        for x in l:
            items.append(x.language)
        return items

    @staticmethod
    def get_experience(r):
        l = ExperienceLink.objects.filter(resume=r).order_by('-start')
        items = []
        for x in l:
            items.append(x.experience)
        return items

    @staticmethod
    def get_awards(r):
        l = AwardLink.objects.filter(resume=r)
        items = []
        for x in l:
            items.append(x.award)
        return items

    @staticmethod
    def get_schools(r):
        l = SchoolLink.objects.filter(resume=r)
        items = []
        for x in l:
            items.append(x.school)
        return items

    @staticmethod
    def get_skills(r):
        l = SkillLink.objects.filter(resume=r)
        items = []
        for x in l:
            items.append(x.skill)
        return items





