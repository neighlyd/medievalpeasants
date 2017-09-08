from rest_framework.serializers import ModelSerializer
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from rest_flex_fields import FlexFieldsModelSerializer
from .models import *

class ArchiveSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Archive
        fields = ('name', 'website', 'notes')


class MoneySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Money
        fields = ('amount', 'in_denarius')


class ChattelSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Chattel
        fields = ('name')


class CaseTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CaseType
        fields = ('case_type')


class CountySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = County
        fields = ('name', 'abbreviation')


class LandSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Land
        fields = ('id', 'notes', 'owner_chain')


class ParcelTenureSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ParcelTenure
        fields = ('tenure')


class ParcelTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ParcelType
        fields = ('parcel_type')


class PositionTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PositionType
        fields = ('title')


class RelationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Relation
        fields = ('relation')


class RoleSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Role
        fields = ('role')


class VerdictSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Verdict
        fields = ('verdict')


class HundredSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Hundred
        fields = ('id','name', 'county')
'''
    expandable_fields = {
        'county': (CountySerializer, {'source': 'county'})
    }
'''

class VillageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Village
        fields = ('id','name', 'latitude', 'longitude', 'hundred', 'county', 'ancient_demesne',
                  'great_rumor', 'notes')
'''
    expandable_fields = {
        'county': (CountySerializer, {'source': 'county'})
    }
'''

class CasePeopleLandSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = CasePeopleLand
        fields = ('person', 'case', 'land', 'role', 'villeinage', 'notes')


class LitigantSerializer(SerializerExtensionsMixin, ModelSerializer):

    class Meta:
        model = Litigant
        fields = ('id', 'person', 'case', 'role', 'fine', 'amercement', 'damage', 'damage_notes',
                  'ad_proximum', 'distrained', 'attached', 'bail')


class PersonSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = Person
        fields = ('id','first_name', 'relation_name', 'last_name', 'village', 'status', 'gender',
                  'tax_1332', 'tax_1379', 'notes')
'''
    expandable_fields ={
        }
'''

class CaseSerializer(SerializerExtensionsMixin, ModelSerializer):

    case_litigants = LitigantSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = ('id', 'summary', 'session', 'case_type', 'court_type', 'verdict', 'of_interest',
                  'ad_legem', 'villeinage_mention', 'active_sale', 'incidental_land', 'case_litigants')
'''
        expandable_fields = dict(
            litigants=dict(
                serializer=LitigantSerializer,
                many=True,
                read_only=True,
            )
        )
'''

class PledgeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Pledge
        fields = ('id', 'case', 'pledge_giver', 'pledge_receiver')
'''
    expandable_fields = {
        'case': (CaseSerializer, {'source': 'case'}),
    }
'''

class RecordSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class SessionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class ChevageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Chevage
        fields = '__all__'


class CornbotSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Cornbot
        fields = '__all__'


class ExtrahuraSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Extrahura
        fields = '__all__'


class HeriotSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Heriot
        fields = '__all__'


class ImpercamentumSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Impercamentum
        fields = '__all__'


class MurrainSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Murrain
        fields = '__all__'


class PlaceMentionedSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PlaceMentioned
        fields = '__all__'


class LandParcelSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = LandParcel
        fields = '__all__'


class LandSplitSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = LandSplit
        fields = '__all__'


class PositionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class RelationshipSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'

