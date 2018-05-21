from django.db.models import Q

from dynamic_rest.viewsets import DynamicModelViewSet

from rest_flex_fields import FlexFieldsModelViewSet

from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from api import serializers
from peasantlegaldb import models


# Function created in order to be able to search for both isnull and FKs. In order to work, you need to create a
# dictionary of key, value pairs using self.request.query_params.get(x, None) where the key is the name of the field you
# want to filter and x is the query_param you want to use in the URL (see the get_queryset function in the
# LitigantViewset class for examples). Pass this dictionary and the ViewSet's queryset to check_chain(), which will
# iterate through the dictionary, checking to see if there is a value or not. If there is, it checks to see if it should
# treat it as a boolean check or not ("true" or "false"), or whether it is a filter check. It then filters the queryset
# based on that, and returns the queryset to the ViewSet class. Again, see the LitigantViewSet for example.
class ChainFilterMixin(object):

    def _get_params(self, chain):
        filter_params = dict()
        for key, value in chain.items():
            filter_params[key.replace('.', '__')] = self.request.query_params.get(value)
        return filter_params

    def filter_chain(self, queryset, chain=False, distinct=False):
        if chain:
            chain = self._get_params(chain)
            for key, value in chain.items():
                if value is not None:
                    if value == "true":
                        new_filter = key + "__isnull"
                        queryset = queryset.filter(**{new_filter: False})
                    elif value == "false":
                        new_filter = key + "__isnull"
                        queryset = queryset.filter(**{new_filter: True})
                    else:
                        queryset = queryset.filter(**{key: value})

        if 'distinct' in self.request.GET:
            distinct = self.request.query_params.get('distinct')
            if distinct == 'true' or distinct == 'True':
                distinct = True
        else:
            distinct = distinct
        if distinct:
            return queryset.distinct()
        else:
            return queryset


def check_chain(check, queryset, distinct=False):
    for key, value in check.items():
        if value is not None:
            if value == "true":
                new_filter = key + "__isnull"
                queryset = queryset.filter(**{new_filter: False})
            elif value == "false":
                new_filter = key + "__isnull"
                queryset = queryset.filter(**{new_filter:True})
            else:
                queryset = queryset.filter(**{key:value})
    return queryset


# API views
class ArchiveViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # API endpoint that allows the model to be viewed or edited.
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    def list(self, request, *args, **kwargs):
        return super(ArchiveViewSet, self).list(request, *args, **kwargs)


class MoneyViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = serializers.MoneySerializer


class ChattelViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Chattel.objects.all().order_by('name')
    serializer_class = serializers.ChattelSerializer


class CaseTypeViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.CaseType.objects.all().order_by('case_type')
    serializer_class = serializers.CaseTypeSerializer


class CountyViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all().order_by('name')


class LandViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['tenants', 'tenants.role', 'tenants.litigant', 'tenants.litigant.person',
                           'tenants.litigant.case']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Land.objects.all()
    serializer_class = serializers.LandSerializer

    def get_queryset(self, queryset=models.Land.objects.all()):
        chain = {
            'tenants__litigant__case': 'case'
        }
        return self.filter_chain(queryset, chain, distinct=True)

class ParcelTenureViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.ParcelTenure.objects.all().order_by('tenure')
    serializer_class = serializers.ParcelTenureSerializer


class ParcelTypeViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.ParcelType.objects.all().order_by('parcel_type')
    serializer_class = serializers.ParcelTypeSerializer


class PositionTypeViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.PositionType.objects.all().order_by('title')
    serializer_class = serializers.PositionTypeSerializer


class RelationViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Relation.objects.all().order_by('relation')
    serializer_class = serializers.RelationSerializer


class RoleViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Role.objects.all().order_by('role')
    serializer_class = serializers.RoleSerializer


class VerdictViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Verdict.objects.all().order_by('verdict')
    serializer_class = serializers.VerdictSerializer


class HundredViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.HundredSerializer
    queryset = models.Hundred.objects.all()


class VillageViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all().prefetch_related('person_set').order_by('county__name', 'name')


class PersonViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['village', 'earliest_case', 'latest_case']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PersonSerializer

    def get_queryset(self, queryset=models.Person.objects.all().select_related('village',
                                                                               'earliest_case__session__village',
                                                                               'latest_case__session__village')):
        chain = {
            'cases.case.session.village.county': 'county_to_litigant',
            'village.county': 'county_to_resident',
            'village': 'village_to_resident',
            'cases.case.session.village': 'village_to_litigant',
            'cases.case.session.village.hundred': 'hundred_to_litigant',
            'village.hundred': 'hundred',
            'cases.case.session': 'session',
            'cases.amercements': 'amercements',
            'cases.capitagia': 'capitagia',
            'cases.damages': 'damages',
            'cases.fines': 'fines',
            'cases.heriots': 'heriots',
            'cases.impercamenta': 'impercamenta',
            'cases.lands': 'lands',
            'pledge_giver': 'pledges_given',
            'cases.pledges': 'pledges_received',
        }
        return self.filter_chain(queryset, chain, distinct=True)


class RecordViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.RecordSerializer
    queryset = models.Record.objects.all().order_by('archive__name', 'name')

    def get_queryset(self, queryset = models.Record.objects.all().order_by('archive__name', 'name')):
        chain = {
            'archive': 'archive'
        }
        return self.filter_chain(queryset, chain)


class SessionViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['village', 'record']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all().order_by('village__name', 'record__record_type', 'date')\
        .prefetch_related('village', 'record')

    def get_queryset(self, queryset=models.Session.objects.all().prefetch_related('village', 'record')):
        chain = {
            'village': 'village',
            'record': 'record',
            'record.archive': 'archive',
        }
        return self.filter_chain(queryset, chain, distinct=True)


class CaseViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['session', 'session.village', 'litigants']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CaseSerializer

    def get_queryset(self, queryset=models.Case.objects.all().select_related('session__village', 'case_type', 'verdict')
                     .prefetch_related('litigants', 'litigants__pledges')):
        chain = {
            'session': 'session',
            'session.record': 'record',
            'session.record.archive': 'archive',
            'session.village': 'village',
            'session.village.hundred': 'hundred',
            'session.village.county': 'county',
            'litigants.lands': 'land',
            'case_type': 'case_type',
            'verdict': 'verdict',
            'litigants.in': 'litigant',
            'cases.pledges': 'pledge_receiver',
        }
        return self.filter_chain(queryset, chain, distinct=True)


class CornbotViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CornbotSerializer
    queryset = models.Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')


class ExtrahuraViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.ExtrahuraSerializer
    queryset = models.Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')


class MurrainViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.MurrainSerializer
    queryset = models.Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')


class PlaceMentionedViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PlaceMentionedSerializer
    queryset = models.PlaceMentioned.objects.all().prefetch_related('village')

    def get_queryset(self, queryset=models.PlaceMentioned.objects.all().prefetch_related('village')):
        chain = {
        'village': 'village',
        'case.session.village': 'related_to',
        }
        return self.filter_chain(queryset, chain, distinct=True)


class LandParcelViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(ChainFilterMixin, FlexFieldsModelViewSet):
    permit_list_expands = ['amercements', 'amercements.amercement',
                           'capitagia', 'capitagia.capitagium',
                           'damages', 'damages.damage',
                           'fines', 'fines.fine',
                           'heriots', 'heriots.animal',
                           'impercamenta', 'impercamenta.impercamentum', 'impercamenta.animal',
                           'lands',
                           'case', 'role',
                           'pledges', 'pledges.giver',
                           'person', 'person.village']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.LitigantSerializer

    def get_queryset(self, queryset = models.Litigant.objects.all().prefetch_related('person', 'case')):
        chain = {
            'person': 'litigant',
            'case': 'case',
            'amercements': 'amercements',
            'damages': 'damages',
            'capitagia': 'capitagia',
            'fines': 'fines',
            'heriots': 'heriots',
            'impercamenta': 'impercamenta',
            'lands': 'lands',
            'pledges': 'pledges',
        }
        return self.filter_chain(queryset, chain)


class PledgeViewSet(ChainFilterMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['giver', 'receiver', 'receiver.case', 'receiver.person']
    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PledgeSerializer

    def get_queryset(self, queryset = models.Pledge.objects.all()
                     .order_by('giver__last_name', 'giver__first_name')):
        chain = {
            'giver': 'giver',
            'receiver.person': 'receiver'
        }
        return self.filter_chain(queryset, chain)



class LandSplitViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.LandSplitSerializer

    def get_queryset(self, queryset=models.LandSplit.objects.all()):
        land = self.request.query_params.get('land')
        if not land:
            return queryset
        else:
            queryset = queryset.filter(Q(new_land_id=land) | Q(old_land_id=land))
            return queryset


class PositionViewSet(ChainFilterMixin, FlexFieldsModelViewSet):
    permit_list_expands = ['session']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()

    def get_queryset(self, queryset = models.Position.objects.all().prefetch_related('session')):
        chain = {
            'person': 'person'
        }
        return self.filter_chain(queryset, chain)


class RelationshipViewSet(FlexFieldsModelViewSet):
    permit_list_expands = ['person_one', 'person_two']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.RelationshipSerializer

    def get_queryset(self, *args, **kwargs):
        relations = self.request.query_params.get('relations')
        if not relations:
             return models.Relationship.objects.all()
        else:
            return models.Relationship.objects.filter(Q(person_one=relations) | Q(person_two=relations))