from django.shortcuts import render, Http404, redirect

from student.util_student import StudentContainer
from company.util_company import CompanyContainer


def student_index(request):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        return render(request, 'manual/student/index.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def student_home(request):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        return render(request, 'manual/student/home.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def student_posts(request):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        return render(request, 'manual/student/posts.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def student_events(request):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        return render(request, 'manual/student/events.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def student_resume(request):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        return render(request, 'manual/student/resume.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def student_profile(request):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        return render(request, 'manual/student/profile.html', {'nav_student': student.get_student(), 'tab': 'manual'})
    raise Http404


def company_index(request):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
        return render(request, 'manual/company/index.html', {'company': company.get_company(), 'tab': 'manual'})
    raise Http404


def company_home(request):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        return render(request, 'manual/company/home.html', {'company': company.get_company(), 'tab': 'manual'})
    raise Http404


def company_posts(request):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        return render(request, 'manual/company/posts.html', {'company': company.get_company(), 'tab': 'manual'})
    raise Http404


def company_events(request):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        return render(request, 'manual/company/events.html', {'company': company.get_company(), 'tab': 'manual'})
    raise Http404


def company_profile(request):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        return render(request, 'manual/company/profile.html', {'company': company.get_company(), 'tab': 'manual'})
    raise Http404











