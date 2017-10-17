from rest_framework import viewsets, generics
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from django_filters import rest_framework as filters
import django_filters

from peasantlegaldb.api import serializers
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
class ArchiveViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    # API endpoint that allows the model to be viewed or edited.
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer


class ArchiveListEndpoint(SerializerExtensionsAPIViewMixin, generics.ListAPIView):
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer


class MoneyViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = serializers.MoneySerializer


class ChattelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Chattel.objects.all().order_by('name')
    serializer_class = serializers.ChattelSerializer


class CaseTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.CaseType.objects.all().order_by('case_type')
    serializer_class = serializers.CaseTypeSerializer


class CountyViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CountySerializer

    def get_queryset(self):
        queryset = models.County.objects.all().order_by('name')

        chain_filter={}
        chain_filter['id'] = self.request.query_params.get('county', None)
        queryset = check_chain(chain_filter, queryset)

        return queryset


class LandViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.LandSerializer

    def get_queryset(self):
        queryset = models.Land.objects.all()

        # get case param from url, then if it is not empty get instance of case object and extract value list of each
        # distinct land associated with it. Afterwards, iterate through this queryset, ignoring blanks, and append each
        # element to a list. Set the Land queryset filter to include all items in list. __in= is the syntax used to
        # include all items in a filter - see:
        #   https://stackoverflow.com/questions/36851257/general-way-of-filtering-by-ids-with-drf
        # An alternative approach using dictionaries instead of lists is included here (perhaps could be used with
        # .value instead of .values_list if necessary):
        #   https://stackoverflow.com/questions/14258338/django-rest-framework-filtering
        case = self.request.query_params.get('case', None)
        if case is not None:
            case_instance = models.Case.objects.get(id=case)
            sub_queryset = case_instance.case_to_person.all().values_list('land_id', flat=True).distinct()
            land_list = []
            for x in sub_queryset:
                if x is not None:
                    land_list.append(x)
            queryset = queryset.filter(id__in=land_list)
        return queryset




class ParcelTenureViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.ParcelTenure.objects.all().order_by('tenure')
    serializer_class = serializers.ParcelTenureSerializer


class ParcelTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.ParcelType.objects.all().order_by('parcel_type')
    serializer_class = serializers.ParcelTypeSerializer


class PositionTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.PositionType.objects.all().order_by('title')
    serializer_class = serializers.PositionTypeSerializer


class RelationViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Relation.objects.all().order_by('relation')
    serializer_class = serializers.RelationSerializer


class RoleViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('role')
    serializer_class = serializers.RoleSerializer


class VerdictViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Verdict.objects.all().order_by('verdict')
    serializer_class = serializers.VerdictSerializer


class HundredViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.HundredSerializer

    def get_queryset(self):
        queryset = models.Hundred.objects.all()

        chain_filter = {}
        chain_filter['county_id'] = self.request.query_params.get('county', None)
        distinct = self.request.query_params.get('distinct', None)

        if distinct == "true":
            queryset = check_chain(chain_filter, queryset, distinct=True)
        queryset = check_chain(chain_filter, queryset)

        return queryset


class VillageViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.VillageSerializer

    def get_queryset(self):
        queryset = models.Village.objects.all().order_by('county__name', 'name')

        chain_filter = {}
        chain_filter['id'] = self.request.query_params.get('village', None)
        chain_filter['county_id'] = self.request.query_params.get('county', None)
        chain_filter['hundred_id'] = self.request.query_params.get('hundred', None)
        distinct = self.request.query_params.get('distinct', None)

        if distinct == "true":
            queryset = check_chain(chain_filter, queryset, distinct=True)
        queryset = check_chain(chain_filter, queryset)

        return queryset



class PersonViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.PersonSerializer

    def get_queryset(self):
        queryset = models.Person.objects.all()

        chain_filter = {}
        chain_filter['id'] = self.request.query_params.get('person', None)
        chain_filter['village_id'] = self.request.query_params.get('village', None)
        chain_filter['village__county_id'] = self.request.query_params.get('county', None)
        chain_filter['village__hundred_id'] = self.request.query_params.get('hundred', None)
        chain_filter['person_to_case__case__session__village_id'] = self.request.query_params.get('village_to_litigant', None)
        chain_filter['person_to_case__case__session__village__county_id'] = self.request.query_params.get('county_to_litigant', None)
        chain_filter['person_to_case__case__session__village__hundred_id'] = self.request.query_params.get('hundred_to_litigant', None)
        distinct = self.request.query_params.get('distinct', None)

        if distinct == "true":
            queryset = check_chain(chain_filter, queryset, distinct=True)
        queryset = check_chain(chain_filter, queryset)

        return queryset

class RecordViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.RecordSerializer

    def get_queryset(self):
        queryset = models.Record.objects.all().order_by('archive__name', 'name')

        chain_filter = {}
        chain_filter['id'] = self.request.query_params.get('record', None)
        chain_filter['archive_id'] = self.request.query_params.get('archive', None)
        queryset = check_chain(chain_filter, queryset)

        return queryset

class SessionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.SessionSerializer

    def get_queryset(self):
        queryset = models.Session.objects.all().order_by('village__name', 'record__record_type', 'date')

        chain_filter = {}
        chain_filter['record_id'] = self.request.query_params.get('record', None)
        chain_filter['id'] = self.request.query_params.get('id', None)
        queryset=check_chain(chain_filter, queryset)

        return queryset


class CaseViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        queryset = models.Case.objects.all().order_by('session__village__name', 'session__date', 'court_type')

        chain_filter = {}
        chain_filter['case_to_person__land_id'] = self.request.query_params.get('land', None)
        chain_filter['id'] = self.request.query_params.get('case', None)
        chain_filter['session_id'] = self.request.query_params.get('session', None)
        chain_filter['session__village_id'] = self.request.query_params.get('village', None)
        chain_filter['case_to_person__person_id'] = self.request.query_params.get('person', None)
        chain_filter['session__village__county_id'] = self.request.query_params.get('county', None)
        chain_filter['session__village__hundred_id'] = self.request.query_params.get('hundred', None)
        distinct = self.request.query_params.get('distinct', None)

        if distinct == "true":
            queryset = check_chain(chain_filter, queryset, distinct=True)
        else:
            queryset = check_chain(chain_filter, queryset)

        return queryset


class CornbotViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.CornbotSerializer

    def get_queryset(self):
        queryset = models.Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')

        chain_filter = {}
        chain_filter['case_id'] = self.request.query_params.get('case', None)
        chain_filter['crop_type_id'] = self.request.query_params.get('crop', None)
        chain_filter['price_id'] = self.request.query_params.get('price', None)
        queryset = check_chain(chain_filter, queryset)

        return queryset


class ExtrahuraViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.ExtrahuraSerializer

    def get_queryset(self):
        queryset = models.Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')

        chain_filter={}
        chain_filter['case_id']=self.request.query_params.get('case', None)
        chain_filter['animal_id']=self.request.query_params.get('animal', None)
        chain_filter['price_id']=self.request.query_params.get('price', None)
        queryset=check_chain(chain_filter, queryset)

        return queryset



class MurrainViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.MurrainSerializer

    def get_queryset(self):
        queryset = models.Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')

        chain_filter={}
        chain_filter['case_id']=self.request.query_params.get('case', None)
        chain_filter['animal_id']=self.request.query_params.get('animal', None)
        queryset=check_chain(chain_filter, queryset)

        return queryset


class PlaceMentionedViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.PlaceMentionedSerializer

    def get_queryset(self):
        queryset = models.PlaceMentioned.objects.all()

        chain_filter={}
        chain_filter['village_id'] = self.request.query_params.get('village', None)
        chain_filter['case_id'] = self.request.query_params.get('case', None)
        queryset = check_chain(chain_filter, queryset)

        return queryset


class LandParcelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer





class LitigantViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    serializer_class = serializers.LitigantSerializer

    def get_queryset(self):
        queryset = models.Litigant.objects.all().prefetch_related('case', 'person')

        chain_filter = {}
        chain_filter['case_id'] = self.request.query_params.get('case', None)
        chain_filter['person_id'] = self.request.query_params.get('person', None)
        chain_filter['land_id'] = self.request.query_params.get('land', None)
        chain_filter['amercement'] = self.request.query_params.get('amercement', None)
        chain_filter['fine'] = self.request.query_params.get('fine', None)
        chain_filter['damage'] = self.request.query_params.get('damage', None)
        chain_filter['impercamentum'] = self.request.query_params.get('impercamentum', None)
        chain_filter['heriot']= self.request.query_params.get('heriot', None)
        chain_filter['chevage'] = self.request.query_params.get('chevage', None)
        distinct = self.request.query_params.get('distinct', None)

        if distinct == "true":
            queryset = check_chain(chain_filter, queryset, distinct=True)
        queryset = check_chain(chain_filter, queryset)

        return queryset


class PledgeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.PledgeSerializer

    def get_queryset(self):
        queryset = models.Pledge.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                    'pledge_giver__last_name', 'pledge_giver__first_name')

        giver = self.request.query_params.get('giver', None)
        if giver is not None:
            queryset = queryset.filter(pledge_giver=giver)

        receiver = self.request.query_params.get('receiver', None)
        if receiver is not None:
            queryset = queryset.filter(pledge_receiver=receiver)

        return queryset

class LandSplitViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.LandSplitSerializer

    def get_queryset(self):
        queryset = models.LandSplit.objects.all().order_by('old_land')
        land = self.request.query_params.get('land', None)
        if land is not None:
            queryset = queryset.filter(new_land_id=land) | queryset.filter(old_land_id=land)

        return queryset


class PositionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.PositionSerializer

    def get_queryset(self):
        queryset = models.Position.objects.all()

        person = self.request.query_params.get('person', None)
        if person is not None:
            queryset = queryset.filter(person_id=person)

        return queryset


class RelationshipViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    serializer_class = serializers.RelationshipSerializer

    def get_queryset(self):
        queryset = models.Relationship.objects.all().order_by('person_one__last_name', 'person_one__first_name')

        person = self.request.query_params.get('person', None)
        if person is not None:
            queryset = queryset.filter(person_one=person) | queryset.filter(person_two=person)

        return queryset
