from django.shortcuts import render, Http404
from student.models import Student


def student_index(request):

    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/index.html', {'nav_student': student})
    raise Http404


def student_home(request):

    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/home.html', {'nav_student': student})
    raise Http404


def student_posts(request):
    return render(request, 'manual/student/index.html')


def student_events(request):
    return render(request, 'manual/student/index.html')


def student_resume(request):
    return render(request, 'manual/student/index.html')


def student_profile(request):
    return render(request, 'manual/student/index.html')


def company_index(request):
    pass


def company_home(request):
    pass


def company_posts(request):
    pass


def company_events(request):
    pass


def company_profile(request):
    pass











