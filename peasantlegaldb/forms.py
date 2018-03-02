from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy

from . import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML, Field, Row, Button
from crispy_forms.bootstrap import StrictButton



class PersonFilterForm(forms.Form):
    select_village = forms.ChoiceField(
        label='Village',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'selector',
            }
        )
    )
    select_filter = forms.ChoiceField(
        label='Filter',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'selector',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(PersonFilterForm, self).__init__(*args, **kwargs)

        # set up a list of tuples as additional optionssasdfasdfwef.

        EXTRA_VILLAGE_CHOICES = [
            ('None', 'Select a Village'),
            ('None', '––––––––––––––––––––––––'),
            ('All', 'All Villages'),
            ('None', '––––––––––––––––––––––––'),
        ]

        FILTER_CHOICES = [
            ('None', 'Select a Filter'),
            ('None', '––––––––––––––––––––––––'),
            ('residents', 'Residents'),
            ('litigants', 'Litigants'),
            ('pledges_given', 'Pledge Givers'),
            ('pledges_received', 'Pledge Receivers'),
            ('amercement', 'Amerced'),
            ('fine', 'Fined'),
            ('damage', 'Damaged'),
            ('chevage', 'Capitagium'),
            ('impercamentum', 'Impercamenta'),
            ('heriot', 'Heriot'),
        ]

        # create a list of tuples for the choices by iterating through Village.objects.all.
        choices = [(vill.id, str(vill)) for vill in models.Village.objects.filter(person__isnull=False).order_by('name').distinct()]
        # add choices list of tuples to EXTRA_CHOICES. Make sure to put E_C before choices, as this establishes the
        # order of the list of tuples that will be displayed, thus putting 'All Villages' and 'No Villages' up top.
        choices = EXTRA_VILLAGE_CHOICES + choices
        self.fields['select_village'].choices = choices
        self.fields['select_filter'].choices = FILTER_CHOICES


class CaseFilterForm(forms.Form):
    # use reverse_lazy to get urls for ajax dropdowns to add as attributes to form fields. JQuery will pick these up on
    # change and use them to find the appropriately updated list.
    case_types_url = reverse_lazy('case:ajax_case_types')
    verdict_types_url = reverse_lazy('case:ajax_verdict_types')
    select_village = forms.ChoiceField(
        label='Village',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'selector',
                'data_case_types_url': case_types_url,
            }
        )
    )
    select_case_type = forms.ChoiceField(
        label='Case Filter',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'selector',
                'data_verdict_types_url': verdict_types_url,
            }
        )
    )
    select_verdict_type = forms.ChoiceField(
            label='Verdict Filter',
            choices=(),
            widget=forms.Select(
                attrs={
                    'class':'selector',
                }
            )
        )

    def __init__(self, *args, **kwargs):
        super(CaseFilterForm, self).__init__(*args, **kwargs)

        # Set initial case_type_queryset to none, because it will dynamically update using ajax after village has been
        # selected.
        village_queryset = models.Village.objects.filter(session__case__isnull=False).order_by('name').distinct()

        # set up a list of tuples as additional options
        CASE_TYPE_CHOICES = [
            ('All', 'All Case Types'),
            ('None', '––––––––––––––––––––––––'),
        ]

        EXTRA_VILLAGE_CHOICES = [
            ('None', 'Select a Village'),
            ('All', 'All Villages'),
            ('None', '––––––––––––––––––––––––'),
        ]

        VERDICT_CHOICES = [
            ('All', 'All Verdicts'),
            ('None', '––––––––––––––––––––––––'),
        ]

        # create a list of tuples for the choices by iterating through querysets
        village_choices = [(village.id, str(village)) for village in village_queryset]

        # add choices list of tuples to EXTRA_CHOICES. Make sure to put EXTRA_CHOICES before choices, as this
        # establishes the order of the list of tuples that will be displayed, thus putting 'All' and 'No' up top.
        additional_village_choices = EXTRA_VILLAGE_CHOICES + village_choices

        # assign the concatted choices to the form fields.
        self.fields['select_case_type'].choices = CASE_TYPE_CHOICES
        self.fields['select_village'].choices = additional_village_choices
        self.fields['select_verdict_type'].choices = VERDICT_CHOICES



class CaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # remove label for 'summary', to be replaced by "Notes" in Fieldset.
        self.fields['summary'].label = False
        # adjust size of summary field widget.
        self.fields['summary'].widget.attrs['rows'] = 15
        self.fields['summary'].widget.attrs['columns'] = 55
        # set form_tag to False to prevent crispy forms from auto-creating a <form> tag. This will allow us to add
        # multiple forms to a single template, though we need to manually add the <form> tag ourselves.
        self.helper.form_tag = False
        # Disable CSRF so that way Crispy forms doesn't create multiple CSRF tokens for each subform generated. Need to
        # manually add CSRF token generation to template.
        self.helper.disable_csrf = True
        self.helper.form_id = 'id-caseForm'
        self.helper.wrapper_class = 'form-row'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        self.helper.layout = Layout(
            'session',
            'court_type',
            'case_type',
            'verdict',
            'of_interest',
            'ad_legem',
            'villeinage_mention',
            'active_sale',
            'incidental_land',
            'summary',
            StrictButton('Save', name='add_single', css_class='btn btn-success'),
            StrictButton('Save and Add Another', name='add_another', css_class='btn btn-success'),
            StrictButton('Cancel', name='cancel', css_class='btn btn-danger'),
        )

    class Meta:
        model = models.Case
        fields = ['summary', 'session', 'court_type', 'case_type', 'verdict', 'of_interest', 'ad_legem',
                  'villeinage_mention', 'active_sale', 'incidental_land',]
        labels = {
            'case_type': _('Case Type'),
            'court_type': _('Court Type'),
            'of_interest': _('Of Interest'),
            'ad_legem': _('At Law'),
            'villeinage_mention': _('Villeinage'),
            'active_sale': _('Active Sale'),
            'incidental_land': _('Incidental Land'),
        }


class LitigantForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LitigantForm, self).__init__(*args, **kwargs)
        self.fields['person'].queryset = self.fields['person'].queryset.order_by('first_name', 'last_name', 'relation_name')
        self.fields['role'].queryset = self.fields['role'].queryset.order_by('role')

        self.helper = FormHelper()
        # disable form_tag so that way LitigantForm can nest within Case form. Need to manually add <form> tags to
        # template.
        self.helper.form_tag = False
        # Disable CSRF so that way Crispy forms doesn't create multiple CSRF tokens for each subform generated. Need to
        # manually add CSRF token generation to template.
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Div(
                Div(
                    'person',
                    css_class='col',
                ),
                Div(
                    'role',
                    css_class='col',
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'ad_proximum',
                    css_class='col',
                ),
                Div(
                    'attached',
                    css_class='col',
                ),
                Div(
                    'distrained',
                    css_class='col',
                ),
                Div(
                    'bail',
                    css_class='col',
                ),
                css_class='row',
            ),
        )

    class Meta:
        model = models.Litigant
        fields = ['person', 'role', 'ad_proximum', 'distrained', 'attached', 'bail']


class AmercementForm(forms.ModelForm):

    class Meta:
        model = models.Amercement
        fields = ['amercement']


class AmercementFormsetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(AmercementFormsetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.form_show_labels = False
        self.template = 'bootstrap/table_inline_formset.html'
        self.layout = Layout(
            'amercement',
        )

# inline formsets

AmercementFormset = inlineformset_factory(models.Litigant, models.Amercement,
                                          fields=('amercement',),
                                          extra=1, can_delete=True)

FineFormset = inlineformset_factory(models.Litigant, models.Fine,
                                    fields=('fine',),
                                    extra=1, can_delete=True)

DamageFormset = inlineformset_factory(models.Litigant, models.Damage,
                                      fields=('damage', 'notes'),
                                      extra=1, can_delete=True)

HeriotFormset = inlineformset_factory(models.Litigant, models.Heriot,
                                      fields=('quantity', 'animal', 'heriot'),
                                      extra=1, can_delete=True)

CapitagiumFormset = inlineformset_factory(models.Litigant, models.Capitagium,
                                          fields=('capitagium', 'notes', 'crossed', 'recessit', 'habet_terram',
                                                  'mortuus'),
                                          extra=1, can_delete=True)

ImpercamentumFormset = inlineformset_factory(models.Litigant, models.Impercamentum,
                                             fields=('quantity', 'animal', 'impercamentum', 'notes'),
                                             extra=1, can_delete=True)

LandFormset = inlineformset_factory(models.Litigant, models.LandtoCase,
                                    fields=('land', 'villeinage', 'notes'),
                                    extra=1, can_delete=True)