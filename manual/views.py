from django.shortcuts import render, Http404
from student.models import Student
from company.models import Company


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
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/posts.html', {'nav_student': student})
    raise Http404


def student_events(request):
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/events.html', {'nav_student': student})
    raise Http404


def student_resume(request):
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/resume.html', {'nav_student': student})
    raise Http404


def student_profile(request):
    if request.method == 'GET':
        student = Student.objects.get(user=request.user)
        return render(request, 'manual/student/profile.html', {'nav_student': student})
    raise Http404


def company_index(request):
    if request.method == 'GET':
        company = Company.objects.get(user=request.user)
        return render(request, 'manual/company/index.html', {'company': company})
    raise Http404


def company_home(request):
    if request.method == 'GET':
        company = Company.objects.get(user=request.user)
        return render(request, 'manual/company/home.html', {'company': company})
    raise Http404


def company_posts(request):
    if request.method == 'GET':
        company = Company.objects.get(user=request.user)
        return render(request, 'manual/company/posts.html', {'company': company})
    raise Http404


def company_events(request):
    if request.method == 'GET':
        company = Company.objects.get(user=request.user)
        return render(request, 'manual/company/events.html', {'company': company})
    raise Http404


def company_profile(request):
    if request.method == 'GET':
        company = Company.objects.get(user=request.user)
        return render(request, 'manual/company/profile.html', {'company': company})
    raise Http404











