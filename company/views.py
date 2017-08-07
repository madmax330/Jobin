from django.views.generic import View
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from django.db import transaction, IntegrityError

from .util_company import CompanyContainer

from home.util_request import RequestUtil
from home.utils import MessageCenter, Pagination
from home.util_home import HomeUtil


def index_view(request):

    if request.method == 'GET':
        post_page = request.GET.get('pp', 1)
        event_page = request.GET.get('ep', 1)
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
        msgs = MessageCenter.get_messages('company', company.get_company())
        posts = Pagination(company.get_home_posts(), 15)
        events = Pagination(company.get_events(), 15)
        context = {
            'company': company.get_company(),
            'posts': posts.get_page(post_page),
            'events': events.get_page(event_page),
            'messages': msgs,
            'notifications': MessageCenter.get_notifications('company', company.get_company()),
            'tab': 'home',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'company/index.html', context)

    raise Http404


class NewCompanyView(View):
    template_name = 'company/company_form.html'

    def get(self, request):
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        rq = RequestUtil()
        i = rq.get_company_info(request)
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
        }
        if i:

            try:
                with transaction.atomic():
                    if company.new_company(i, request.user):
                        m = 'Company profile created successfully.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return redirect('company:index')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['company'] = i
                context['errors'] = company.get_form().errors

        else:
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


class EditCompanyView(View):
    template_name = 'company/company_form.html'

    def get(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'profile',
        }
        print(str(company.get_company().is_startup))
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        rq = RequestUtil()
        i = rq.get_company_info(request)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'profile',
        }
        if i:

            try:
                with transaction.atomic():
                    if company.edit_company(i):
                        m = 'Company profile edited successfully.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return redirect('company:index')
                    else:
                        raise IntegrityError
            except IntegrityError:
                context['errors'] = company.get_form().errors

        else:
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


def profile_view(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)
        context = {
            'user': company.get_user(),
            'company': company.get_company(),
            'tab': 'profile',
        }
        return render(request, 'company/profile.html', context)

    raise Http404


def suggestions_view(request):

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        company = CompanyContainer(request.user)
        suggestions = Pagination(company.get_suggestions(), 10)
        msgs = MessageCenter.get_messages('company', company.get_company())
        context = {
            'suggestions': suggestions.get_page(page),
            'company': company.get_company(),
            'messages': msgs,
            'tab': 'suggestions',
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'company/suggestions.html', context)

    raise Http404


def new_suggestion(request):

    if request.method == 'POST':
        company = CompanyContainer(request.user)
        rq = RequestUtil()
        i = rq.get_suggestion_info(request)
        if i:

            try:
                with transaction.atomic():
                    if company.new_suggestion(i):
                        m = 'Suggestion successfully submitted.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return HttpResponse(status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                return HttpResponse(str(company.get_errors()), status=400)

        else:
            return HttpResponse(str(rq.get_errors()), status=400)

    raise Http404


def company_not_new(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)
        if company.not_new():
            return HttpResponse('good', status=200)
        else:
            return HttpResponse(str(company.get_errors()), status=400)

    raise Http404


def upload_logo(request):

    if request.method == 'POST':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.upload_logo(request.POST, request.FILES):
                    m = 'Logo uploaded successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    data = {'is_valid': True}
                    return JsonResponse(data)
                else:
                    raise IntegrityError
        except IntegrityError:
            data = {'is_valid': False, 'error': str(company.get_errors())}
            return JsonResponse(data)

    raise Http404


def delete_logo(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)

        try:
            with transaction.atomic():
                if company.delete_logo():
                    m = 'Logo delete successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                else:
                    raise IntegrityError
        except IntegrityError:
            m = str(company.get_errors())
            MessageCenter.new_message('company', company.get_company(), 'danger', m)

        return redirect('company:index')

    raise Http404


def comment_suggestion(request, pk):

    if request.method == 'POST':
        company = CompanyContainer(request.user)
        comment = request.POST.get('suggestion_comment')
        if comment:

            try:
                with transaction.atomic():
                    if company.comment_suggestion(pk, comment):
                        m = 'Comment successfully added.'
                        MessageCenter.new_message('company', company.get_company(), 'success', m)
                        return HttpResponse(status=200)
                    else:
                        raise IntegrityError
            except IntegrityError:
                return HttpResponse(str(company.get_errors()), status=400)

        else:
            return HttpResponse('Comment field cannot be empty', status=400)


