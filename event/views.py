from django.views.generic import View
from django.shortcuts import redirect, render, Http404, HttpResponse
from django.db import transaction, IntegrityError

from home.utils import MessageCenter, Pagination
from home.util_home import HomeUtil
from home.util_request import RequestUtil

from company.util_company import CompanyContainer
from student.util_student import StudentContainer


def company_index(request):
    if request.method == 'GET':
        event_page = request.GET.get('ep', 1)
        ex_event_page = request.GET.get('xep', 1)
        company = CompanyContainer(request.user)
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


class NewEventView(View):
    template_name = 'event/event_form.html'

    def get(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        rq = RequestUtil()
        i = rq.get_event_info(request)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
        }
        if i:

            try:
                with transaction.atomic():
                    if company.new_event(i):
                        m = 'New event created successfully.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return redirect('event:company_events')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['event'] = i
                context['errors'] = company.get_form().errors

        else:
            context['event'] = i
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


class EditEventView(View):
    template_name = 'event/event_form.html'

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
        rq = RequestUtil()
        i = rq.get_event_info(request)
        context = {
            'company': company.get_company(),
            'event': company.get_event(pk),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'events',
        }
        if i:

            try:
                with transaction.atomic():
                    if company.edit_event(pk, i):
                        m = 'Event edited successfully.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return redirect('event:company_events')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['event'] = i
                context['errors'] = company.get_form().errors

        else:
            context['event'] = i
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


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
                    m = 'Event successfully closed.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse('success', status=200)
                else:
                    raise IntegrityError
        except IntegrityError:
            return HttpResponse(str(company.get_errors()), status=400)

        return render(request, 'event/detail.html', context)

    raise Http404


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


def student_index(request, pk):

    if request.method == 'GET':
        student = StudentContainer(request.user)
        msgs = MessageCenter.get_messages('student', student.get_student())
        notes = MessageCenter.get_notifications('student', student.get_student())
        events = student.get_events(pk)
        context = {
            'student': student.get_student(),
            'events': events,
            'count': len(events),
            'messages': msgs,
            'notifications': notes,
            'tab': 'events',
        }
        return render(request, 'event/student_index.html', context)

    raise Http404


class RecoverEventView(View):
    template_name = 'event/event_form.html'

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
        rq = RequestUtil()
        i = rq.get_event_info(request)
        context = {
            'company': company.get_company(),
            'tab': 'events',
        }
        if i:

            try:
                with transaction.atomic():
                    if company.recover_event(pk, i):
                        m = 'Event recovered successfully.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return redirect('event:company_events')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['event'] = i
                context['errors'] = company.get_form().errors

        else:
            context['errors'] = rq.get_errors()

        context['event'] = company.get_event(pk)
        return render(request, self.template_name, context)


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


