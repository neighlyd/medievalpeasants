from django.db.models import Count, Max, Min, Avg, Sum

from rest_framework import serializers

from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

from dynamic_rest.serializers import DynamicModelSerializer, DynamicEphemeralSerializer
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField

from peasantlegaldb import models


# Normalized tables section
class ParcelTenureSerializer(DynamicModelSerializer):

    class Meta:
        model = models.ParcelTenure
        name = 'parcel tenure'
        fields = ('id', 'tenure',)


class ParcelTypeSerializer(DynamicModelSerializer):

    class Meta:
        model = models.ParcelType
        name = 'parcel type'
        fields = ('id', 'parcel_type',)


class PositionTypeSerializer(DynamicModelSerializer):

    class Meta:
        model = models.PositionType
        name = 'position title'
        fields = ('id', 'title',)


class RelationSerializer(DynamicModelSerializer):

    class Meta:
        model = models.Relation
        name = 'relation title'
        fields = ('id', 'relation',)


class RoleSerializer(DynamicModelSerializer):

    class Meta:
        model = models.Role
        name = 'role'
        fields = ('id', 'role',)


class VerdictSerializer(DynamicModelSerializer):

    class Meta:
        model = models.Verdict
        name = 'verdict'
        fields = ('id', 'verdict',)


class MoneySerializer(DynamicModelSerializer):

    class Meta:
        model = models.Money
        name = 'money'
        fields = ('id', 'amount', 'in_denarius')


class ChattelSerializer(DynamicModelSerializer):

    class Meta:
        model = models.Chattel
        name = 'chattel'
        fields = ('id', 'name',)


class CaseTypeSerializer(DynamicModelSerializer):

    class Meta:
        model = models.CaseType
        name = 'case type'
        fields = ('id', 'case_type',)


# Begin Data-Entry tables

class ArchiveSerializer(DynamicModelSerializer):

    counts = DynamicMethodField(
        requires = [
            'record_set__session_set__case'
        ]
    )

    class Meta:
        model = models.Archive
        name = 'archive'
        fields = ('id', 'name', 'website', 'notes', 'counts')

    def get_counts(self, record):
        counts = {}
        counts['record'] = record.record_count
        counts['session'] = record.session_count
        counts['case'] = record.case_count
        return counts

    def get_record_count(self, record):
        return record.record_count

    def get_session_count(self, record):
        return record.session_count

    def get_case_count(self, record):
        return record.case_count


class RecordSerializer(DynamicModelSerializer):

    record_type = serializers.SerializerMethodField()
    archive = DynamicRelationField('ArchiveSerializer', deferred=True)
    sessions = DynamicRelationField('SessionSerializer', source='session_set', many=True, deferred=True)
    counts = DynamicMethodField(
        requires = [
            'session_set__case'
        ]
    )

    class Meta:
        model = models.Record
        fields = ('id', 'name', 'record_type', 'reel', 'notes', 'counts', 'archive', 'sessions')

    def get_counts(self, record):
        counts = {}
        counts['earliest_session'] = record.earliest_session_info
        counts['latest_session'] = record.latest_session_info
        counts['case'] = record.case_count
        counts['session'] = record.session_count
        return counts

    def get_record_type(self, record):
        return record.get_record_type_display()


class CountySerializer(DynamicModelSerializer):

    counts = DynamicMethodField(
        requires = [
            'village_set__session_set__case', 'village_set__person'
        ]
    )

    class Meta:
        model = models.County
        fields = ('id', 'name', 'abbreviation', 'counts')

    def get_counts(self, record):
        counts = {}
        counts['hundred'] = record.hundred_count
        counts['village']= record.village_count
        counts['great_rumor'] = record.great_rumor_count
        counts['ancient_demesne'] = record.ancient_demesne_count
        counts['session']= record.session_count
        counts['case'] = record.case_count
        counts['resident'] = record.resident_count
        counts['litigant'] = record.litigant_count
        return counts


class HundredSerializer(DynamicModelSerializer):

    county = DynamicRelationField('CountySerializer')
    counts = DynamicMethodField(
        requires = [
            'village'
        ]
    )

    class Meta:
        model = models.Hundred
        fields = ('id', 'name', 'counts', 'county')

    def get_counts(self, record):
        counts={}
        counts['village'] = record.village_count
        return counts


class VillageSerializer(DynamicModelSerializer):

    hundred = DynamicRelationField('HundredSerializer', deferred=True)
    county = DynamicRelationField('CountySerializer', deferred=True)
    counts = DynamicMethodField(
        requires = [
            'person'
        ]
    )

    class Meta:
        model = models.Village
        fields = ('id', 'name', 'latitude', 'longitude', 'ancient_demesne', 'great_rumor', 'notes', 'counts', 'county',
                  'hundred')

    def get_counts(self, record):
        counts = {}
        counts['case'] = record.case_count
        counts['resident'] = record.resident_count
        counts['litigant']= record.litigant_count
        counts['session']= record.session_count
        return counts



class SessionSerializer(DynamicModelSerializer):

    law_term = serializers.SerializerMethodField()
    year = serializers.ReadOnlyField()
    human_date = serializers.ReadOnlyField()
    village = DynamicRelationField('VillageSerializer', deferred=True, embed=True)
    record = DynamicRelationField('RecordSerializer', deferred=True)
    counts = DynamicMethodField(
        requires = [
            'cases',
        ]
    )

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year', 'human_date', 'village', 'record', 'counts')

    def get_counts(self, record):
        counts = {}
        counts['case'] = record.case_count
        counts['litigant'] = record.litigant_count
        counts['land_case'] = record.land_case_count
        counts['chevage_case'] = record.chevage_case_count
        counts['impercamentum_case_count'] = record.impercamentum_case_count
        return counts

    def get_law_term(self, record):
        return record.get_law_term_display()


class PersonSerializer(DynamicModelSerializer):

    # Use ReadOnlyField to pull in model functions:
    # https://stackoverflow.com/questions/24233988/django-serializer-method-field
    full_name = serializers.ReadOnlyField()
    gender = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    counts = DynamicMethodField(
        requires = [
            'person_to_case__case__session', 'pledge_giver', 'pledge_receiver', 'position', 'relationship_person_one',
            'relationship_person_two', 'case_set'
        ],
        deferred=True
    )
    village = DynamicRelationField('VillageSerializer', embed=True, deferred=True)

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'relation_name', 'last_name', 'status', 'gender', 'tax_1332', 'tax_1379', 'notes',
                  'full_name', 'counts', 'village')

    def get_gender(self, record):
        return record.get_gender_display()

    def get_status(self, record):
        return record.get_status_display()

    def get_counts(self, record):
        counts = {}

        pledge_counts = {}
        pledge_counts['given'] = record.pledges_given_count
        pledge_counts['received'] = record.pledges_received_count

        counts['pledge'] = pledge_counts
        counts['monetary'] = record.monetary_counts
        counts['relationship'] = record.relationship_count
        counts['position'] = record.position_count
        counts['litigation'] = record.case_count_litigation
        counts['all_cases'] = record.case_count_all
        counts['earliest_case'] = record.earliest_case
        counts['latest_case'] = record.latest_case
        return counts


class LandSerializer(DynamicModelSerializer):

    def get_tenant_history(field):
        # return queryset of litigants associated with particular land.
        return models.Person.objects.filter(person_to_case__land_id=field.id)

    parcel_list = DynamicMethodField(
        requires = [
            'parcels__parcel_type', 'parcels__parcel_tenure'
        ]
    )
    case_info = DynamicMethodField(
        requires = [
            'case_to_land__case__session'
        ]
    )
    tenant_history = DynamicRelationField(
        'LitigantSerializer', source='case_to_land' ,many=True, deferred=True, embed=True,
    )

    class Meta:
        model = models.Land
        name = 'land'
        fields = ('id', 'notes', 'parcel_list', 'case_info', 'tenant_history')
        deferred_fields = ('tenant_history', 'case_info')

    def get_parcel_list(self, record):
        return record.parcel_list

    def get_case_info(self, record):
        case_info={}
        case_info['earliest'] = record.earliest_case
        case_info['latest'] = record.latest_case

        return case_info


class CaseSerializer(DynamicModelSerializer):

    litigant_count = serializers.ReadOnlyField()
    court_type = serializers.SerializerMethodField()
    litigant_list = serializers.ReadOnlyField()

    session = DynamicRelationField('SessionSerializer', embed=True)
    case_type = DynamicRelationField('CaseTypeSerializer', embed=True)
    verdict = DynamicRelationField('VerdictSerializer', embed=True)
    litigants = DynamicRelationField('LitigantSerializer', many=True, embed=True, deferred=True)

    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'court_type', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale',
                  'incidental_land', 'litigant_count', 'litigant_list', 'session', 'case_type', 'verdict', 'litigants')

    def get_court_type(self, obj):
        return obj.get_court_type_display()


class LitigantSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    person = DynamicRelationField('PersonSerializer', deferred=True, embed=True)
    land = DynamicRelationField('LandSerializer', deferred=True, embed=True)
    role = DynamicRelationField('RoleSerializer', embed=True)
    fine = DynamicRelationField('MoneySerializer', embed=True)
    amercement = DynamicRelationField('MoneySerializer', embed=True)
    damage = DynamicRelationField('MoneySerializer', embed=True)
    chevage = DynamicRelationField('MoneySerializer', embed=True)
    heriot = DynamicRelationField('MoneySerializer', embed=True)
    heriot_animal = DynamicRelationField('ChattelSerializer', embed=True)
    impercamentum = DynamicRelationField('MoneySerializer', embed=True)
    impercamentum_animal = DynamicRelationField('ChattelSerializer', embed=True)

    class Meta:
        model = models.Litigant
        fields = ('id', 'damage_notes', 'ad_proximum', 'distrained', 'attached', 'bail', 'chevage', 'crossed',
                  'recessit', 'habet_terram', 'chevage_notes', 'heriot_quantity', 'impercamentum_quantity',
                  'impercamentum_notes', 'amercement', 'fine', 'damage', 'chevage', 'heriot_animal', 'heriot',
                  'impercamentum_animal', 'impercamentum', 'land_notes', 'land_villeinage', 'land', 'person', 'case',
                  'role',)


class PledgeSerializer(DynamicModelSerializer):

    pledge_giver = DynamicRelationField('PersonSerializer', embed=True)
    pledge_receiver = DynamicRelationField('PersonSerializer', embed=True)
    case = DynamicRelationField('CaseSerializer', embed=True)

    class Meta:
        model = models.Pledge
        fields = ('id', 'pledge_giver', 'pledge_receiver', 'case')


class CornbotSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', embed=True)
    crop_type = DynamicRelationField('CropTypeSerializer', embed=True)
    price = DynamicRelationField('MoneySerializer', embed=True)

    class Meta:
        model = models.Cornbot
        fields = ('id', 'amount', 'notes', 'case', 'crop_type', 'price')


class ExtrahuraSerializer(DynamicModelSerializer):

    animal = DynamicRelationField('ChattelSerializer', embed=True)
    price = DynamicRelationField('MoneySerializer', embed=True)
    case = DynamicRelationField('CaseSerializer', embed=True)

    class Meta:
        model = models.Extrahura
        fields = ('id', 'amount', 'animal', 'price', 'case')


class MurrainSerializer(DynamicModelSerializer):

    animal = DynamicRelationField('ChattelSerializer', embed=True)
    case = DynamicRelationField('CaseSerializer', embed=True)

    class Meta:
        model = models.Murrain
        fields = ('id', 'amount', 'notes', 'animal', 'case')


class PlaceMentionedSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', embed=True)
    village = DynamicRelationField('VillageSerializer', embed=True)

    class Meta:
        model = models.PlaceMentioned
        fields = ('id', 'notes', 'case', 'village')


class LandParcelSerializer(DynamicModelSerializer):

    parcel_type = DynamicRelationField('ParcelTypeSerializer', embed=True)
    parcel_tenure = DynamicRelationField('ParcelTenureSerializer', embed=True)

    class Meta:
        model = models.LandParcel
        fields = ('id', 'amount', 'parcel_type', 'parcel_tenure')


class LandSplitSerializer(DynamicModelSerializer):

    old_land = DynamicRelationField('LandSerializer', embed=True)
    new_land = DynamicRelationField('LandSerializer', embed=True)

    class Meta:
        model = models.LandSplit
        fields = ('id', 'old_land', 'new_land')


class PositionSerializer(DynamicModelSerializer):

    person = DynamicRelationField('PersonSerializer', embed=True)
    title = DynamicRelationField('PositionTypeSerializer', embed=True)
    session = DynamicRelationField('SessionSerializer', embed=True)

    class Meta:
        model = models.Position
        fields = ('id', 'definitive', 'person', 'title', 'session')


class RelationshipSerializer(DynamicModelSerializer):

    person_one = DynamicRelationField('PersonSerializer', embed=True)
    person_two = DynamicRelationField('PersonSerializer', embed=True)
    relationship = DynamicRelationField('RelationSerializer', embed=True)

    class Meta:
        model = models.Relationship
        fields = ('id', 'definitive')
