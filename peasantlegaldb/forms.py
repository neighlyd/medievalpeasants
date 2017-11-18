from django import forms
from django.forms import BaseInlineFormSet
from . import models


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


class LitigantForm(BaseInlineFormSet):
