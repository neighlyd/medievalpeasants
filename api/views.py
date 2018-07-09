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
class ChainFilterQueryMixin(object):

    def _get_chain_params(self, chain):
        for key, value in chain.items():
            chain[key]['field'] = value['field'].replace('.', '__')
            chain[key]['search'] = self.request.query_params.get(key)
        return chain

    def _get_distinct_params(self):
        distinct_param = self.request.query_params.get('distinct', None)
        if distinct_param is not None:
            if distinct_param == 'false' or distinct_param == 'False':
                distinct = False
            elif distinct_param == 'true' or distinct_param == 'True':
                distinct = True
        else:
            try:
                distinct = self.chain_filter_distinct
            except:
                distinct = True
        return distinct

    def _filter_chain(self, queryset, chain):
        filtered_chain = self._get_chain_params(chain)
        distinct = self._get_distinct_params()
        for key, value in filtered_chain.items():
            if value['search'] is not None:
                # query_params are strings. Convert to python boolean objects.
                if value['search'] == 'true' or value['search'] == 'True':
                    search_val = True
                elif value['search'] == 'false' or value['search'] == 'False':
                    search_val = False
                else:
                    search_val = value['search']
                if 'type' in value:
                    # I prefer to search for isnull using opposite true/false tests (e.g. are there fines?). Sue me.
                    if value['type'] == 'isnull':
                        if value['search'] == 'true' or value['search'] == 'True':
                            new_filter = value['field'] + '__isnull'
                            queryset = queryset.filter(**{new_filter: False})
                        elif value['search'] == 'false' or value['search'] == 'False':
                            new_filter = value['field'] + '__isnull'
                            queryset = queryset.filter(**{new_filter: True})
                    else:
                        continue
                else:
                    queryset = queryset.filter(**{value['field']: search_val})
        # import ipdb
        # ipdb.set_trace()
        if distinct == True:
            return queryset.distinct()
        else:
            return queryset

    def get_queryset(self):
        queryset = super(ChainFilterQueryMixin, self).get_queryset()
        try:
            chain = self.chain
            return self._filter_chain(queryset, chain)
        except:
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


class CountyViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all().order_by('name')


class LandViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['tenants', 'tenants.role', 'tenants.litigant', 'tenants.litigant.person',
                           'tenants.litigant.case']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Land.objects.all().prefetch_related('tenants__litigant__case', 'parcels')
    serializer_class = serializers.LandSerializer
    chain = {
        'case': {'field': 'tenants.litigant.case'},
        'village': {'field': 'tenants.litigant.case.session.village'},
    }

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

    permit_list_expands = ['county']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.HundredSerializer
    queryset = models.Hundred.objects.all().select_related('county')


class VillageViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['hundred', 'county', ]

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all()\
        .select_related('county', 'hundred')\
        .prefetch_related('person_set')\
        .order_by('county__name', 'name')
    chain = {
        'village': {'field': 'name'},
    }


class PersonViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['village', 'earliest_case', 'latest_case']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all().select_related(
        'village',
        'earliest_case__session__village',
        'latest_case__session__village').order_by('first_name', 'last_name')
    chain = {
        'county_to_litigant': {'field': 'cases.case.session.village.county'},
        'county_to_resident': {'field': 'village.county'},
        'village_to_resident': {'field': 'village'},
        'village_to_litigant': {'field': 'cases.case.session.village'},
        'hundred_to_litigant': {'field': 'cases.case.session.village.hundred'},
        'hundred': {'field': 'village.hundred'},
        'session': {'field': 'cases.case.session'},
        'amerced': {'field': 'cases.amercements', 'type': 'isnull'},
        'capitagia': {'field': 'cases.capitagia', 'type': 'isnull'},
        'damaged': {'field': 'cases.damages', 'type': 'isnull'},
        'fined': {'field': 'cases.fines', 'type': 'isnull'},
        'heriot': {'field': 'cases.heriots', 'type': 'isnull'},
        'impercamenta':{'field': 'cases.impercamenta', 'type': 'isnull'},
        'lands': {'field': 'cases.lands', 'type': 'isnull'},
        'pledges_given': {'field': 'pledge_giver', 'type': 'isnull'},
        'pledges_received': {'field': 'cases.pledges', 'type': 'isnull'},
        'case': {'field': 'cases.case'},
    }


class RecordViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['sessions', 'archive']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.RecordSerializer
    queryset = models.Record.objects.all().select_related('archive').order_by('archive__name', 'name')
    chain = {
        'archive': {'field': 'archive'}
    }


class SessionViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['village', 'record']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all()\
        .select_related('village', 'record')\
        .order_by('village__name', 'record__record_type', 'date')
    chain = {
        'village': {'field': 'village'},
        'record': {'field': 'record'},
        'archive': {'field': 'record.archive'},
    }


class CaseViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['session', 'session.village', 'litigants']
    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects.all()\
        .select_related('session__village', 'case_type', 'verdict')\
        .prefetch_related('litigants', 'litigants__pledges')
    chain = {
        'session': {'field': 'session'},
        'record': {'field': 'session.record'},
        'archive': {'field': 'session.record.archive'},
        'village': {'field': 'session.village'},
        'hundred': {'field': 'session.village.hundred'},
        'county': {'field': 'session.village.county'},
        'land': {'field': 'litigants.lands'},
        'case_type': {'field': 'case_type'},
        'verdict': {'field': 'verdict'},
        'litigant': {'field': 'litigants.in'},
        'pledge_receiver': {'field': 'cases.pledges'} ,
    }


class CornbotViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['crop_type', 'price']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.CornbotSerializer
    queryset = models.Cornbot.objects.all()\
        .select_related('case__session__village')\
        .order_by('case__session__village__name', 'case__session__date')
    chain = {
        'case': {'field': 'case'},
    }


class ExtrahuraViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):
    permit_list_expands = ['animal', 'price']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.ExtrahuraSerializer
    queryset = models.Extrahura.objects.all()\
        .select_related('case__session__village')\
        .order_by('case__session__village__name', 'case__session__date')
    chain = {
        'case': {'field': 'case'},
    }


class MurrainViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['animal']
    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.MurrainSerializer
    queryset = models.Murrain.objects.all()\
        .select_related('case__session__village')\
        .order_by('case__session__village__name', 'case__session__date')
    chain = {
        'case': {'field': 'case'},
    }


class PlaceMentionedViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['village', 'case']
    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PlaceMentionedSerializer
    queryset = models.PlaceMentioned.objects.all()\
        .select_related('village', 'case__session__village')\
        .order_by('village')
    chain = {
        'village': {'field': 'village'},
        'related_to': {'field': 'case.session.village'},
        'case': {'field': 'case', 'select_related': 'case'},
        'ancient_demesne': {'field': 'village.ancient_demesne'},
        'great_rumor': {'field': 'village.great_rumor'},
    }


class LandParcelViewSet(FlexFieldsModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.LandParcel.objects.all().select_related('parcel_type').order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):
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
    queryset = models.Litigant.objects.all()\
        .select_related('person', 'case')\
        .order_by('person__first_name', 'person__last_name')
    chain = {
        'litigant': {'field': 'person'},
        'case': {'field': 'case'},
        'amercements': {'field': 'amercements', 'type': 'isnull'},
        'damages': {'field': 'damages', 'type': 'isnull'},
        'capitagia': {'field': 'capitagia', 'type': 'isnull'},
        'fines': {'field': 'fines', 'type': 'isnull'},
        'heriots': {'field': 'heriots', 'type': 'isnull'},
        'impercamenta': {'field': 'impercamenta', 'type': 'isnull'},
        'lands': {'field': 'lands', 'type': 'isnull'},
        'pledges': {'field': 'pledges', 'type': 'isnull'},
    }


class PledgeViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):

    permit_list_expands = ['giver', 'receiver', 'receiver.case', 'receiver.person']
    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = serializers.PledgeSerializer
    queryset = models.Pledge.objects.all()\
        .select_related('giver','receiver__case', 'receiver__person')\
        .order_by('giver__last_name', 'giver__first_name')
    chain = {
        'giver': {'field': 'giver'},
        'receiver': {'field': 'receiver.person'},
        'case': {'field': 'receiver.case'},
    }


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


class PositionViewSet(ChainFilterQueryMixin, FlexFieldsModelViewSet):
    permit_list_expands = ['session']

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all().prefetch_related('session')
    chain = {
        'person': {'field': 'person'}
    }


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