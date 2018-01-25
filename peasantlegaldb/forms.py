from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.models import inlineformset_factory

from . import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML, Field, Row, Button
from crispy_forms.bootstrap import StrictButton



class PersonFilterForm(forms.Form):
    village_selection = forms.ChoiceField(
        label='Village',
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

        EXTRA_CHOICES = [
            (None, 'Select a Village'),
            (None, '––––––––––––––––––––––––'),
            ('All', 'All Villages'),
            ('None', 'No Village'),
            (None, '––––––––––––––––––––––––'),
        ]

        # create a list of tuples for the choices by iterating through Village.objects.all.
        choices = [(vill.id, str(vill)) for vill in models.Village.objects.filter(person__isnull=False).order_by('name').distinct()]
        # add choices list of tuples to EXTRA_CHOICES. Make sure to put E_C before choices, as this establishes the
        # order of the list of tuples that will be displayed, thus putting 'All Villages' and 'No Villages' up top.
        choices = EXTRA_CHOICES + choices
        self.fields['village_selection'].choices = choices


class CaseFilterForm(forms.Form):
    case_selection = forms.ChoiceField(
        label='Case Type',
        choices=(),
        widget=forms.Select(
            attrs={
                'class':'selector',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(CaseFilterForm, self).__init__(*args, **kwargs)

        # set up a list of tuples as additional optionssasdfasdfwef.

        EXTRA_CHOICES = [
            (None, 'Select a Case Type'),
            ('All', 'All Case Types'),
            (None, '––––––––––––––––––––––––'),
        ]

        # create a list of tuples for the choices by iterating through Village.objects.all.
        choices = [(case_type.id, str(case_type)) for case_type in models.CaseType.objects.all().order_by('case_type')]
        # add choices list of tuples to EXTRA_CHOICES. Make sure to put E_C before choices, as this establishes the
        # order of the list of tuples that will be displayed, thus putting 'All Villages' and 'No Villages' up top.
        choices = EXTRA_CHOICES + choices
        self.fields['case_selection'].choices = choices


class CaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        #remove label for 'summary', to be replaced by "Notes" in Fieldset.
        self.fields['summary'].label = False
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.form_id = 'id-caseForm'
        self.helper.wrapper_class = 'form-row'
        self.helper.label_class = 'col-4'
        self.helper.field_class = 'col-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_case'
        # set form_tag to False to prevent crispy forms from auto-creating a <form> tag. This will allow us to add
        # multiple forms to a single template, though we need to manually add the <form> tag ourselves.
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'session',
            'court_type',
            'case_type',
            'verdict',
            Field('of_interest', css_class='pull-right'),
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
        fields = ['summary', 'session', 'case_type', 'court_type', 'verdict', 'of_interest', 'ad_legem',
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
        self.helper = FormHelper()
        self.form_method = 'post'
        # disable form_tag so that way LitigantForm can nest within Case form. Need to manually add <form> tags to
        # template.
        self.helper.form_tag = False
        # Disable CSRF so that way Crispy forms doesn't create multiple CSRF tokens for each subform generated. Need to
        # manually add CSRF token generation to template.
        self.helper.disable_csrf = True
        self.helper.form_show_labels = False
        self.helper.template = 'bootstrap/table_inline_formset.html'
        self.helper.layout = Layout(
            'person',
            'role',
            Field('DELETE'),
            Button('add_amercement', 'Add Amercement')
        )

    class Meta:
        model = models.Litigant
        fields = ['person', 'role']


# inlines
LitigantFormset = inlineformset_factory(models.Case, models.Litigant, form=LitigantForm, extra=0, can_delete=True)