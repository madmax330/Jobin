from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from django.db import transaction, IntegrityError
from home.utils import MessageCenter, Pagination

from home.util_request import RequestUtil
from student.util_student import StudentContainer


def resume_index(request):

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        student = StudentContainer(request.user)
        msgs = MessageCenter.get_messages('student', student.get_student())
        notes = MessageCenter.get_notifications('student', student.get_student())
        resumes = Pagination(student.get_resumes(), 20)
        context = {
            'student': student.get_student(),
            'resumes': resumes.get_page(page),
            'messages': msgs,
            'first': 'false' if resumes.count > 0 else 'true',
            'notifications': notes,
            'tab': 'resume',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'resume/index.html', context)

    raise Http404


def resume_detail(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        msgs = MessageCenter.get_messages('student', student.get_student())
        resume = student.get_display_resume(pk)
        if not resume:
            MessageCenter.new_message('student', student.get_student(), 'warning', str(student.get_errors()))
            return redirect('resume:index')
        context = {
            'student': student.get_student(),
            'resume': resume,
            'messages': msgs,
            'other_schools': student.get_other_schools(),
            'other_languages': student.get_other_languages(),
            'other_experience': student.get_other_experience(),
            'other_awards': student.get_other_awards(),
            'other_skills': student.get_other_skills(),
            'other_references': student.get_other_references(),
            'tab': 'resume',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'resume/details.html', context)

    raise Http404


def new_resume(request):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_resume_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_resume(i):
                        m = 'New resume created successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        r = student.get_resume()
                        if r.is_complete:
                            m = 'resume complete'
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                return HttpResponse(str(student.get_errors()), status=400)

        else:
            return HttpResponse(str(rq.get_errors()), status=400)

    raise Http404


def copy_resume(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.copy_resume(pk):
                    m = 'New resume successfully created.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:index')

    raise Http404


def edit_resume(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_resume_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_resume(pk, i):
                        m = 'Resume edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                MessageCenter.new_message('student', student.get_student(), 'danger', m)

        else:
            m = str(rq.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return HttpResponse('Invalid resume request.', status=400)

    raise Http404


def change_application_resume(request, pk, ak):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.change_application_resume(pk, ak):
                    m = 'Resume changed successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    return HttpResponse(m, status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)
            return HttpResponse(m, status=400)

    raise Http404


def change_active_resume(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.make_active_resume(pk):
                    m = 'Active resume changed successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_resume(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_resume(pk):
                    m = 'Resume deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_errors(), 'danger', m)

        return redirect('resume:index')


def new_language(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_language_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_language(pk, i):
                        m = 'New language added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_language(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_language(rk, pk):
                    m = 'Language added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_language(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_language_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_language(pk, i):
                        m = 'Language edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_language(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_language(rk, pk):
                    m = 'Language deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def new_experience(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_experience_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_experience(pk, i):
                        m = 'New experience added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_experience(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_experience(rk, pk):
                    m = 'Experience added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_experience(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_experience_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_experience(pk, i):
                        m = 'Experience edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_experience(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_experience(rk, pk):
                    m = 'Experience deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def new_award(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_award_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_award(pk, i):
                        m = 'New award added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_award(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_award(rk, pk):
                    m = 'Award added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_award(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_award_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_award(pk, i):
                        m = 'Award edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_award(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_award(rk, pk):
                    m = 'Award deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def new_school(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_school_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_school(pk, i):
                        m = 'New school added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_school(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_school(rk, pk):
                    m = 'School added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_school(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_school_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_school(pk, i):
                        m = 'School edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_school(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_school(rk, pk):
                    m = 'School deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def new_skill(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_skill_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_skill(pk, i):
                        m = 'New skill added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_skill(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_skill(rk, pk):
                    m = 'Skill added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_skill(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_skill_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_skill(pk, i):
                        m = 'Skill edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_skill(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_skill(rk, pk):
                    m = 'Skill deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def new_reference(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_reference_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.new_reference(pk, i):
                        m = 'New reference added successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def add_reference(request, pk, rk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_reference(rk, pk):
                    m = 'Reference added successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def edit_reference(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)
        rq = RequestUtil()
        i = rq.get_reference_info(request)
        if i:

            try:
                with transaction.atomic():
                    if student.edit_reference(pk, i):
                        m = 'Reference edited successfully.'
                        MessageCenter.new_message('student', student.get_student(), 'success', m)
                        return HttpResponse(m, status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                m = str(student.get_errors())
                return HttpResponse(m, status=400)

        else:
            m = str(rq.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


def delete_reference(request, rk, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_reference(rk, pk):
                    m = 'Reference deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=rk)

    raise Http404


def add_file_resume(request, pk):

    if request.method == 'POST':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.add_file_resume(pk, request.POST, request.FILES):
                    m = 'File uploaded successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    data = {'is_valid': True}
                    return JsonResponse(data)
                else:
                    raise IntegrityError
        except IntegrityError:
            data = {'is_valid': False, 'error': str(student.get_errors())}
            return JsonResponse(data)

    raise Http404


def delete_file_resume(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.delete_file_resume(pk):
                    m = 'File resume deleted successfully.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(student.get_errors())
            MessageCenter.new_message('student', student.get_student(), 'danger', m)

        return redirect('resume:details', pk=pk)

    raise Http404



