from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Company
from event.models import Event
from home.models import JobinTerritory
from home.utils import MessageCenter, Pagination
from .forms import NewCompanyForm
from post.models import Post
from post.utils import PostUtil
from django.views.generic import View
import simplejson
from django.http import HttpResponse


class IndexView(View):
    template_name = 'company/company_home.html'

    def get(self, request):
        user = self.request.user
        res = Company.objects.filter(user=user)
        if res.count() > 0:
            posts = Post.objects.filter(company=res.first(), status='open')
            temp = PostUtil.do_post_notifications(posts)
            if len(temp) > 0:
                MessageCenter.new_applicants_message(res.first(), temp)
            msgs = MessageCenter.get_messages('company', res.first())
            events = Event.objects.filter(company=res.first(), active=True)
            ppages = Pagination.get_pages(posts)
            epages = Pagination.get_pages(events)
            context = {
                'company': res.first(),
                'posts': Pagination.get_page_items(posts),
                'events': Pagination.get_page_items(events),
                'msgs': msgs,
                'notifications': MessageCenter.get_notifications('company', res.first()),
                'ppages': ppages,
                'ppage': 1,
                'epages': epages,
                'epage': 1,
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        else:
            return redirect('company:new')

    def post(self, request):
        company = Company.objects.get(user=self.request.user)
        ppage = int(request.POST.get('post_page'))
        epage = int(request.POST.get('event_page'))
        print('epage: ' + str(epage))
        print('ppage: ' + str(ppage))
        posts = Post.objects.filter(company=company, status='open')
        temp = PostUtil.do_post_notifications(posts)
        if len(temp) > 0:
            MessageCenter.new_applicants_message(company, temp)
        msgs = MessageCenter.get_messages('company', company)
        events = Event.objects.filter(company=company, active=True)
        ppages = Pagination.get_pages(posts)
        epages = Pagination.get_pages(events)
        context = {
            'company': company,
            'posts': Pagination.get_page_items(posts, ppage),
            'events': Pagination.get_page_items(events, epage),
            'msgs': msgs,
            'notifications': MessageCenter.get_notifications('company', company),
            'ppages': ppages,
            'ppage': ppage + 1,
            'epages': epages,
            'epage': epage + 1,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class NewCompanyView(CreateView):
    model = Company
    form_class = NewCompanyForm

    def form_valid(self, form):
        company = form.save(commit=False)
        company.user = self.request.user
        company.points = 0
        company.email = self.request.user.email
        return super(NewCompanyView, self).form_valid(form)


class UpdateCompanyView(UpdateView):
    model = Company
    form_class = NewCompanyForm

    def get_context_data(self, **kwargs):
        context = super(UpdateCompanyView, self).get_context_data(**kwargs)
        context['update'] = 'True'
        return context

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        MessageCenter.company_updated(company)
        return super(UpdateCompanyView, self).form_valid(form)


class DetailsView(generic.DetailView):
    model = Company
    template_name = 'company/company_details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        company.is_new = False
        company.save()
        MessageCenter.company_created(company)
        return context


class ProfileView(View):
    template_name = 'company/company_profile.html'

    def get(self, request):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        return render(request, self.template_name, {'company': company, 'user': user})




