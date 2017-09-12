from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from .models import *


class ArchiveSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Archive
        fields = ('name', 'website', 'notes')


class MoneySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Money
        fields = ('amount', 'in_denarius')


class ChattelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Chattel
        fields = ('name',)


class CaseTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = CaseType
        fields = ('case_type',)


class CountySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ('name', 'abbreviation')


class LandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Land
        fields = ('id', 'notes', 'owner_chain')


class ParcelTenureSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = ParcelTenure
        fields = ('tenure',)


class ParcelTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = ParcelType
        fields = ('parcel_type',)


class PositionTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = PositionType
        fields = ('title',)


class RelationSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Relation
        fields = ('relation',)


class RoleSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('role',)


class VerdictSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Verdict
        fields = ('verdict',)


class HundredSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Hundred
        fields = ('id', 'name', 'county')


class VillageSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Village
        fields = ('id','name', 'latitude', 'longitude', 'hundred', 'county', 'ancient_demesne',
                  'great_rumor', 'notes')


class CasePeopleLandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):


    class Meta:
        model = CasePeopleLand
        fields = ('person', 'case', 'land', 'role', 'villeinage', 'notes')


class LitigantSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Litigant
        fields = ('id', 'person', 'case', 'role', 'fine', 'amercement', 'damage', 'damage_notes',
                  'ad_proximum', 'distrained', 'attached', 'bail')


class PersonSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('id','first_name', 'relation_name', 'last_name', 'village', 'status', 'gender',
                  'tax_1332', 'tax_1379', 'notes')


class CaseSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    litigant_count = serializers.ReadOnlyField()

    class Meta:
        model = Case
        fields = ('id', 'summary', 'session', 'case_type', 'court_type', 'verdict', 'of_interest',
                  'ad_legem', 'villeinage_mention', 'active_sale', 'incidental_land','litigant_count')

        expandable_fields = dict(
                case_to_person=dict(
                    serializer=LitigantSerializer,
                    many=True,
                    id_source=Litigant.pk,),
                litigants=dict(
                    serializer=PersonSerializer,
                    many=True,
                    read_only=True,
                ),
        )


class PledgeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Pledge
        fields = ('id', 'case', 'pledge_giver', 'pledge_receiver')


class RecordSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = Record
        fields = '__all__'


class SessionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class ChevageSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Chevage
        fields = '__all__'


class CornbotSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Cornbot
        fields = '__all__'


class ExtrahuraSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Extrahura
        fields = '__all__'


class HeriotSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Heriot
        fields = '__all__'


class ImpercamentumSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Impercamentum
        fields = '__all__'


class MurrainSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Murrain
        fields = '__all__'


class PlaceMentionedSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = PlaceMentioned
        fields = '__all__'


class LandParcelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = LandParcel
        fields = '__all__'


class LandSplitSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = LandSplit
        fields = '__all__'


class PositionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class RelationshipSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'

