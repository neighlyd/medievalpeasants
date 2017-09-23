from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from . import models


class PeopleListView(ListView):
    model = models.Person
    queryset = models.Person.objects.all().select_related('village').order_by('first_name')
    context_object_name = 'person_list'


class PersonView(DetailView):
    model = models.Person
    queryset = models.Person.objects.all()


class CaseListView(ListView):
    model = models.Case
    queryset = models.Case.objects.all().select_related('session').order_by('session__village__name', 'session__date', 'court_type')
    context_object_name = 'case_list'


class CaseView(DetailView):
    model = models.Case
    queryset = models.Case.objects.all()

class LitigantListView(ListView):
    model = models.Litigant
    queryset = models.Litigant.objects.all()