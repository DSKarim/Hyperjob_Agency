from django.shortcuts import render
from django.views import View
from .models import Vacancy


class Vacancies(View):
    vacancy = Vacancy.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, 'vacancy/vacancies.html', context={'vacancies': self.vacancy})

