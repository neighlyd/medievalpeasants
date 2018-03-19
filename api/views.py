from django.db.models import Q
from dynamic_rest.viewsets import DynamicModelViewSet
from rest_framework import permissions

from api import serializers
from peasantlegaldb import models


# Function created in order to be able to search for both isnull and FKs. In order to work, you need to create a
# dictionary of key, value pairs using self.request.query_params.get(x, None) where the key is the name of the field you
# want to filter and x is the query_param you want to use in the URL (see the get_queryset function in the
# LitigantViewset class for examples). Pass this dictionary and the ViewSet's queryset to check_chain(), which will
# iterate through the dictionary, checking to see if there is a value or not. If there is, it checks to see if it should
# treat it as a boolean check or not ("true" or "false"), or whether it is a filter check. It then filters the queryset
# based on that, and returns the queryset to the ViewSet class. Again, see the LitigantViewSet for example.
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

    if distinct == True:
        queryset = queryset.distinct()

    return queryset


# API views
class ArchiveViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # API endpoint that allows the model to be viewed or edited.
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    def list(self, request, *args, **kwargs):
        return super(ArchiveViewSet, self).list(request, *args, **kwargs)


class MoneyViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = serializers.MoneySerializer


class ChattelViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Chattel.objects.all().order_by('name')
    serializer_class = serializers.ChattelSerializer


class CaseTypeViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.CaseType.objects.all().order_by('case_type')
    serializer_class = serializers.CaseTypeSerializer


class CountyViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all().order_by('name')


class LandViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Land.objects.all()
    serializer_class = serializers.LandSerializer

    def get_queryset(self, *args, **kwargs):

        # get case param from url, then if it is not empty get instance of case object and extract value list of each
        # distinct land associated with it. Afterwards, iterate through this queryset, ignoring blanks, and append each
        # element to a list. Set the Land queryset filter to include all items in list. __in= is the syntax used to
        # include all items in a filter - see:
        #   https://stackoverflow.com/questions/36851257/general-way-of-filtering-by-ids-with-drf
        # An alternative approach using dictionaries instead of lists is included here (perhaps could be used with
        # .value instead of .values_list if necessary):
        #   https://stackoverflow.com/questions/14258338/django-rest-framework-filtering

        case = self.request.query_params.get('case')
        if not case:
            return models.Land.objects.all()
        else:
            case_instance = models.Case.objects.get(id=case)
            sub_queryset = case_instance.case_to_person.all().values_list('land_id', flat=True).distinct()
            land_list=[]
            for x in sub_queryset:
                if x is not None:
                    land_list.append(x)
            return models.Land.objects.filter(id__in=land_list)

class ParcelTenureViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.ParcelTenure.objects.all().order_by('tenure')
    serializer_class = serializers.ParcelTenureSerializer


class ParcelTypeViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.ParcelType.objects.all().order_by('parcel_type')
    serializer_class = serializers.ParcelTypeSerializer


class PositionTypeViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.PositionType.objects.all().order_by('title')
    serializer_class = serializers.PositionTypeSerializer


class RelationViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Relation.objects.all().order_by('relation')
    serializer_class = serializers.RelationSerializer


class RoleViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Role.objects.all().order_by('role')
    serializer_class = serializers.RoleSerializer


class VerdictViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.Verdict.objects.all().order_by('verdict')
    serializer_class = serializers.VerdictSerializer


class HundredViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.HundredSerializer
    queryset = models.Hundred.objects.all()


class VillageViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all().order_by('county__name', 'name')


class PersonViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PersonSerializer

    def get_queryset(self, queryset=models.Person.objects.all().select_related('village')):
        chain_filter = {}
        chain_filter['cases__case__session__village__county_id'] = self.request.query_params.get('county_to_litigant')
        chain_filter['village__county_id'] = self.request.query_params.get('county_to_resident')
        chain_filter['cases__case__session__village_id'] = self.request.query_params.get('village_to_litigant')
        chain_filter['cases__case__session__village__hundred_id'] = self.request.query_params.get('hundred_to_litigant')
        chain_filter['village__hundred_id'] = self.request.query_params.get('hundred')
        chain_filter['cases__chevage'] = self.request.query_params.get('chevage')
        chain_filter['cases__impercamentum'] = self.request.query_params.get('impercamentum')
        chain_filter['cases__amercement'] = self.request.query_params.get('amercement')
        chain_filter['cases__fine'] = self.request.query_params.get('fine')
        chain_filter['cases__heriot'] = self.request.query_params.get('heriot')
        chain_filter['cases__damage'] = self.request.query_params.get('damage')
        chain_filter['pledge_giver'] = self.request.query_params.get('pledges_given')
        chain_filter['cases__pledges'] = self.request.query_params.get('pledges_received')
        
        if not chain_filter:
            return queryset
        else:
            queryset = check_chain(chain_filter, queryset)
            return queryset


class RecordViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.RecordSerializer
    queryset = models.Record.objects.all().order_by('archive__name', 'name')


class SessionViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all().order_by('village__name', 'record__record_type', 'date')

    def get_queryset(self, queryset=models.Session.objects.all()):
        chain_filter = {}
        chain_filter['village'] = self.request.query_params.get('village')

        distinct = self.request.query_params.get('distinct')

        if not chain_filter:
            return queryset
        else:
            if distinct == "true":
                queryset = check_chain(chain_filter, queryset, True)
            else:
                queryset = check_chain(chain_filter, queryset, False)
            return queryset


class CaseViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CaseSerializer

    def get_queryset(self, queryset=models.Case.objects.all()):
        chain_filter={}
        chain_filter['session__village_id'] = self.request.query_params.get('village')
        chain_filter['session__village__hundred_id'] = self.request.query_params.get('hundred')
        chain_filter['session__village__county_id'] = self.request.query_params.get('county')
        chain_filter['litigants__land_id'] = self.request.query_params.get('land')
        chain_filter['case_type'] = self.request.query_params.get('case_type')
        chain_filter['verdict'] = self.request.query_params.get('verdict')
        distinct = self.request.query_params.get('distinct')

        if not chain_filter:
            return queryset
        else:
            if distinct == "true":
                queryset = check_chain(chain_filter, queryset, True)
            else:
                queryset = check_chain(chain_filter, queryset)
            return queryset


class CornbotViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.CornbotSerializer
    queryset = models.Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')


class ExtrahuraViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.ExtrahuraSerializer
    queryset = models.Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')


class MurrainViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.MurrainSerializer
    queryset = models.Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')


class PlaceMentionedViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PlaceMentionedSerializer
    queryset = models.PlaceMentioned.objects.all()

    def get_queryset(self, queryset=models.PlaceMentioned.objects.all()):
        chain_filter={}
        chain_filter['village_id'] = self.request.query_params.get('village')
        chain_filter['case__session__village_id'] = self.request.query_params.get('related_to')
        if not chain_filter:
            return queryset
        else:
            queryset = check_chain(chain_filter, queryset)
            return queryset


class LandParcelViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.LitigantSerializer
    queryset = models.Litigant.objects.all()


class PledgeViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PledgeSerializer
    queryset = models.Pledge.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                    'pledge_giver__last_name', 'pledge_giver__first_name')


class LandSplitViewSet(DynamicModelViewSet):

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


class PositionViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()


class RelationshipViewSet(DynamicModelViewSet):

    # Must be logged in to edit
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    serializer_class = serializers.RelationshipSerializer

    def get_queryset(self, *args, **kwargs):
        relations = self.request.query_params.get('relations')
        if not relations:
             return models.Relationship.objects.all()
        else:
            return models.Relationship.objects.filter(Q(person_one=relations) | Q(person_two=relations))