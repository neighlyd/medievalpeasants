from rest_framework import viewsets, generics

from dynamic_rest.viewsets import DynamicModelViewSet

from rest_framework.reverse import reverse

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
class ArchiveViewSet(DynamicModelViewSet):

    # API endpoint that allows the model to be viewed or edited.
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer

    def list(self, request, *args, **kwargs):
        return super(ArchiveViewSet, self).list(request, *args, **kwargs)


class ArchiveListEndpoint(DynamicModelViewSet):
    queryset = models.Archive.objects.all()
    serializer_class = serializers.ArchiveSerializer


class MoneyViewSet(DynamicModelViewSet):
    queryset = models.Money.objects.all().order_by('in_denarius', 'amount')
    serializer_class = serializers.MoneySerializer


class ChattelViewSet(DynamicModelViewSet):
    queryset = models.Chattel.objects.all().order_by('name')
    serializer_class = serializers.ChattelSerializer


class CaseTypeViewSet(DynamicModelViewSet):
    queryset = models.CaseType.objects.all().order_by('case_type')
    serializer_class = serializers.CaseTypeSerializer


class CountyViewSet(DynamicModelViewSet):
    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all().order_by('name')


class LandViewSet(DynamicModelViewSet):
    queryset = models.Land.objects.all()
    serializer_class = serializers.LandSerializer


class ParcelTenureViewSet(DynamicModelViewSet):
    queryset = models.ParcelTenure.objects.all().order_by('tenure')
    serializer_class = serializers.ParcelTenureSerializer


class ParcelTypeViewSet(DynamicModelViewSet):
    queryset = models.ParcelType.objects.all().order_by('parcel_type')
    serializer_class = serializers.ParcelTypeSerializer


class PositionTypeViewSet(DynamicModelViewSet):
    queryset = models.PositionType.objects.all().order_by('title')
    serializer_class = serializers.PositionTypeSerializer


class RelationViewSet(DynamicModelViewSet):
    queryset = models.Relation.objects.all().order_by('relation')
    serializer_class = serializers.RelationSerializer


class RoleViewSet(DynamicModelViewSet):
    queryset = models.Role.objects.all().order_by('role')
    serializer_class = serializers.RoleSerializer


class VerdictViewSet(DynamicModelViewSet):
    queryset = models.Verdict.objects.all().order_by('verdict')
    serializer_class = serializers.VerdictSerializer


class HundredViewSet(DynamicModelViewSet):
    serializer_class = serializers.HundredSerializer
    queryset = models.Hundred.objects.all()


class VillageViewSet(DynamicModelViewSet):
    serializer_class = serializers.VillageSerializer
    queryset = models.Village.objects.all().order_by('county__name', 'name')


class PersonViewSet(DynamicModelViewSet):
    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()


class RecordViewSet(DynamicModelViewSet):
    serializer_class = serializers.RecordSerializer
    queryset = models.Record.objects.all().order_by('archive__name', 'name')


class SessionViewSet(DynamicModelViewSet):
    serializer_class = serializers.SessionSerializer
    queryset = models.Session.objects.all().order_by('village__name', 'record__record_type', 'date')


class CaseViewSet(DynamicModelViewSet):
    serializer_class = serializers.CaseSerializer
    queryset = models.Case.objects.all().order_by('session__village__name', 'session__date', 'court_type')


class CornbotViewSet(DynamicModelViewSet):
    serializer_class = serializers.CornbotSerializer
    queryset = models.Cornbot.objects.all().order_by('case__session__village__name', 'case__session__date')


class ExtrahuraViewSet(DynamicModelViewSet):
    serializer_class = serializers.ExtrahuraSerializer
    queryset = models.Extrahura.objects.all().order_by('case__session__village__name', 'case__session__date')


class MurrainViewSet(DynamicModelViewSet):
    serializer_class = serializers.MurrainSerializer
    queryset = models.Murrain.objects.all().order_by('case__session__village__name', 'case__session__date')


class PlaceMentionedViewSet(DynamicModelViewSet):
    serializer_class = serializers.PlaceMentionedSerializer
    queryset = models.PlaceMentioned.objects.all()


class LandParcelViewSet(DynamicModelViewSet):
    queryset = models.LandParcel.objects.all().order_by('land', 'parcel_type__parcel_type')
    serializer_class = serializers.LandParcelSerializer


class LitigantViewSet(DynamicModelViewSet):
    serializer_class = serializers.LitigantSerializer
    queryset = models.Litigant.objects.all().prefetch_related('case', 'person')


class PledgeViewSet(DynamicModelViewSet):
    serializer_class = serializers.PledgeSerializer
    queryset = models.Pledge.objects.all().order_by('case__session__village__name', 'case__session__date',
                                                    'pledge_giver__last_name', 'pledge_giver__first_name')


class LandSplitViewSet(DynamicModelViewSet):
    serializer_class = serializers.LandSplitSerializer
    queryset = models.LandSplit.objects.all().order_by('old_land')


class PositionViewSet(DynamicModelViewSet):
    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()


class RelationshipViewSet(DynamicModelViewSet):
    serializer_class = serializers.RelationshipSerializer
    queryset = models.Relationship.objects.all().order_by('person_one__last_name', 'person_one__first_name')
