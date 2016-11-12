from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from .models import Company
from home.models import Message, Notification,JobinTerritory
from .forms import NewCompanyForm
from post.models import Post
from django.views.generic import View
import simplejson
from django.http import HttpResponse


class IndexView(View):
    template_name = 'company/company_home.html'

    def get(self, request):
        res = Company.objects.filter(user=request.user)
        if res.count() > 0:
            posts = Post.objects.filter(company=res.first(), status='open')
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
        x = Message()
        x.code = 'info'
        x.message = 'Your profile was successfully updated.'
        x.company = company
        x.save()


class DetailsView(generic.DetailView):
    model = Company
    template_name = 'company/company_details.html'

    def get_context_data(self, **kwargs):
        context = super(DetailsView, self).get_context_data(**kwargs)
        x = Message()
        x.code = 'info'
        x.company = Company.objects.get(user=self.request.user)
        x.message = 'Your profile was successfully created. Welcome to Jobin!'
        x.save()
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