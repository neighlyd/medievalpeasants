from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.urls import reverse_lazy, reverse
from django.db.models import Count, Max, Min, Avg, Sum, Q
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from braces.views import GroupRequiredMixin

from . import models
from . import forms

import pdb


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
        return reverse('archive:detail', kwargs={'pk': pk})


class ArchiveAddView(GroupRequiredMixin, CreateView):

    model = models.Archive
    fields = ['name', 'website', 'notes']
    template_name = 'archive/archive_add.html'

    group_required = Add

    def get_success_url(self):
        return reverse('archive:detail', args=(self.object.id,))


class ArchiveDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Archive
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('archive:list')


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
        return reverse('record:detail', kwargs={'pk': pk})



class RecordAddView(GroupRequiredMixin, CreateView):

    model = models.Record
    fields = ['name', 'archive', 'record_type', 'reel', 'notes']
    template_name = 'record/record_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('record:detail', args=(self.object.id,))

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
        return reverse('record:list')


class CaseListView(ListView):

    model = models.Case
    queryset = models.Case.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CaseListView, self).get_context_data(**kwargs)
        filter_case_form = forms.CaseFilterForm(self.request.GET or None)
        context['filter_case_form'] = filter_case_form
        context['page_title'] = 'Case'
        return context


# view used to dynamically load list of case_types in the Case List view after selecting the village.
def load_case_types(request):
    village_id = request.GET.get('village')
    if (village_id == "All"):
        case_types = models.CaseType.objects.all().order_by('case_type').distinct()
    elif (village_id == "None"):
        case_types = models.CaseType.objects.none()
    else:
        case_types = models.CaseType.objects.filter(case__session__village_id=village_id).order_by('case_type').distinct()
    return render(request, 'case/case_type_dropdown.html', {'case_types': case_types})

def load_verdict_types(request):
    case_type_id = request.GET.get('case_type')
    if (case_type_id == "All"):
        verdicts = models.Verdict.objects.all().order_by('verdict').distinct()
    elif(case_type_id == "None"):
        verdicts = models.Verdict.objects.none()
    else:
        verdicts = models.Verdict.objects.filter(case__case_type=case_type_id).order_by('verdict').distinct()
    return render(request, 'case/verdict_type_dropdown.html', {'verdicts': verdicts})

class CaseDetailView(DetailView):

    model = models.Case
    queryset = models.Case.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(CaseDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Case'
        return context


def CaseEditView(request, pk):

    case = get_object_or_404(models.Case, pk=pk)
    litigant_list = models.Litigant.objects.filter(case = case).prefetch_related('person')\
        .order_by('person__first_name', 'person__last_name')

    if request.method == 'POST':
        form = forms.CaseForm(request.POST, instance=case)
    else:
        form = forms.CaseForm(instance=case)

    context = {
        'case': case,
        'litigant_list': litigant_list,
        'form': form,
    }

    return render(request, 'case/case_edit.html', context)


# TODO: Convert add_litigant and edit_litigant to class based views and add in GroupRequiredMixin.

def add_litigant(request, pk):

    data = dict()
    # Get the appropriate case pk for the litigant to be assigned to.
    case_instance = get_object_or_404(models.Case, pk=pk)

    if request.method == "POST":
        form = forms.LitigantForm(request.POST)
        amercement_formset = forms.AmercementFormset(request.POST, prefix='amercement')
        fine_formset = forms.FineFormset(request.POST, prefix='fine')
        damage_formset = forms.DamageFormset(request.POST, prefix='damage')
        heriot_formset = forms.HeriotFormset(request.POST, prefix='heriot')
        capitagium_formset = forms.CapitagiumFormset(request.POST, prefix='capitagium')
        impercamentum_formset = forms.ImpercamentumFormset(request.POST, prefix='impercamentum')
        land_formset = forms.LandFormset(request.POST, prefix='land')
        if form.is_valid():
            new_litigant = form.save(commit=False)
            new_litigant.case = case_instance
            new_litigant.save()
            # save any changes to the various formsets. Do this by first checking to see if the formset has changed.
            # If it has, then check to see if it is valid, if so, make an instance of it, add the litigant fk to that
            # instance, and then finally save it to the database.
            if amercement_formset.has_changed():
                if amercement_formset.is_valid():
                    for form in amercement_formset:
                        new_amercement = form.save(commit=False)
                        new_amercement.litigant = new_litigant
                        new_amercement.save()
            if fine_formset.has_changed():
                if fine_formset.is_valid():
                    for form in fine_formset:
                        new_fine = form.save(commit=False)
                        new_fine.litigant = new_litigant
                        new_fine.save()
            if damage_formset.has_changed():
                if damage_formset.is_valid():
                    for form in damage_formset:
                        new_damage = form.save(commit=False)
                        new_damage.litigant = new_litigant
                        new_damage.save()
            if heriot_formset.has_changed():
                if heriot_formset.is_valid():
                    for form in heriot_formset:
                        new_heriot = form.save(commit=False)
                        new_heriot.litigant = new_litigant
                        new_heriot.save()
            if capitagium_formset.has_changed():
                if capitagium_formset.is_valid():
                    for form in capitagium_formset:
                        new_capitagium = form.save(commit=False)
                        new_capitagium.litigant = new_litigant
                        new_capitagium.save()
            if impercamentum_formset.has_changed():
                if impercamentum_formset.is_valid():
                    for form in impercamentum_formset:
                        new_impercamentum = form.save(commit=False)
                        new_impercamentum.litigant = new_litigant
                        new_impercamentum.save()
            if land_formset.has_changed():
                if land_formset.is_valid():
                    for form in land_formset:
                        new_land = form.save(commit=False)
                        new_land.litigant = new_litigant
                        new_litigant.save()
            data['form_is_valid'] = True
            # Once litigant has been added, requery the Litigant model to retrieve an updated list of Litigants.
            litigant_list = models.Litigant.objects.filter(case=case_instance).prefetch_related('person')\
                .order_by('person__first_name', 'person__last_name')
            # Render the template to a string, with associated context (i.e. litigant list and case used for reversing
            # urls) and assign to a dict entry in data to pass through ajax.
            data['html_litigant_list'] = render_to_string('case/litigant_table_body_for_case.html',
                                                          {'litigant_list': litigant_list,
                                                           'case': case_instance}
                                                          )
        else:
            data['form_is_valid'] = False
    else:
        form = forms.LitigantForm(initial={'case' : case_instance})
        amercement_formset = forms.AmercementFormset(prefix='amercement')
        fine_formset = forms.FineFormset(prefix='fine')
        damage_formset = forms.DamageFormset(prefix='damage')
        heriot_formset = forms.HeriotFormset(prefix='heriot')
        capitagium_formset = forms.CapitagiumFormset(prefix='capitagium')
        impercamentum_formset = forms.ImpercamentumFormset(prefix='impercamentum')
        land_formset = forms.LandFormset(prefix='land')

    context = {
        'form': form, 
        'case': case_instance,
        'amercement_formset': amercement_formset,
        'fine_formset': fine_formset,
        'damage_formset': damage_formset,
        'heriot_formset': heriot_formset,
        'capitagium_formset': capitagium_formset,
        'impercamentum_formset': impercamentum_formset,
        'land_formset': land_formset,
    }

    # Before passing template and context along, render it as a string so that it can be serialized and sent as JSON data.
    data['html_form'] = render_to_string('case/_case_add_litigant_modal.html', context, request=request)

    return JsonResponse(data)


def edit_litigant(request, pk, litigant_pk):
    # See add_litigant for comments.
    litigant = get_object_or_404(models.Litigant, pk=litigant_pk)
    case_instance = litigant.case

    data = dict()

    if request.method == 'POST':
        form = forms.LitigantForm(data=request.POST, instance=litigant)
        amercement_formset = forms.AmercementFormset(request.POST, instance=litigant, prefix='amercement')
        fine_formset = forms.FineFormset(request.POST, instance=litigant, prefix='fine')
        damage_formset = forms.DamageFormset(request.POST, instance=litigant, prefix='damage')
        heriot_formset = forms.HeriotFormset(request.POST, instance=litigant, prefix='heriot')
        capitagium_formset = forms.CapitagiumFormset(request.POST, instance=litigant, prefix='capitagium')
        impercamentum_formset = forms.ImpercamentumFormset(request.POST, instance=litigant, prefix='impercamentum')
        land_formset = forms.LandFormset(request.POST, instance=litigant, prefix='land')
        if form.is_valid():
            litigant = form.save(commit=False)
            litigant.save()
            if amercement_formset.has_changed():
                if amercement_formset.is_valid():
                    amercement_formset.save()
            if fine_formset.has_changed():
                if fine_formset.is_valid():
                    fine_formset.save()
            if damage_formset.has_changed():
                if damage_formset.is_valid():
                    damage_formset.save()
            if heriot_formset.has_changed():
                if heriot_formset.is_valid():
                    heriot_formset.save()
            if capitagium_formset.has_changed():
                if capitagium_formset.is_valid():
                    capitagium_formset.save()
            if impercamentum_formset.has_changed():
                if impercamentum_formset.is_valid():
                    impercamentum_formset.save()
            if land_formset.has_changed():
                if land_formset.is_valid():
                    land_formset.save()
            data['form_is_valid'] = True
            litigant_list = models.Litigant.objects.filter(case=case_instance).prefetch_related('person') \
                .order_by('person__first_name', 'person__last_name')
            data['html_litigant_list'] = render_to_string('case/litigant_table_body_for_case.html',
                                                          {'litigant_list': litigant_list,
                                                           'case': case_instance}
                                                          )
        else:
            data['form_is_valid'] = False
    else:
        form = forms.LitigantForm(instance=litigant)
        amercement_formset = forms.AmercementFormset(instance=litigant, prefix='amercement')
        fine_formset = forms.FineFormset(instance=litigant, prefix='fine')
        damage_formset = forms.DamageFormset(instance=litigant, prefix='damage')
        heriot_formset = forms.HeriotFormset(instance=litigant, prefix='heriot')
        capitagium_formset = forms.CapitagiumFormset(instance=litigant, prefix='capitagium')
        impercamentum_formset = forms.ImpercamentumFormset(instance=litigant, prefix='impercamentum')
        land_formset = forms.LandFormset(instance=litigant, prefix='land')

    context = {
        'form': form,
        'litigant': litigant,
        'case': case_instance,
        'amercement_formset': amercement_formset,
        'fine_formset': fine_formset,
        'damage_formset': damage_formset,
        'heriot_formset': heriot_formset,
        'capitagium_formset': capitagium_formset,
        'impercamentum_formset': impercamentum_formset,
        'land_formset': land_formset,
    }
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
                    reverse('case:add') + "?session=" + session + "&case_type=" + case_type +
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


class LitigantListforAddCase(ListView):

    model = models.Litigant

    def get_queryset(self):
        return models.Litigant.objects.filter(case=self.kwargs['pk'])

class CaseDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Case
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('case:list')


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
        return reverse('county:detail', kwargs={'pk': pk})


class CountyAddView(GroupRequiredMixin, CreateView):

    model = models.County
    fields = ['name', 'abbreviation',]
    template_name = 'county/county_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('county:detail', args=(self.object.id,))


class CountyDeleteView(GroupRequiredMixin, DeleteView):

    model = models.County
    template_name = 'confirm_delete.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('county:list')


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
        return reverse('hundred:detail', kwargs={'pk': pk})



class HundredAddView(GroupRequiredMixin, CreateView):

    model = models.Hundred
    fields = ['name', 'county',]
    template_name = 'hundred/hundred_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('hundred:detail', args=(self.object.id,))

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
        return reverse('hundred:list')


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


def person_lists(request, pk):

    # Set up our data dictionary that will be passed through the JsonResponse
    data = dict()

    # get the last element of the requesting URL.
    path = request.path.split('/').pop()

    # Depending on the last element, assign the query
    if (path == 'case_list'):
        list = models.Litigant.objects.filter(person=pk).distinct().prefetch_related('case__session').order_by('case__session__date')
    elif (path == 'damage_list'):
        list = models.Litigant.objects.filter(person=pk, damages__damage__isnull=False).distinct().prefetch_related('case__session').order_by('case__session__date')
    elif (path == 'relationship_list'):
        list = models.Relationship.objects.filter(Q(person_one=pk) | Q(person_two=pk))

    # TODO: lists - amercement, capitagium, fine, heriot, impercamentum, land, pledge, position.

    # Check which page the url is on by getting the `?page=` param. If it is not 1, assign 1
    page = request.GET.get('page', 1)
    # Limit the list to 15 items.
    paginator = Paginator(list, 10)

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    template = 'person/' + path + '.html'

    # Need to assign person context for in-page links and data-urls, such as the pagination buttons.
    context={
        'list': list,
        'person': pk,
        'path': path,
    }

    data['html_list'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


class PersonDetailView(DetailView):

    model = models.Person
    queryset = models.Person.objects.all().annotate(amercement_count=Count('cases__amercement'),
                                                    amercement_max=Max('cases__amercement__in_denarius'),
                                                    amercement_min=Min('cases__amercement__in_denarius'),
                                                    amercement_avg=Avg('cases__amercement__in_denarius'),
                                                    amercement_sum=Sum('cases__amercement__in_denarius'),
                                                    fine_count=Count('cases__fine'),
                                                    fine_max=Max('cases__fine__in_denarius'),
                                                    fine_min=Min('cases__fine__in_denarius'),
                                                    fine_avg=Avg('cases__fine__in_denarius'),
                                                    fine_sum=Sum('cases__fine__in_denarius'),
                                                    damage_count=Count('cases__damage'),
                                                    damage_max=Max('cases__damage__in_denarius'),
                                                    damage_min=Min('cases__damage__in_denarius'),
                                                    damage_avg=Avg('cases__damage__in_denarius'),
                                                    damage_sum=Sum('cases__damage__in_denarius'),
                                                    chevage_count=Count('cases__chevage'),
                                                    chevage_max=Max('cases__chevage__in_denarius'),
                                                    chevage_min=Min('cases__chevage__in_denarius'),
                                                    chevage_avg=Avg('cases__chevage__in_denarius'),
                                                    chevage_sum=Sum('cases__chevage__in_denarius'),
                                                    heriot_count=Count('cases__heriot'),
                                                    heriot_max=Max('cases__heriot__in_denarius'),
                                                    heriot_min=Min('cases__heriot__in_denarius'),
                                                    heriot_avg=Avg('cases__heriot__in_denarius'),
                                                    heriot_sum=Sum('cases__heriot__in_denarius'),
                                                    impercamentum_count=Count('cases__impercamentum'),
                                                    impercamentum_max=Max('cases__impercamentum__in_denarius'),
                                                    impercamentum_min=Min('cases__impercamentum__in_denarius'),
                                                    impercamentum_avg=Avg('cases__impercamentum__in_denarius'),
                                                    impercamentum_sum=Sum('cases__impercamentum__in_denarius'))

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
        return reverse('session:detail', kwargs={'pk': pk})


class SessionAddView(GroupRequiredMixin, CreateView):

    model = models.Session
    fields = ['date', 'law_term', 'folio', 'record', 'village', 'notes']
    template_name = 'session/session_add.html'

    group_required = Add

    def get_success_url(self):
        referer = self.request.META.get('HTTP_REFERER', '/')
        return reverse('session:detail', args=(self.object.id,))

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
        return reverse('session:list')

    

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
    queryset = models.Person.objects.all().filter(cases__chevage__isnull=False).distinct()\
        .prefetch_related('cases__case__session','village').order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super(ChevageAnalysisListView, self).get_context_data(**kwargs)
        qs = context['object_list']
        village_id = self.kwargs.get('village_pk')
        chevage_list = qs.filter(cases__case__session__village=village_id).filter(cases__chevage__isnull=True)
        village =  models.Village.objects.get(id=village_id)
        context['chevage_list'] = chevage_list
        context['village'] = village
        context['page_title'] = 'Chevage'
        return context