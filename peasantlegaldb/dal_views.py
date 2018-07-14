from django.db.models import Q

from dal import autocomplete

from . import models

class PersonAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Person.objects.all().select_related('village')

        if self.q:
            qs = qs.filter(Q(full_name__icontains=self.q) | Q(village__name__istartswith=self.q))
        return qs


class VillageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = models.Village.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs