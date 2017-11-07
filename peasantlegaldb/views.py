from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.db.models import Count, Max, Min, Avg, Sum
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import forms


class ArchiveDetailView(DetailView):

    model = models.Archive
    queryset = models.Archive.objects.all()


class ArchiveListView(ListView):

    model = models.Archive
    queryset = models.Archive.objects.all()


class CaseListView(ListView):

    model = models.Case
    queryset = models.Case.objects.all().select_related('session').order_by('session__village__name', 'session__date',
                                                                            'court_type')
    context_object_name = 'case_list'


class CaseListFilterView(FormView):

    form_class = forms.CaseFilterForm


class CaseDetailView(DetailView):

    model = models.Case
    queryset = models.Case.objects.all()


class CountyDetailView(DetailView):

    model = models.County
    queryset = models.County.objects.all()


class CountyListView(ListView):

    model = models.County
    queryset = models.County.objects.all()


class HundredDetailView(DetailView):

    model = models.Hundred
    queryset = models.Hundred.objects.all()


class HundredListView(ListView):

    model = models.Hundred
    queryset = models.Hundred.objects.all()


class LitigantListView(ListView):

    model = models.Litigant
    queryset = models.Litigant.objects.all()


class LandDetailView(DetailView):

    model = models.Land
    queryset = models.Land.objects.prefetch_related('parcels').all()

class LandListView(ListView):

    model = models.Land
    queryset = models.Land.objects.all()


class PeopleListView(ListView):

    model = models.Person
    queryset = models.Person.objects.all()
    context_object_name = 'person_list'

    def get_context_data(self, **kwargs):
        context = super(PeopleListView, self).get_context_data(**kwargs)
        context['current_url'] = resolve(self.request.path_info).url_name
        context['title'] = self.kwargs.get('title')
        return context

class PeopleListFilterView(FormView):
    queryset = models.Person.objects.all()
    form_class = forms.PersonFilterForm


class PersonDetailView(DetailView):

    model = models.Person
    queryset = models.Person.objects.all().annotate(amercement_count=Count('person_to_case__amercement'),
                                                    amercement_max=Max('person_to_case__amercement__in_denarius'),
                                                    amercement_min=Min('person_to_case__amercement__in_denarius'),
                                                    amercement_avg=Avg('person_to_case__amercement__in_denarius'),
                                                    amercement_sum=Sum('person_to_case__amercement__in_denarius'),
                                                    fine_count=Count('person_to_case__fine'),
                                                    fine_max=Max('person_to_case__fine__in_denarius'),
                                                    fine_min=Min('person_to_case__fine__in_denarius'),
                                                    fine_avg=Avg('person_to_case__fine__in_denarius'),
                                                    fine_sum=Sum('person_to_case__fine__in_denarius'),
                                                    damage_count=Count('person_to_case__damage'),
                                                    damage_max=Max('person_to_case__damage__in_denarius'),
                                                    damage_min=Min('person_to_case__damage__in_denarius'),
                                                    damage_avg=Avg('person_to_case__damage__in_denarius'),
                                                    damage_sum=Sum('person_to_case__damage__in_denarius'),
                                                    chevage_count=Count('person_to_case__chevage'),
                                                    chevage_max=Max('person_to_case__chevage__in_denarius'),
                                                    chevage_min=Min('person_to_case__chevage__in_denarius'),
                                                    chevage_avg=Avg('person_to_case__chevage__in_denarius'),
                                                    chevage_sum=Sum('person_to_case__chevage__in_denarius'),
                                                    heriot_count=Count('person_to_case__heriot'),
                                                    heriot_max=Max('person_to_case__heriot__in_denarius'),
                                                    heriot_min=Min('person_to_case__heriot__in_denarius'),
                                                    heriot_avg=Avg('person_to_case__heriot__in_denarius'),
                                                    heriot_sum=Sum('person_to_case__heriot__in_denarius'),
                                                    impercamentum_count=Count('person_to_case__impercamentum'),
                                                    impercamentum_max=Max('person_to_case__impercamentum__in_denarius'),
                                                    impercamentum_min=Min('person_to_case__impercamentum__in_denarius'),
                                                    impercamentum_avg=Avg('person_to_case__impercamentum__in_denarius'),
                                                    impercamentum_sum=Sum('person_to_case__impercamentum__in_denarius'))


class RecordDetailView(DetailView):

    model = models.Record
    queryset = models.Record.objects.all().prefetch_related('session_set')


class RecordListView(ListView):

    model = models.Record
    queryset = models.Record.objects.all()


class SessionDetailView(DetailView):

    model = models.Session
    queryset = models.Session.objects.all().select_related('village')


class SessionListView(ListView):

    model = models.Session
    queryset = models.Session.objects.all()
    

class VillageDetailView(DetailView):

    model = models.Village
    queryset = models.Village.objects.all()
    

class VillageListView(ListView):

    model = models.Village
    queryset = models.Village.objects.all()


    