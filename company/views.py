from django.views.generic import View
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .util_company import CompanyContainer

from home.utils import MessageCenter, Pagination
from home.util_home import HomeUtil


@login_required(login_url='/')
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


class NewCompanyView(LoginRequiredMixin, View):
    template_name = 'company/company_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'new': True,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        context = {
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'new': True
        }

        try:

            with transaction.atomic():
                if company.new_company(request.POST.copy(), request.user):
                    m = 'Company profile created successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return redirect('company:index')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['company'] = request.POST
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


class EditCompanyView(LoginRequiredMixin, View):
    template_name = 'company/company_form.html'
    login_url = '/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'profile',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        company = CompanyContainer(request.user)
        context = {
            'company': company.get_company(),
            'countries': HomeUtil.get_countries(),
            'states': HomeUtil.get_states(),
            'tab': 'profile',
        }

        try:

            with transaction.atomic():
                if company.edit_company(request.POST.copy()):
                    m = 'Company profile edited successfully.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return redirect('company:profile')
                else:
                    raise IntegrityError

        except IntegrityError:
            context['company'] = request.POST
            context['errors'] = company.get_form_errors()

        return render(request, self.template_name, context)


@login_required(login_url='/')
def profile_view(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
        msgs = MessageCenter.get_messages('company', company.get_company())
        context = {
            'user': company.get_user(),
            'company': company.get_company(),
            'tab': 'profile',
            'messages': msgs,
        }
        MessageCenter.clear_msgs(msgs)
        return render(request, 'company/profile.html', context)

    raise Http404


@login_required(login_url='/')
def suggestions_view(request):

    if request.method == 'GET':
        page = request.GET.get('page', 1)
        company = CompanyContainer(request.user)
        if company.get_company() is None:
            return redirect('company:new')
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


@login_required(login_url='/')
def new_suggestion(request):

    if request.method == 'POST':
        company = CompanyContainer(request.user)

        try:

            with transaction.atomic():
                if company.new_suggestion(request.POST.copy()):
                    m = 'Suggestion successfully submitted.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse(status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            return HttpResponse(str(company.get_errors()), status=400)

    raise Http404


@login_required(login_url='/')
def company_not_new(request):

    if request.method == 'GET':
        company = CompanyContainer(request.user)
        if company.not_new():
            return HttpResponse('good', status=200)
        else:
            return HttpResponse(str(company.get_errors()), status=400)

    raise Http404


@login_required(login_url='/')
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


@login_required(login_url='/')
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

        return redirect('company:profile')

    raise Http404


@login_required(login_url='/')
def comment_suggestion(request, pk):

    if request.method == 'POST':
        company = CompanyContainer(request.user)

        try:

            with transaction.atomic():
                if company.comment_suggestion(pk, request.POST.copy()):
                    m = 'Comment successfully added.'
                    MessageCenter.new_message('company', company.get_company(), 'success', m)
                    return HttpResponse(status=200)
                else:
                    raise IntegrityError

        except IntegrityError:
            return HttpResponse(str(company.get_errors()), status=400)

    raise Http404
