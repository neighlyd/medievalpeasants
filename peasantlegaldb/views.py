from rest_framework import viewsets, generics
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from .serializers import *
from .models import *

# Create your views here.
class ArchiveViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    '''
        API endpoint that allows the model to be viewed or edited.
    '''
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer

class ArchiveListEndpoint(generics.ListAPIView):
    queryset = Archive.objects.all()
    serializer_class =  ArchiveSerializer


class MoneyViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = MoneySerializer


class ChattelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Chattel.objects.all().order_by('name')
    serializer_class = ChattelSerializer


class CaseTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = CaseType.objects.all().order_by('case_type')
    serializer_class = CaseTypeSerializer


class CountyViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = County.objects.all().order_by('name')
    serializer_class = CountySerializer


class LandViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Land.objects.all()
    serializer_class = LandSerializer


class ParcelTenureViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = ParcelTenure.objects.all().order_by('tenure')
    serializer_class = ParcelTenureSerializer


class ParcelTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = ParcelType.objects.all().order_by('parcel_type')
    serializer_class = ParcelTypeSerializer


class PositionTypeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = PositionType.objects.all().order_by('title')
    serializer_class = PositionTypeSerializer


class RelationViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Relation.objects.all().order_by('relation')
    serializer_class = RelationSerializer


class RoleViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('role')
    serializer_class = RoleSerializer


class VerdictViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Verdict.objects.all().order_by('verdict')
    serializer_class = VerdictSerializer


class HundredViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Hundred.objects.all().order_by('county__name', 'name')
    serializer_class = HundredSerializer


class VillageViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Village.objects.all().order_by('county__name', 'name')
    serializer_class = VillageSerializer


class PersonViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('village__name', 'last_name', 'first_name')
    serializer_class = PersonSerializer


class RecordViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Record.objects.all().order_by('archive__name', 'name')
    serializer_class = RecordSerializer


class SessionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Session.objects.all().order_by('village__name', 'record__record_type', 'date')
    serializer_class = SessionSerializer


class CaseViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Case.objects.all().prefetch_related('case_to_person').order_by('session__village__name', 'session__date', 'court_type').annotate(num_litigants=Count('case_to_person__person', distinct=True))
    serializer_class = CaseSerializer


class ChevageViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Chevage.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = ChevageSerializer


class CornbotViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = CornbotSerializer


class ExtrahuraViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = ExtrahuraSerializer


class HeriotViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Heriot.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = HeriotSerializer


class ImpercamentumViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Impercamentum.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = ImpercamentumSerializer


class MurrainViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = MurrainSerializer


class PlaceMentionedViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = PlaceMentioned.objects.all().order_by('case__session__village__name', 'case__session__date', 'village__name')
    serializer_class = PlaceMentionedSerializer


class LandParcelViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = LandParcelSerializer


class LitigantViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Litigant.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                             'person__first_name')
    serializer_class = LitigantSerializer


class CasePeopleLandViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = CasePeopleLand.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = CasePeopleLandSerializer


class PledgeViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Pledge.objects.all().order_by('case__session__village__name', 'case__session__date', 'pledge_giver__last_name',
                                              'pledge_giver__first_name')
    serializer_class = PledgeSerializer


class LandSplitViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = LandSplit.objects.all().order_by('old_land')
    serializer_class = LandSplitSerializer


class PositionViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Position.objects.all().order_by('person__village__name', 'person__last_name', 'person__first_name')
    serializer_class = PositionSerializer


class RelationshipViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Relationship.objects.all().order_by('person_one__last_name', 'person_one__first_name')
    serializer_class = Relationship