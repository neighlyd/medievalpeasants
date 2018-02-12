from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.urls import reverse_lazy, reverse
from django.db.models import Count, Max, Min, Avg, Sum
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory

from braces.views import GroupRequiredMixin


from . import models
from . import forms

Delete = [u"Full Editor"]
Edit = [u"Full Editor", u"Editor"]
Add = [u"Full Editor", u"Editor", u"Contributor"]


class ArchiveDetailView(DetailView):

    queryset = models.Archive.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ArchiveDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Archive'
        return context
    

class ArchiveListView(ListView):

    model = models.Archive
    queryset = models.Archive.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(ArchiveListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Archive'
        return context


class ArchiveEditView(GroupRequiredMixin, UpdateView):

    model = models.Archive
    fields = ['name', 'website', 'notes']
    template_name = 'archive/archive_edit.html'

    group_required = Edit

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('archive', kwargs={'pk': pk})


class ArchiveAddView(GroupRequiredMixin, CreateView):

    model = models.Archive
    fields = ['name', 'website', 'notes']
    template_name = 'archive/archive_add.html'

    group_required = Add

    def get_success_url(self):
        return reverse('archive', args=(self.object.id,))


class ArchiveDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Archive
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('archive_list')


class RecordDetailView(DetailView):
    model = models.Record
    queryset = models.Record.objects.all().prefetch_related('session_set')

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Record'
        return context


class RecordListView(ListView):
    model = models.Record
    queryset = models.Record.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Record'
        return context


class RecordEditView(GroupRequiredMixin, UpdateView):

    model = models.Record
    fields = ['name', 'archive', 'record_type', 'reel', 'notes']
    template_name = 'record/record_edit.html'

    group_required = Edit

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('record', kwargs={'pk': pk})



class RecordAddView(GroupRequiredMixin, CreateView):

    model = models.Record
    fields = ['name', 'archive', 'record_type', 'reel', 'notes']
    template_name = 'record/record_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('record', args=(self.object.id,))

    def get_initial(self):
        initial = super(RecordAddView, self).get_initial()
        archive = self.request.GET.get('archive')
        initial['archive'] = archive
        return initial



class RecordDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Record
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('record_list')


class CaseListView(ListView):

    model = models.Case
    queryset = models.Case.objects.all().select_related('session').order_by('session__village__name', 'session__date',
                                                                            'court_type')

    def get_context_data(self, **kwargs):
        context = super(CaseListView, self).get_context_data(**kwargs)
        filter_case_form = forms.CaseFilterForm(self.request.GET or None)
        context['filter_case_form'] = filter_case_form
        context['page_title'] = 'Case'
        return context
    

class CaseDetailView(DetailView):

    model = models.Case
    queryset = models.Case.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CaseDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Case'
        return context


def CaseEditView(request, pk):

    case = get_object_or_404(models.Case, pk=pk)
    litigants = models.Litigant.objects.filter(case = case)
    # inlines
    LitigantFormset = inlineformset_factory(models.Case, models.Litigant, form=forms.LitigantForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = forms.CaseForm(request.POST, instance=case)
        litigant_formset = LitigantFormset(request.POST, prefix='litigant')
    else:
        form = forms.CaseForm(instance=case)
        litigant_formset = LitigantFormset(instance=case, prefix='litigant')

    context = {
        'case': case,
        'litigants': litigants,
        'form': form,
        'litigant_formset': litigant_formset,
    }

    return render(request, 'case/case_edit.html', context)


def add_litigant(request):

    data = dict()

    if request.method == "POST":
        form = forms.LitigantForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.LitigantForm()

    context = {'form': form}

    # Before passing context along, render it as a string so that it can be serialized and sent as JSON data.
    data['html_form'] = render_to_string('case/_case_add_litigant_modal.html', context, request=request)

    return JsonResponse(data)


def edit_litigant(request, id):
    litigant = get_object_or_404(models.Litigant, pk=id)

    data = dict()

    if request.method == 'POST':
        form = forms.LitigantForm(request.POST, instance=litigant)
    else:
        form = forms.LitigantForm(instance=litigant)

    context = {'form': form}

    data['html_form'] = render_to_string('case/_case_edit_litigant_modal.html', context, request=request)

    return JsonResponse(data)



def add_case(request):

    initial = dict()

    if request.method == 'POST':
        form = forms.CaseForm(request.POST)
        if 'add_litigants' in request.POST:
            if form.is_valid():
                case = form.save(commit=False)
                case.save()
                return redirect('edit_case', pk=case.pk)
        elif 'add_another' in request.POST:
            if form.is_valid():
                case = form.save(commit=False)
                case.save()
                session = str(case.session.id)
                case_type = str(case.case_type.id)
                court_type = str(case.court_type)
                return HttpResponseRedirect(
                    reverse('add_case') + "?session=" + session + "&case_type=" + case_type +
                    "&court_type=" + court_type)
    else:
        session = request.GET.get('session')
        case_type = request.GET.get('case_type')
        court_type = request.GET.get('court_type')
        initial['session'] = session
        initial['case_type'] = case_type
        initial['court_type'] = court_type
        if (initial is not None):
            form = forms.CaseForm(initial=initial)
        else:
            form = forms.CaseForm

    return render(request, 'case/case_add.html', {'form': form})

'''
class CaseEditView(GroupRequiredMixin, UpdateView):

    model = models.Case
    form_class = forms.CaseForm
    template_name = 'case/case_edit.html'

    group_required = Edit
    def get_context_data(self, **kwargs):
        context = super(CaseEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = forms.LitigantFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = forms.LitigantFormset(instance=self.object)
        return context

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('case', kwargs={'pk': pk})


class CaseAddView(GroupRequiredMixin, CreateView):

    model = models.Case
    fields = ['summary', 'session', 'case_type', 'court_type', 'verdict', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale', 'incidental_land']
    template_name = 'case/case_add.html'
    form = forms.CaseForm
    group_required = Add

    def form_valid(self, form):
        if 'add_single' in self.request.POST:
            pass
        if 'add_another' in self.request.POST:
            self.object = form.save()
            session = str(self.object.session.id)
            case_type = str(self.object.case_type.id)
            court_type = str(self.object.court_type)
            return HttpResponseRedirect(reverse('add_case') + "?session=" + session + "&case_type=" + case_type +
                                        "&court_type=" + court_type)

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('case', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        data = super(CaseAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['litigant_formset'] = forms.LitigantFormset(self.request.POST)
        else:
            data['litigant_formset'] = forms.LitigantFormset()
        return data

    def get_initial(self):
        initial = super(CaseAddView, self).get_initial()
        session = self.request.GET.get('session')
        case_type = self.request.GET.get('case_type')
        court_type = self.request.GET.get('court_type')
        initial['session'] = session
        initial['case_type'] = case_type
        initial['court_type'] = court_type
        return initial
'''

# temp view for testing an idea
class LitigantListforAddCase(ListView):

    model = models.Litigant

    def get_queryset(self):
        return models.Litigant.objects.filter(case=self.kwargs['pk'])

class CaseDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Case
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('case_list')


class CountyDetailView(DetailView):

    model = models.County
    queryset = models.County.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CountyDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'County'
        return context


class CountyListView(ListView):

    model = models.County
    queryset = models.County.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CountyListView, self).get_context_data(**kwargs)
        context['page_title'] = 'County'
        return context
    

class CountyEditView(GroupRequiredMixin, UpdateView):

    model = models.County
    fields = ['name', 'abbreviation',]
    template_name = 'county/county_edit.html'

    group_required = Edit

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('county', kwargs={'pk': pk})


class CountyAddView(GroupRequiredMixin, CreateView):

    model = models.County
    fields = ['name', 'abbreviation',]
    template_name = 'county/county_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('county', args=(self.object.id,))


class CountyDeleteView(GroupRequiredMixin, DeleteView):

    model = models.County
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('county_list')


class HundredDetailView(DetailView):

    model = models.Hundred
    queryset = models.Hundred.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HundredDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Hundred'
        return context


class HundredListView(ListView):

    model = models.Hundred
    queryset = models.Hundred.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HundredListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Hundred'
        return context


class HundredEditView(GroupRequiredMixin, UpdateView):

    model = models.Hundred
    fields = ['name', 'county',]
    template_name = 'hundred/hundred_edit.html'

    group_required = Edit

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('hundred', kwargs={'pk': pk})



class HundredAddView(GroupRequiredMixin, CreateView):

    model = models.Hundred
    fields = ['name', 'county',]
    template_name = 'hundred/hundred_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('hundred', args=(self.object.id,))

    def get_initial(self):
        initial = super(HundredAddView, self).get_initial()
        county = self.request.GET.get('county')
        initial['county'] = county
        return initial



class HundredDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Hundred
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('hundred_list')


class LitigantListView(ListView):

    model = models.Litigant
    queryset = models.Litigant.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(LitigantListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Litigant'
        return context


class LandDetailView(DetailView):

    model = models.Land
    queryset = models.Land.objects.prefetch_related('parcels').all()
    
    def get_context_data(self, **kwargs):
        context = super(LandDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Land'
        return context


class LandListView(ListView):

    model = models.Land
    queryset = models.Land.objects.all()

    def get_context_data(self, **kwargs):
        context = super(LandListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Land'
        return context
    

class PeopleListView(ListView):

    model = models.Person
    queryset = models.Person.objects.all()
    context_object_name = 'person_list'

    def get_context_data(self, **kwargs):
        context = super(PeopleListView, self).get_context_data(**kwargs)
        context['current_url'] = resolve(self.request.path_info).url_name
        filter_village_form = forms.PersonFilterForm(self.request.GET or None)
        context['filter_village_form'] = filter_village_form
        context['page_title'] = 'People'
        return context


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

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Person'
        return context


class SessionDetailView(DetailView):

    model = models.Session
    queryset = models.Session.objects.all().select_related('village')
    
    def get_context_data(self, **kwargs):
        context = super(SessionDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Session'
        return context


class SessionListView(ListView):

    model = models.Session
    queryset = models.Session.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(SessionListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Session'
        return context
    
        
class SessionEditView(GroupRequiredMixin, UpdateView):

    model = models.Session
    fields = ['date', 'law_term', 'folio', 'record', 'village', 'notes']
    template_name = 'session/session_edit.html'

    group_required = Edit

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse('session', kwargs={'pk': pk})


class SessionAddView(GroupRequiredMixin, CreateView):

    model = models.Session
    fields = ['date', 'law_term', 'folio', 'record', 'village', 'notes']
    template_name = 'session/session_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('session', args=(self.object.id,))

    def get_initial(self):
        initial = super(SessionAddView, self).get_initial()
        record = self.request.GET.get('record')
        initial['record'] = record
        return initial


class SessionDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Session
    template_name = 'session/session_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('session_list')

    

class VillageDetailView(DetailView):

    model = models.Village
    queryset = models.Village.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(VillageDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Village'
        return context
    

class VillageListView(ListView):

    model = models.Village
    queryset = models.Village.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(VillageListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Village'
        return context


class ChevageAnalysisListView(ListView):

    model = models.Person
    queryset = models.Person.objects.all().filter(person_to_case__chevage__isnull=False).distinct()\
        .prefetch_related('person_to_case__case__session','village').order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super(ChevageAnalysisListView, self).get_context_data(**kwargs)
        qs = context['object_list']
        village_id = self.kwargs.get('village_pk')
        chevage_list = qs.filter(person_to_case__case__session__village=village_id).filter(person_to_case__chevage__isnull=True)
        village =  models.Village.objects.get(id=village_id)
        context['chevage_list'] = chevage_list
        context['village'] = village
        context['page_title'] = 'Chevage'
        return context