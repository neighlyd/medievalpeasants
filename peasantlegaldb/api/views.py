from django.db.models import Count
from rest_framework import viewsets, generics
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin

from peasantlegaldb.api import serializers
from peasantlegaldb import models

# API views
class ArchiveViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    '''
        API endpoint that allows the model to be viewed or edited.
    '''
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

class ArchiveListEndpoint(generics.ListAPIView):
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
    queryset = models.Land.objects.all()
    serializer_class = serializers.LandSerializer


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
    queryset = models.Case.objects.all().prefetch_related('case_to_person').order_by('session__village__name', 'session__date', 'court_type')
    serializer_class = serializers.CaseSerializer



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
    queryset = models.PlaceMentioned.objects.all().order_by('case__session__village__name', 'case__session__date', 'village__name')
    serializer_class = serializers.PlaceMentionedSerializer


class LandParcelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(generics.ListAPIView):

    serializer_class = serializers.LitigantSerializer

    def get_queryset(self):
        queryset = models.Litigant.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                          'person__last_name',
                                                          'person__first_name')
        case = self.request.query_params.get('case', None)
        if case is not None:
            queryset = queryset.filter(case_id = case)
        return queryset

class CasePeopleLandViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.CasePeopleLand.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = serializers.CasePeopleLandSerializer


class PledgeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Pledge.objects.all().order_by('case__session__village__name', 'case__session__date', 'pledge_giver__last_name',
                                              'pledge_giver__first_name')
    serializer_class = serializers.PledgeSerializer


class LandSplitViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.LandSplit.objects.all().order_by('old_land')
    serializer_class = serializers.LandSplitSerializer


class PositionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Position.objects.all().order_by('person__village__name', 'person__last_name', 'person__first_name')
    serializer_class = serializers.PositionSerializer


class RelationshipViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = models.Relationship.objects.all().order_by('person_one__last_name', 'person_one__first_name')
    serializer_class = serializers.RelationshipSerializer