from rest_flex_fields import FlexFieldsModelViewSet
from rest_framework import viewsets
from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from .serializers import *
from .models import *

# Create your views here.
class ArchiveViewSet(FlexFieldsModelViewSet):
    '''
        API endpoint that allows the model to be viewed or edited.
    '''
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class MoneyViewSet(FlexFieldsModelViewSet):
    queryset = Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = MoneySerializer


class ChattelViewSet(FlexFieldsModelViewSet):
    queryset = Chattel.objects.all().order_by('name')
    serializer_class = ChattelSerializer


class CaseTypeViewSet(FlexFieldsModelViewSet):
    queryset = CaseType.objects.all().order_by('case_type')
    serializer_class = CaseTypeSerializer


class CountyViewSet(FlexFieldsModelViewSet):
    queryset = County.objects.all().order_by('name')
    serializer_class = CountySerializer


class LandViewSet(FlexFieldsModelViewSet):
    queryset = Land.objects.all()
    serializer_class = LandSerializer


class ParcelTenureViewSet(FlexFieldsModelViewSet):
    queryset = ParcelTenure.objects.all().order_by('tenure')
    serializer_class = ParcelTenureSerializer


class ParcelTypeViewSet(FlexFieldsModelViewSet):
    queryset = ParcelType.objects.all().order_by('parcel_type')
    serializer_class = ParcelTypeSerializer


class PositionTypeViewSet(FlexFieldsModelViewSet):
    queryset = PositionType.objects.all().order_by('title')
    serializer_class = PositionTypeSerializer


class RelationViewSet(FlexFieldsModelViewSet):
    queryset = Relation.objects.all().order_by('relation')
    serializer_class = RelationSerializer


class RoleViewSet(FlexFieldsModelViewSet):
    queryset = Role.objects.all().order_by('role')
    serializer_class = RoleSerializer


class VerdictViewSet(FlexFieldsModelViewSet):
    queryset = Verdict.objects.all().order_by('verdict')
    serializer_class = VerdictSerializer


class HundredViewSet(FlexFieldsModelViewSet):
    queryset = Hundred.objects.all().order_by('county__name', 'name')
    serializer_class = HundredSerializer


class VillageViewSet(FlexFieldsModelViewSet):
    queryset = Village.objects.all().order_by('county__name', 'name')
    serializer_class = VillageSerializer


class PersonViewSet(FlexFieldsModelViewSet):
    queryset = Person.objects.all().order_by('village__name', 'last_name', 'first_name')
    serializer_class = PersonSerializer


class RecordViewSet(FlexFieldsModelViewSet):
    queryset = Record.objects.all().order_by('archive__name', 'name')
    serializer_class = RecordSerializer


class SessionViewSet(FlexFieldsModelViewSet):
    queryset = Session.objects.all().order_by('village__name', 'record__record_type', 'date')
    serializer_class = SessionSerializer


class CaseViewSet(SerializerExtensionsAPIViewMixin, viewsets.ModelViewSet):
    queryset = Case.objects.all().prefetch_related('litigants').order_by('session__village__name', 'session__date', 'court_type')
    #queryset = Case.objects.all().prefetch_related('litigants')
    serializer_class = CaseSerializer


class ChevageViewSet(FlexFieldsModelViewSet):
    queryset = Chevage.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = ChevageSerializer


class CornbotViewSet(FlexFieldsModelViewSet):
    queryset = Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = CornbotSerializer


class ExtrahuraViewSet(FlexFieldsModelViewSet):
    queryset = Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = ExtrahuraSerializer


class HeriotViewSet(FlexFieldsModelViewSet):
    queryset = Heriot.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = HeriotSerializer


class ImpercamentumViewSet(FlexFieldsModelViewSet):
    queryset = Impercamentum.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = ImpercamentumSerializer


class MurrainViewSet(FlexFieldsModelViewSet):
    queryset = Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')
    serializer_class = MurrainSerializer


class PlaceMentionedViewSet(FlexFieldsModelViewSet):
    queryset = PlaceMentioned.objects.all().order_by('case__session__village__name', 'case__session__date', 'village__name')
    serializer_class = PlaceMentionedSerializer


class LandParcelViewSet(FlexFieldsModelViewSet):
    queryset = LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = LandParcelSerializer


class LitigantViewSet(FlexFieldsModelViewSet):
    queryset = Litigant.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                             'person__first_name')
    serializer_class = LitigantSerializer


class CasePeopleLandViewSet(FlexFieldsModelViewSet):
    queryset = CasePeopleLand.objects.all().order_by('case__session__village__name', 'case__session__date', 'person__last_name',
                                              'person__first_name')
    serializer_class = CasePeopleLandSerializer


class PledgeViewSet(FlexFieldsModelViewSet):
    queryset = Pledge.objects.all().order_by('case__session__village__name', 'case__session__date', 'pledge_giver__last_name',
                                              'pledge_giver__first_name')
    serializer_class = PledgeSerializer


class LandSplitViewSet(FlexFieldsModelViewSet):
    queryset = LandSplit.objects.all().order_by('old_land')
    serializer_class = LandSplitSerializer


class PositionViewSet(FlexFieldsModelViewSet):
    queryset = Position.objects.all().order_by('person__village__name', 'person__last_name', 'person__first_name')
    serializer_class = PositionSerializer


class RelationshipViewSet(FlexFieldsModelViewSet):
    queryset = Relationship.objects.all().order_by('person_one__last_name', 'person_one__first_name')
    serializer_class = Relationship