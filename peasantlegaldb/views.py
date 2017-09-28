from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.db.models import Count, Max, Min, Avg
from django.shortcuts import get_object_or_404

from . import models


class PeopleListView(ListView):

    model = models.Person
    queryset = models.Person.objects.all().select_related('village').order_by('first_name')
    context_object_name = 'person_list'


class PersonDetailView(DetailView):

    model = models.Person
    queryset = models.Person.objects.all().annotate(amercement_count=Count('person_to_case__amercement'),
                                                    amercement_max=Max('person_to_case__amercement__in_denarius'),
                                                    amercement_min=Min('person_to_case__amercement__in_denarius'),
                                                    amercement_avg=Avg('person_to_case__amercement__in_denarius'),
                                                    fine_count=Count('person_to_case__fine'),
                                                    fine_max=Max('person_to_case__fine__in_denarius'),
                                                    fine_min=Min('person_to_case__fine__in_denarius'),
                                                    fine_avg=Avg('person_to_case__fine__in_denarius'),
                                                    damage_count=Count('person_to_case__damage'),
                                                    damage_max=Max('person_to_case__damage__in_denarius'),
                                                    damage_min=Min('person_to_case__damage__in_denarius'),
                                                    damage_avg=Avg('person_to_case__damage__in_denarius'),
                                                    chevage_count=Count('person_to_case__chevage'),
                                                    chevage_max=Max('person_to_case__chevage__in_denarius'),
                                                    chevage_min=Min('person_to_case__chevage__in_denarius'),
                                                    chevage_avg=Avg('person_to_case__chevage__in_denarius'),
                                                    heriot_count=Count('person_to_case__heriot_assessment'),
                                                    heriot_max=Max('person_to_case__heriot_assessment__in_denarius'),
                                                    heriot_min=Min('person_to_case__heriot_assessment__in_denarius'),
                                                    heriot_avg=Avg('person_to_case__heriot_assessment__in_denarius'),
                                                    impercamentum_count=Count('person_to_case__impercamentum_amercement'),
                                                    impercamentum_max=Max('person_to_case__impercamentum_amercement__in_denarius'),
                                                    impercamentum_min=Min('person_to_case__impercamentum_amercement__in_denarius'),
                                                    impercamentum_avg=Avg('person_to_case__impercamentum_amercement__in_denarius'))


class CaseListView(ListView):

    model = models.Case
    queryset = models.Case.objects.all().select_related('session').order_by('session__village__name', 'session__date', 'court_type')
    context_object_name = 'case_list'


class CaseDetailView(DetailView):

    model = models.Case
    queryset = models.Case.objects.all()

class LitigantListView(ListView):

    model = models.Litigant
    queryset = models.Litigant.objects.all()