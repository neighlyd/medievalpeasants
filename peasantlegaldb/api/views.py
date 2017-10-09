from rest_framework import viewsets, generics
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from peasantlegaldb.api import serializers
from peasantlegaldb import models


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
    queryset = models.County.objects.all().order_by('name')
    serializer_class = serializers.CountySerializer


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
    queryset = models.Hundred.objects.all().order_by('county__name', 'name')
    serializer_class = serializers.HundredSerializer


class VillageViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Village.objects.all().order_by('county__name', 'name')
    serializer_class = serializers.VillageSerializer


class PersonViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Person.objects.all().order_by('village__name', 'last_name', 'first_name')
    serializer_class = serializers.PersonSerializer


class RecordViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Record.objects.all().order_by('archive__name', 'name')
    serializer_class = serializers.RecordSerializer


class SessionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Session.objects.all().order_by('village__name', 'record__record_type', 'date')
    serializer_class = serializers.SessionSerializer


class CaseViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    serializer_class = serializers.CaseSerializer

    def get_queryset(self):
        queryset = models.Case.objects.all().order_by('session__village__name', 'session__date', 'court_type')
        land = self.request.query_params.get('land', None)
        if land is not None:
            queryset = models.Land.objects.get(id=land).case_set.all().distinct()

        return queryset


class CornbotViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = serializers.CornbotSerializer


class ExtrahuraViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = serializers.ExtrahuraSerializer


class MurrainViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = serializers.MurrainSerializer


class PlaceMentionedViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.PlaceMentioned.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                            'village__name')
    serializer_class = serializers.PlaceMentionedSerializer


class LandParcelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    serializer_class = serializers.LitigantSerializer

    def get_queryset(self):
        queryset = models.Litigant.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                          'person__last_name',
                                                          'person__first_name')

        case = self.request.query_params.get('case', None)
        if case is not None:
            queryset = queryset.filter(case_id=case)

        person = self.request.query_params.get('person', None)
        if person is not None:
            queryset = queryset.filter(person_id=person)

        return queryset


class CasePeopleLandViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):

    serializer_class = serializers.CasePeopleLandSerializer

    def get_queryset(self):
        queryset = models.CasePeopleLand.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                            'person__last_name', 'person__first_name')

        person = self.request.query_params.get('person', None)
        if person is not None:
            queryset = queryset.filter(person=person)

        land = self.request.query_params.get('land', None)
        if land is not None:
            queryset = queryset.filter(land=land)

        case = self.request.query_params.get('case', None)
        if case is not None:
            queryset = queryset.filter(case=case)

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
