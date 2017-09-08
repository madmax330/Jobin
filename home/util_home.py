from django.core.exceptions import ObjectDoesNotExist

from home.models import JobinSchool, JobinProgram, JobinMajor, JobinTerritory


class HomeUtil:
    COUNTRIES = ['Canada', 'United States']

    @staticmethod
    def get_countries():
        return HomeUtil.COUNTRIES

    @staticmethod
    def get_states():
        return JobinTerritory.objects.all()

    @staticmethod
    def get_program(name):
        try:
            return JobinProgram.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_programs():
        return JobinProgram.objects.all()

    @staticmethod
    def get_student_programs():
        return JobinProgram.objects.exclude(name='All Programs')

    @staticmethod
    def get_majors():
        return JobinMajor.objects.all()

    @staticmethod
    def get_program_majors(program):
        majors = JobinMajor.objects.filter(program=program)
        if majors.count() > 0:
            return list(majors)
        else:
            return []

    @staticmethod
    def get_schools():
        return list(JobinSchool.objects.all())

    @staticmethod
    def open_school(email):
        ext = email.split('@', 1)[1]
        return JobinSchool.objects.filter(email=ext.lower()).count() > 0


