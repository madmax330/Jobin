from django.views.generic import View
from django.shortcuts import redirect, render, Http404, HttpResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from home.utils import MessageCenter, Pagination
from home.util_home import HomeUtil

from company.util_company import CompanyContainer
from student.util_student import StudentContainer


@login_required(login_url='/')
def company_index(request):
    if request.method == 'GET':
        event_page = request.GET.get('ep', 1)
        ex_event_page = request.GET.get('xep', 1)
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
        msgs = MessageCenter.get_messages('company', company.get_company())
        events = Pagination(company.get_events(), 10)
        ex_events = Pagination(company.get_expired_events(), 10)
        context = {
            'company': company.get_company(),
            'events': events.get_page(event_page),
            'expired_events': ex_events.get_page(ex_event_page),
            'messages': msgs,
            'tab': 'events',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'event/company_index.html', context)

    raise Http404


class NewEventView(LoginRequiredMixin, View):
    template_name = 'event/event_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
            'new': True,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
            'new': True,
        }
        info = request.POST.copy()

        try:
            with transaction.atomic():
                if company.new_event(info):
                    return redirect('event:company_events')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['event'] = info
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


class EditEventView(LoginRequiredMixin, View):
    template_name = 'event/event_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'event': company.get_event(pk),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'event': company.get_event(pk),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
        }
        info = request.POST.copy()
        info['id'] = pk

        try:
            with transaction.atomic():
                if company.edit_event(pk, info):
                    return redirect('event:company_events')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['event'] = info
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


@login_required(login_url='/')
def close_event(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        context = {
            'event': company.get_event(pk),
            'company': company.get_company(),
            'tab': 'events',
        }

        try:
            with transaction.atomic():
                if company.close_event(pk):
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            return HttpResponse(str(company.get_errors()), status=400)

        return render(request, 'event/detail.html', context)

    raise Http404


@login_required(login_url='/')
def detail_view(request, pk):
    if request.method == 'GET':
        company = CompanyContainer(request.user)
        context = {
            'event': company.get_event(pk),
            'company': company.get_company(),
            'tab': 'events',
        }
        return render(request, 'event/detail.html', context)

    raise Http404


@login_required(login_url='/')
def student_index(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)
        if student.get_student() is None:
            return redirect('student:new')
        msgs = MessageCenter.get_messages('student', student.get_student())
        events = student.get_events(pk)
        context = {
            'student': student.get_student(),
            'events': events,
            'count': len(events),
            'messages': msgs,
            'tab': 'events',
        }
        return render(request, 'event/student_index.html', context)

    raise Http404


class RecoverEventView(LoginRequiredMixin, View):
    template_name = 'event/event_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'event': company.get_event(pk),
            'company': company.get_company(),
            'tab': 'events',
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'tab': 'events',
        }
        info = request.POST.copy()
        info['id'] = pk

        try:
            with transaction.atomic():
                if company.recover_event(pk, info):
                    return redirect('event:company_events')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['event'] = info
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


@login_required(login_url='/')
def save_event(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.save_event(pk):
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404


@login_required(login_url='/')
def remove_saved_event(request, pk):
    if request.method == 'GET':
        student = StudentContainer(request.user)

        try:
            with transaction.atomic():
                if student.remove_saved_event(pk):
                    m = 'Event successfully removed.'
                    MessageCenter.new_message('student', student.get_student(), 'success', m)
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            m = str(student.get_errors())
            return HttpResponse(m, status=400)

    raise Http404
