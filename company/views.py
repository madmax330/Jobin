from django.views.generic import View
from django.shortcuts import render, redirect, Http404
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
        msgs = MessageCenter.get_messages('company', company.get_company())
        posts = Pagination(company.get_posts(), 15)
        events = Pagination(company.get_events(), 15)
        context = {
            'company': company.get_company(),
            'posts': posts.get_page(post_page),
            'events': events.get_page(event_page),
            'messages': msgs,
            'notifications': MessageCenter.get_notifications('company', company.get_company()),
        }
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
                context['errors'] = company.get_errors()

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
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        rq = RequestUtil()
        i = rq.get_company_info(request)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
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
                context['errors'] = company.get_errors()

        else:
            context['errors'] = rq.get_errors()

        return render(request, self.template_name, context)


def profile_view(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)
        context = {
            'user': company.get_user(),
            'company': company.get_company(),
        }
        return render(request, 'company/profile.html', context)




