from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.views.generic import ListView, TemplateView

from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.urls import reverse_lazy, reverse
from django.db.models import Count, Max, Min, Avg, Sum, Q, Case, When
from django.core.urlresolvers import resolve
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from braces.views import GroupRequiredMixin, AjaxResponseMixin

from . import models
from . import forms

import pdb

# TODO: Finish comparison of case/litigant/person btwn litigant table and amercements, damages, fines, impercamentum, landtocase
# TODO: Merge litigant btwn Litigant table and landtocase, fixing Role between the two.


Delete = [u"Full Editor"]
Edit = [u"Full Editor", u"Editor"]
Add = [u"Full Editor", u"Editor", u"Contributor"]

def nested_test(request):
    return render(request, 'case/_case_test.html')

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
    queryset = models.Case.objects.all().prefetch_related('litigants__person', 'litigants__amercements',
                                                          'litigants__capitagia', 'litigants__damages',
                                                          'litigants__fines', 'litigants__heriots',
                                                          'litigants__impercamenta', 'litigants__lands')\
        .order_by('litigants__person__last_name', 'litigants__person__first_name')\
        .annotate(amercement_count=Count('litigants__amercements'), cap_count=Count('litigants__capitagia'),
                  damage_count=Count('litigants__damages'), fine_count=Count('litigants__fines'),
                  heriot_count=Count('litigants__heriots'), imperc_count=Count('litigants__impercamenta'),
                  land_count=Count('litigants__lands'),
                  ad_proximum_count=Count(Case(When(litigants__ad_proximum=True, then=1))),
                  attached_count=Count(Case(When(litigants__attached=True, then=1))),
                  bail_count=Count(Case(When(litigants__bail=True, then=1))),
                  distrain_count=Count(Case(When(litigants__distrained=True, then=1))),
                  pledges_count=Count('litigants__pledges'))
    
    def get_context_data(self, **kwargs):
        context = super(CaseDetailView, self).get_context_data(**kwargs)
        lands = models.Land.objects.filter(tenants__litigant__case=self.object.id).distinct().order_by('tenants__litigant__case__session__date')
        context['page_title'] = 'Case'
        context['lands'] = lands
        return context


def CaseEditView(request, pk):

    case = get_object_or_404(models.Case, pk=pk)
    litigant_list = models.Litigant.objects.filter(case = case).prefetch_related('person')\
        .order_by('person__first_name', 'person__last_name')

    if request.method == 'POST':
        form = forms.CaseForm(request.POST, instance=case)
        form.save()
        if 'finish_editing' in request.POST:
            return redirect(reverse('case:detail', kwargs={"pk" : case.id}))
        elif 'add_another' in request.POST:
            return redirect(reverse('case:add'))
    else:
        form = forms.CaseForm(instance=case)

    context = {
        'case': case,
        'litigant_list': litigant_list,
        'form': form,
    }

    return render(request, 'case/case_edit.html', context)


# TODO: Convert add_litigant, delete_litigant, and edit_litigant to class based views and add in GroupRequiredMixin.

def add_litigant(request, pk):

    data = dict()
    # Get the appropriate case pk for the litigant to be assigned to.
    case_instance = get_object_or_404(models.Case, pk=pk)

    if request.method == "POST":
        form = forms.LitigantForm(request.POST)
        amercement_formset = forms.AmercementFormset(request.POST, prefix='amercement')
        capitagium_formset = forms.CapitagiumFormset(request.POST, prefix='capitagium')
        damage_formset = forms.DamageFormset(request.POST, prefix='damage')
        fine_formset = forms.FineFormset(request.POST, prefix='fine')
        heriot_formset = forms.HeriotFormset(request.POST, prefix='heriot')
        impercamentum_formset = forms.ImpercamentumFormset(request.POST, prefix='impercamentum')
        land_formset = forms.LandFormset(request.POST, prefix='land')
        pledge_formset = forms.PledgeFormset(request.POST, prefix='land')
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
                        new_land.save()
            if pledge_formset.has_changed():
                if pledge_formset.is_valid():
                    for form in pledge_formset:
                        new_pledge = form.save(commit=False)
                        new_pledge.litigant = new_litigant
                        new_pledge.save()
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
        capitagium_formset = forms.CapitagiumFormset(prefix='capitagium')
        damage_formset = forms.DamageFormset(prefix='damage')
        fine_formset = forms.FineFormset(prefix='fine')
        heriot_formset = forms.HeriotFormset(prefix='heriot')
        impercamentum_formset = forms.ImpercamentumFormset(prefix='impercamentum')
        land_formset = forms.LandFormset(prefix='land')
        pledge_formset = forms.PledgeFormset(prefix='pledge')

    context = {
        'form': form, 
        'case': case_instance,
        'amercement_formset': amercement_formset,
        'capitagium_formset': capitagium_formset,
        'damage_formset': damage_formset,
        'fine_formset': fine_formset,
        'heriot_formset': heriot_formset,
        'impercamentum_formset': impercamentum_formset,
        'land_formset': land_formset,
        'pledge_formset': pledge_formset,
    }

    # Before passing template and context along, render it as a string so that it can be serialized and sent as JSON data.
    data['html_form'] = render_to_string('case/_case_add_litigant_modal.html', context, request=request)

    return JsonResponse(data)

def delete_litigant(request, pk):
    litigant = get_object_or_404(models.Litigant, pk=pk)
    case_instance = litigant.case
    data = dict()
    if request.method == 'POST':
        litigant.delete()
        data['form_is_valid'] = True
        litigant_list = models.Litigant.objects.filter(case=case_instance).prefetch_related('person') \
            .order_by('person__first_name', 'person__last_name')
        data['html_litigant_list'] = render_to_string('case/litigant_table_body_for_case.html',
                                                      {'litigant_list': litigant_list,
                                                       'case': case_instance
                                                       }
                                                      )
    else:
        context = {'litigant': litigant}
        data['html_form'] = render_to_string('case/litigant_delete_confirm.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def edit_litigant(request, pk):
    # See add_litigant for comments.
    litigant = get_object_or_404(models.Litigant, pk=pk)
    case_instance = litigant.case

    data = dict()

    if request.method == 'POST':
        form = forms.LitigantForm(data=request.POST, instance=litigant)
        amercement_formset = forms.AmercementFormset(request.POST, instance=litigant, prefix='amercement')
        capitagium_formset = forms.CapitagiumFormset(request.POST, instance=litigant, prefix='capitagium')
        damage_formset = forms.DamageFormset(request.POST, instance=litigant, prefix='damage')
        fine_formset = forms.FineFormset(request.POST, instance=litigant, prefix='fine')
        heriot_formset = forms.HeriotFormset(request.POST, instance=litigant, prefix='heriot')
        impercamentum_formset = forms.ImpercamentumFormset(request.POST, instance=litigant, prefix='impercamentum')
        land_formset = forms.LandFormset(request.POST, instance=litigant, prefix='land')
        pledge_formset = forms.PledgeFormset(request.POST, instance=litigant, prefix='pledge')
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
            if pledge_formset.has_changed():
                if pledge_formset.is_valid():
                    pledge_formset.save()
            data['form_is_valid'] = True
            litigant_list = models.Litigant.objects.filter(case=case_instance).prefetch_related('person') \
                .order_by('person__first_name', 'person__last_name')
            data['html_litigant_list'] = render_to_string('case/litigant_table_body_for_case.html',
                                                          {'litigant_list': litigant_list,
                                                           'case': case_instance
                                                           }
                                                          )
        else:
            data['form_is_valid'] = False
    else:
        form = forms.LitigantForm(instance=litigant)
        amercement_formset = forms.AmercementFormset(instance=litigant, prefix='amercement')
        capitagium_formset = forms.CapitagiumFormset(instance=litigant, prefix='capitagium')
        damage_formset = forms.DamageFormset(instance=litigant, prefix='damage')
        fine_formset = forms.FineFormset(instance=litigant, prefix='fine')
        heriot_formset = forms.HeriotFormset(instance=litigant, prefix='heriot')
        impercamentum_formset = forms.ImpercamentumFormset(instance=litigant, prefix='impercamentum')
        land_formset = forms.LandFormset(instance=litigant, prefix='land')
        pledge_formset = forms.PledgeFormset(instance=litigant, prefix='pledge')

    context = {
        'form': form,
        'litigant': litigant,
        'case': case_instance,
        'amercement_formset': amercement_formset,
        'capitagium_formset': capitagium_formset,
        'damage_formset': damage_formset,
        'fine_formset': fine_formset,
        'heriot_formset': heriot_formset,
        'impercamentum_formset': impercamentum_formset,
        'land_formset': land_formset,
        'pledge_formset': pledge_formset,
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
                return redirect(reverse('case:edit', kwargs={"pk" : case.id }))
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

    person = models.Person.objects.get(id=pk)

    template = 'person/' + path + '.html'

    # Need to assign person context for in-page links and data-urls, such as the pagination buttons.
    context={
        'person': person,
    }

    data['html_list'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


def village_case_list(request, pk):

    data=dict()
    path = request.path.split('/').pop()
    village = models.Village.objects.get(id=pk)
    if path == 'case_list':
        query_list = models.Case.objects.filter(session__village=village).prefetch_related('session')\
            .order_by('session__date')

    page = request.GET.get('page', 1)
    paginator = Paginator(query_list, 10)

    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    template = 'village/' + path + '.html'

    context = {
        'list': query_list,
        'village': village,
    }

    data['html_list'] = render_to_string(template, context, request=request)

    return JsonResponse(data)


def case_lists(request, pk):

    # see person_lists for details on logic.
    data = dict()
    path = request.path.split('/').pop()
    case = models.Case.objects.get(id=pk)
    if path == 'litigant_list':
        query_list = models.Case.objects.filter(id=pk).prefetch_related('litigants__person', 'litigants__amercements',
                                                                        'litigants__capitagia', 'litigants__damages',
                                                                        'litigants__fines', 'litigants__heriots',
                                                                        'litigants__impercamenta', 'litigants__lands')\
            .order_by('litigants__person__last_name', 'litigants__person__first_name')\
            .annotate(amercement_count=Count('litigants__amercements'), cap_count=Count('litigants__capitagia'),
                      damage_count=Count('litigants__damages'), fine_count=Count('litigants__fines'),
                      heriot_count=Count('litigants__heriots'), imperc_count=Count('litigants__impercamenta'),
                      land_count=Count('litigants__lands'))

    page = request.GET.get('page', 1)
    paginator = Paginator(query_list, 10)

    try:
        query_list = paginator.page(page)
    except PageNotAnInteger:
        query_list = paginator.page(1)
    except EmptyPage:
        query_list = paginator.page(paginator.num_pages)

    template = 'case/' + path + '.html'

    context = {
        'list': query_list,
        'case': case,
    }

    data['html_list'] = render_to_string(template, context, request=request)

    return JsonResponse(data)


class PersonDetailView(DetailView):

    model = models.Person
    queryset = models.Person.objects.all().annotate(amercement_count=Count('cases__amercements'),
                                                    amercement_max=Max('cases__amercements__amercement__in_denarius'),
                                                    amercement_min=Min('cases__amercements__amercement__in_denarius'),
                                                    amercement_avg=Avg('cases__amercements__amercement__in_denarius'),
                                                    amercement_sum=Sum('cases__amercements__amercement__in_denarius'),
                                                    fine_count=Count('cases__fines'),
                                                    fine_max=Max('cases__fines__fine__in_denarius'),
                                                    fine_min=Min('cases__fines__fine__in_denarius'),
                                                    fine_avg=Avg('cases__fines__fine__in_denarius'),
                                                    fine_sum=Sum('cases__fines__fine__in_denarius'),
                                                    damage_count=Count('cases__damages'),
                                                    damage_max=Max('cases__damages__damage__in_denarius'),
                                                    damage_min=Min('cases__damages__damage__in_denarius'),
                                                    damage_avg=Avg('cases__damages__damage__in_denarius'),
                                                    damage_sum=Sum('cases__damages__damage__in_denarius'),
                                                    chevage_count=Count('cases__capitagia'),
                                                    chevage_max=Max('cases__capitagia__capitagium__in_denarius'),
                                                    chevage_min=Min('cases__capitagia__capitagium__in_denarius'),
                                                    chevage_avg=Avg('cases__capitagia__capitagium__in_denarius'),
                                                    chevage_sum=Sum('cases__capitagia__capitagium__in_denarius'),
                                                    heriot_count=Count('cases__heriots'),
                                                    heriot_max=Max('cases__heriots__heriot__in_denarius'),
                                                    heriot_min=Min('cases__heriots__heriot__in_denarius'),
                                                    heriot_avg=Avg('cases__heriots__heriot__in_denarius'),
                                                    heriot_sum=Sum('cases__heriots__heriot__in_denarius'),
                                                    impercamentum_count=Count('cases__impercamenta'),
                                                    impercamentum_max=Max('cases__impercamenta__impercamentum__in_denarius'),
                                                    impercamentum_min=Min('cases__impercamenta__impercamentum__in_denarius'),
                                                    impercamentum_avg=Avg('cases__impercamenta__impercamentum__in_denarius'),
                                                    impercamentum_sum=Sum('cases__impercamenta__impercamentum__in_denarius'))

    def get_context_data(self, **kwargs):
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Person'
        return context


class PersonAddView(GroupRequiredMixin, CreateView):

    model = models.Person
    form_class = forms.PersonForm
    template_name = 'person/person_add.html'

    group_required = Add


class PersonEditView(GroupRequiredMixin, UpdateView):

    model = models.Person
    form_class = forms.PersonForm
    template_name = 'person/person_edit.html'
    group_required = Edit


class PersonDeleteView(GroupRequiredMixin, DeleteView):

    model = models.Person
    template_name = 'person/person_delete_confirm.html'

    group_required = Delete

    def get_success_url(self):
        return reverse('person:list')


class SessionDetailView(DetailView):

    model = models.Session
    queryset = models.Session.objects.all().select_related('village')
    
    def get_context_data(self, **kwargs):
        context = super(SessionDetailView, self).get_context_data(**kwargs)
        context['page_title'] = 'Session'
        return context


def session_case_list(request, pk):
    data = dict()
    path = request.path.split('/').pop()
    queryset = models.Case.objects.filter(session_id=pk)

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    template = 'session/' + path + '.html'

    context = {
        'list': queryset,
    }

    data['html_list'] = render_to_string(template, context, request=request)

    return JsonResponse(data)


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


# class RelationshipAddView(GroupRequiredMixin, AjaxResponseMixin, CreateView):
#     model = models.Person
#     queryset = models.Relationship.objects.all().select_related('person_two', 'relationship')
#     template_name = 'person/add_relationship.html'
#     group_required = Edit
#     fields = ['person_two', 'relationship', 'confidence']
#
#     def get_ajax(self, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return render(self.request, self.template_name, context)
#

class RelationshipList(TemplateView):
    template_name = 'person/relationship_list.html'

    def get_context_data(self, **kwargs):
        context = super(RelationshipList, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


def RelationshipAddView(request, pk):

    data = dict()
    person_instance = get_object_or_404(models.Person, pk=pk)

    if request.method == 'POST':
        form = forms.AddRelationshipForm(request.POST)
        if form.is_valid():
            new_relationship = form.save(commit=False)
            new_relationship.person_one = person_instance
            new_relationship.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.AddRelationshipForm()

    context = {
        'form': form,
        'pk': pk,
    }
    data['html_form'] = render_to_string('person/add_relationship.html', context, request=request)

    return JsonResponse(data)


def RelationshipEditView(request, pk):

    data = dict()
    relationship_instance = get_object_or_404(models.Relationship, pk=pk)

    if request.method == 'POST':
        form = forms.EditRelationshipForm(data=request.POST, instance=relationship_instance)
        if form.is_valid():
            edit_relationship = form.save(commit=False)
            edit_relationship.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = forms.EditRelationshipForm(instance=relationship_instance)

    context = {
        'form': form,
        'pk': pk,
    }
    data['html_form'] = render_to_string('person/edit_relationship.html', context, request=request)

    return JsonResponse(data)


