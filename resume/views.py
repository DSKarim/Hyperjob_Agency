from django.shortcuts import render
from django.views import View
from .models import Resume
from vacancy.models import Vacancy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import AddForm


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'resume/main.html')


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'resume/login.html'


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'resume/signup.html'


class Resumes(View):
    def get(self, request, *args, **kwargs):
        resume = Resume.objects.all()
        return render(request, 'resume/resumes.html', context={'resumes': resume})


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, 'resume/home.html')
        else:
            return HttpResponseRedirect('/login')


class NewResumeView(View):
    def post(self, request, *args, **kwargs):
        form = AddForm(request.POST)
        clean_form = dict()
        if form.is_valid():
            clean_form = form.cleaned_data
            description = clean_form['description']
            if request.user.is_authenticated and not request.user.is_staff:
                # Resume.objects.filter(author=request.user).update(description=description)
                r = Resume(description=description, author=request.user)
                r.save()
                del r
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()


class NewVacancyView(View):
    def post(self, request, *args, **kwargs):
        form = AddForm(request.POST)
        clean_form = dict()
        if form.is_valid():
            clean_form = form.cleaned_data
            description = clean_form['description']
            if request.user.is_authenticated and request.user.is_staff:
                # Resume.objects.filter(author=request.user).update(description=description)
                r = Vacancy(description=description, author=request.user)
                r.save()
                del r
                return HttpResponseRedirect('/home')
            else:
                return HttpResponseForbidden()
        return HttpResponseForbidden()
