from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Company
from home.models import Message, Notification, JobinTerritory
from home.utils import new_message
from .forms import NewCompanyForm
from post.models import Post, Application
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
            temp = []
            for x in posts:
                if Application.objects.filter(post=x, cover_submitted=True, cover_opened=False, status='active').count() > 0:
                    x.notified = True
                else:
                    x.notified = False
                if Application.objects.filter(post=x, opened=False, status='active').count() > 0:
                    temp.append(x.title)
                    x.new_apps = True
                else:
                    x.new_apps = False
                x.save()
            if len(temp) > 0:
                msg = 'There are new applications for the following posts: '
                for x in temp:
                    msg += x
                    msg += ', '
                new_message('company', res.first(), 'info', msg[:-2])
            msgs = Message.objects.filter(company=res.first())
            context = {
                'company': res.first(),
                'posts': posts,
                'msgs': msgs,
                'notifications': Notification.objects.filter(company=res.first()).filter(opened=False),
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        else:
            return redirect('company:new')


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
        msg = 'Your profile was successfully updated.'
        new_message('company', company, 'info', msg)
        return super(UpdateCompanyView, self).form_valid(form)


class DetailsView(generic.DetailView):
    model = Company
    template_name = 'company/company_details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        company = Company.objects.get(user=self.request.user)
        company.is_new = False
        company.save()
        msg = 'Your profile was successfully created. Welcome to Jobin!'
        new_message('company', company, 'info', msg)
        return context


class ProfileView(View):
    template_name = 'company/company_profile.html'

    def get(self, request):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        return render(request, self.template_name, {'company': company, 'user': user})

def get_states(request, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')

def get_states_update(request,pk, country_name):
    states = JobinTerritory.objects.filter(country=country_name)
    state_dic = {}
    for state in states:
        state_dic[state.name] = state.name
    return HttpResponse(simplejson.dumps(state_dic), content_type='application/json')