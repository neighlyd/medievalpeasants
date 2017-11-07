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
        ],
        deferred=True
    )
    records = DynamicRelationField('RecordSerializer', source='record_set', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Archive
        name = 'archive'
        fields = ('id', 'name', 'website', 'notes', 'counts', 'records')

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
    archive = DynamicRelationField('ArchiveSerializer', deferred=True, embed=True)
    sessions = DynamicRelationField('SessionSerializer', source='session_set', many=True, deferred=True, embed=True)
    counts = DynamicMethodField(
        requires = [
            'session_set__case'
        ],
        deferred=True
    )
    session_dates = DynamicMethodField(
        requires = [
            'session_set'
        ],
        deferred=True
    )

    class Meta:
        model = models.Record
        fields = ('id', 'name', 'record_type', 'reel', 'notes', 'counts', 'archive', 'sessions', 'session_dates')

    def get_session_dates(self, record):
        counts = {}

        counts['earliest_session'] = record.earliest_session
        counts['latest_session'] = record.latest_session

        return counts

    def get_counts(self, record):
        counts = {}
        counts['case'] = record.case_count
        counts['session'] = record.session_count
        return counts

    def get_record_type(self, record):
        return record.get_record_type_display()


class CountySerializer(DynamicModelSerializer):

    counts = DynamicMethodField(
        requires = [
            'village_set__session_set__case', 'village_set__person'
        ],
        deferred=True
    )
    villages = DynamicRelationField('VillageSerializer', source='village_set', deferred=True, many=True, embed=True)
    hundreds = DynamicRelationField('HundredSerializer', source='hundred_set', deferred=True, many=True, embed=True)

    class Meta:
        model = models.County
        fields = ('id', 'name', 'abbreviation', 'counts', 'villages', 'hundreds',)

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

    county = DynamicRelationField('CountySerializer', deferred=True, embed=True)
    counts = DynamicMethodField(
        requires = [
            'village'
        ],
        deferred=True
    )
    villages = DynamicRelationField('VillageSerializer', source='village_set', many=True, deferred=True, embed=True)

    class Meta:
        model = models.Hundred
        fields = ('id', 'name', 'counts', 'county', 'villages')

    def get_counts(self, record):
        counts={}
        counts['village'] = record.village_count
        return counts


class VillageSerializer(DynamicModelSerializer):

    hundred = DynamicRelationField('HundredSerializer', deferred=True, embed=True)
    county = DynamicRelationField('CountySerializer', deferred=True, embed=True)
    sessions = DynamicRelationField('SessionSerializer', source='session_set', deferred=True, many=True, embed=True)
    counts = DynamicMethodField(
        requires = [
            'person'
        ],
        deferred=True,
    )
    chevage_payer_count = DynamicMethodField(deferred=True)
    fine_payer_count = DynamicMethodField(deferred=True)
    impercamentum_payer_count = DynamicMethodField(deferred=True)
    heriot_payer_count = DynamicMethodField(deferred=True)
    damaged_party_count = DynamicMethodField(deferred=True)

    class Meta:
        model = models.Village
        fields = ('id', 'name', 'latitude', 'longitude', 'ancient_demesne', 'great_rumor', 'notes', 'counts', 'county',
                  'hundred', 'sessions', 'chevage_payer_count', 'fine_payer_count', 'impercamentum_payer_count', 
                  'heriot_payer_count', 'damaged_party_count')

    def get_chevage_payer_count(self, record):
        return record.chevage_payer_count

    def get_fine_payer_count(self, record):
        return record.fine_payer_count

    def get_impercamentum_payer_count(self, record):
        return record.impercamentum_payer_count

    def get_heriot_payer_count(self, record):
        return record.heriot_payer_count

    def get_damaged_party_count(self, record):
        return record.damaged_party_count

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
        ],
        deferred=True,
    )
    cases = DynamicRelationField('CaseSerializer', deferred=True, embed=True, many=True)

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year', 'human_date', 'village', 'record', 'counts',
                  'cases')

    def get_counts(self, record):
        counts = {}
        counts['case'] = record.case_count
        counts['litigant'] = record.litigant_count
        counts['land'] = record.land_case_count
        counts['chevage_payer'] = record.chevage_payer_count
        counts['impercamentum_payer'] = record.impercamentum_payer_count
        return counts

    def get_law_term(self, record):
        return record.get_law_term_display()


class PersonSerializer(DynamicModelSerializer):


    # Use ReadOnlyField to pull in model functions:
    # https://stackoverflow.com/questions/24233988/django-serializer-method-field
    full_name = serializers.ReadOnlyField()
    gender_display = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField()

    counts = DynamicMethodField(
        requires = [
            'person_to_case__case__session', 'pledge_giver', 'pledge_receiver', 'position', 'relationship_person_one',
            'relationship_person_two', 'case_set'
        ],
        deferred=True
    )
    case_dates = DynamicMethodField(
        requires = [
            'person_to_case__case__session', 'pledge_giver__case__session', 'pledge_receiver__case__session'
        ],
        deferred=True
    )
    village = DynamicRelationField('VillageSerializer', embed=True, deferred=True)
    cases = DynamicRelationField('LitigantSerializer', deferred=True, source='person_to_case', many=True, embed=True)
    pledges_given = DynamicRelationField('PledgeSerializer', deferred=True, source='pledge_giver', many=True,
                                         embed=True)
    pledges_received = DynamicRelationField('PledgeSerializer', deferred=True, source='pledge_receiver', many=True,
                                            embed=True)
    positions = DynamicRelationField('PositionSerializer', deferred=True, source='position', many=True, embed=True)

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'relation_name', 'last_name', 'status', 'gender', 'tax_1332', 'tax_1379', 'notes',
                  'full_name', 'counts', 'village', 'cases', 'pledges_given', 'pledges_received', 'positions',
                  'gender_display', 'status_display', 'case_dates')

    def get_case_dates(self, record):
        dates = {}

        dates['earliest_case'] = record.earliest_case
        dates['latest_case'] = record.latest_case
        return dates

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

        return counts


class LandSerializer(DynamicModelSerializer):

    parcel_list = DynamicMethodField(
        requires = [
            'parcels__parcel_type', 'parcels__parcel_tenure'
        ]
    )
    case_dates = DynamicMethodField(
        requires = [
            'case_to_land__case__session'
        ],
        deferred=True
    )

    tenant_history = DynamicRelationField(
        'LitigantSerializer',
        source='case_to_land',
        many=True,
        deferred=True,
        embed=True,
        queryset=models.Litigant.objects.order_by('case__session__date')
    )

    class Meta:
        model = models.Land
        name = 'land'
        fields = ('id', 'notes', 'parcel_list', 'tenant_history', 'case_dates')

    def get_parcel_list(self, record):
        return record.parcel_list

    def get_case_dates(self, record):
        case_info={}
        case_info['earliest'] = record.earliest_case
        case_info['latest'] = record.latest_case

        return case_info


class CaseSerializer(DynamicModelSerializer):

    court_type = serializers.SerializerMethodField()
    litigant_count = DynamicMethodField(
        requires=[
            'case_to_person'
        ],
        deferred=True
    )
    litigant_list = DynamicMethodField(
        requires=[
            'case_to_person'
        ],
        deferred=True
    )
    pledge_count = DynamicMethodField(
        requires=[
            'case_to_pledge'
        ],
        deferred=True
    )

    session = DynamicRelationField('SessionSerializer', deferred=True, embed=True)
    case_type = DynamicRelationField('CaseTypeSerializer', embed=True)
    verdict = DynamicRelationField('VerdictSerializer', embed=True)
    litigants = DynamicRelationField('PersonSerializer', deferred=True, many=True, embed=True)
    cornbot = DynamicRelationField('CornbotSerializer', deferred=True, many=True, embed=True)
    extrahura = DynamicRelationField('ExtrahuraSerializer', deferred=True, many=True, embed=True)
    murrain = DynamicRelationField('MurrainSerializer', deferred=True, many=True, embed=True)
    places_mentioned = DynamicRelationField('PlaceMentionedSerializer', source='placementioned_set', deferred=True,
                                            many=True, embed=True)
    people = DynamicRelationField('LitigantSerializer', source='case_to_person', deferred=True, many=True, embed=True)
    pledges = DynamicRelationField('PledgeSerializer', source='case_to_pledge', deferred=True, many=True, embed=True)


    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'court_type', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale',
                  'incidental_land', 'session', 'case_type', 'verdict', 'litigants', 'litigant_count', 'litigant_list',
                  'cornbot', 'extrahura', 'murrain', 'places_mentioned', 'people', 'pledges', 'pledge_count')

    def get_court_type(self, record):
        return record.get_court_type_display()

    def get_litigant_list(self, record):
        return record.litigant_list

    def get_litigant_count(self, record):
        return record.litigant_count

    def get_pledge_count(self, record):
        return record.pledge_count


class LitigantSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    person = DynamicRelationField('PersonSerializer', deferred=True, embed=True)
    land = DynamicRelationField('LandSerializer', embed=True)
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
    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)

    class Meta:
        model = models.Pledge
        fields = ('id', 'pledge_giver', 'pledge_receiver', 'case')


class CornbotSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    crop_type = DynamicRelationField('ChattelSerializer', embed=True)
    price = DynamicRelationField('MoneySerializer', embed=True)

    class Meta:
        model = models.Cornbot
        fields = ('id', 'amount', 'notes', 'case', 'crop_type', 'price')


class ExtrahuraSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    animal = DynamicRelationField('ChattelSerializer', embed=True)
    price = DynamicRelationField('MoneySerializer', embed=True)

    class Meta:
        model = models.Extrahura
        fields = ('id', 'amount', 'animal', 'price', 'case')


class MurrainSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    animal = DynamicRelationField('ChattelSerializer', embed=True)

    class Meta:
        model = models.Murrain
        fields = ('id', 'amount', 'notes', 'animal', 'case')


class PlaceMentionedSerializer(DynamicModelSerializer):

    case = DynamicRelationField('CaseSerializer', deferred=True, embed=True)
    village = DynamicRelationField('VillageSerializer', deferred=True, embed=True)

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

    old_land = DynamicRelationField('LandSerializer', deferred=True, embed=True)
    new_land = DynamicRelationField('LandSerializer', deferred=True, embed=True)

    class Meta:
        model = models.LandSplit
        fields = ('id', 'old_land', 'new_land')


class PositionSerializer(DynamicModelSerializer):

    person = DynamicRelationField('PersonSerializer', deferred=True, embed=True)
    title = DynamicRelationField('PositionTypeSerializer', embed=True)
    session = DynamicRelationField('SessionSerializer', deferred=True, embed=True)

    class Meta:
        model = models.Position
        fields = ('id', 'definitive', 'person', 'title', 'session')


class RelationshipSerializer(DynamicModelSerializer):

    person_one = DynamicRelationField('PersonSerializer', deferred=True, embed=True)
    person_two = DynamicRelationField('PersonSerializer', deferred=True, embed=True)
    relationship = DynamicRelationField('RelationSerializer', embed=True)

    class Meta:
        model = models.Relationship
        fields = ('id', 'definitive', 'person_one', 'person_two', 'relationship')