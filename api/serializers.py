from rest_framework import serializers

from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.fields import DynamicMethodField, DynamicRelationField

from rest_flex_fields import FlexFieldsModelSerializer

from peasantlegaldb import models


# Normalized tables section
class ParcelTenureSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.ParcelTenure
        name = 'parcel_tenure'
        fields = ('id', 'tenure',)
        datatables_always_serialize = ('id',)


class ParcelTypeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.ParcelType
        name = 'parcel_type'
        fields = ('id', 'parcel_type',)
        datatables_always_serialize = ('id',)


class PositionTypeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.PositionType
        name = 'position_title'
        fields = ('id', 'title',)
        datatables_always_serialize = ('id',)


class RelationSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Relation
        name = 'relation_title'
        fields = ('id', 'relation',)
        datatables_always_serialize = ('id',)


class RoleSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Role
        name = 'role'
        fields = ('id', 'role',)
        datatables_always_serialize = ('id',)


class VerdictSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Verdict
        name = 'verdict'
        fields = ('id', 'verdict',)
        datatables_always_serialize = ('id',)


class MoneySerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Money
        name = 'money'
        fields = ('id', 'amount', 'in_denarius')
        datatables_always_serialize = ('id',)


class ChattelSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Chattel
        name = 'chattel'
        fields = ('id', 'name',)
        datatables_always_serialize = ('id',)


class CaseTypeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.CaseType
        name = 'case_type'
        fields = ('id', 'case_type',)
        datatables_always_serialize = ('id',)


class LandParcelSerializer(FlexFieldsModelSerializer):
    parcel_type = ParcelTypeSerializer()
    parcel_tenure = ParcelTenureSerializer()

    class Meta:
        model = models.LandParcel
        fields = '__all__'
        datatables_always_serialize = ('id',)


class AmercementSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Amercement
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'amercement': (MoneySerializer, {'source': 'amercement'}),
    }


class CapitagiumSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Capitagium
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'capitagium': (MoneySerializer, {'source': 'capitagium'}),
    }


class DamageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Damage
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'damage': (MoneySerializer, {'source': 'damage'}),
    }


class FineSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Fine
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'fine': (MoneySerializer, {'source': 'fine'}),
    }


class HeriotSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Heriot
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'heriot': (MoneySerializer, {'source': 'heriot'}),
        'animal': (ChattelSerializer, {'source': 'animal'}),
    }


class ImpercamentumSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Impercamentum
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'impercamentum': (MoneySerializer, {'source': 'impercamentum'}),
        'animal': (ChattelSerializer, {'source': 'animal'}),
    }


# Begin Data-Entry tables

class ArchiveSerializer(FlexFieldsModelSerializer):

    counts = serializers.SerializerMethodField()

    class Meta:
        model = models.Archive
        name = 'archive'
        fields = ('id', 'name', 'website', 'notes', 'counts')
        datatables_always_serialize = ('id',)

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['record'] = record.record_count
        counts['session'] = record.session_count
        counts['case'] = record.case_count
        return counts

    @staticmethod
    def get_record_count(record):
        return record.record_count

    @staticmethod
    def get_session_count(record):
        return record.session_count

    @staticmethod
    def get_case_count(record):
        return record.case_count


class RecordSerializer(FlexFieldsModelSerializer):

    record_type = serializers.SerializerMethodField()
    counts = serializers.SerializerMethodField()
    earliest_session = serializers.ReadOnlyField()
    latest_session = serializers.ReadOnlyField()

    class Meta:
        model = models.Record
        fields = ('id', 'name', 'record_type', 'reel', 'notes', 'counts', 'archive', 'earliest_session', 'latest_session')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'archive': (ArchiveSerializer, {'source': 'archive'}),
        'sessions': ('api.SessionSerializer', {'source': 'session_set', 'many': True}),
    }

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['case'] = record.case_count
        counts['session'] = record.session_count
        return counts

    @staticmethod
    def get_record_type(record):
        return record.get_record_type_display()


class CountySerializer(FlexFieldsModelSerializer):

    counts = serializers.SerializerMethodField()

    class Meta:
        model = models.County
        fields = ('id', 'name', 'abbreviation', 'counts',)
        datatables_always_serialize = ('id',)

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['hundred'] = record.hundred_count
        counts['village'] = record.village_count
        counts['great_rumor'] = record.great_rumor_count
        counts['ancient_demesne'] = record.ancient_demesne_count
        counts['session'] = record.session_count
        counts['case'] = record.case_count
        counts['resident'] = record.resident_count
        counts['litigant'] = record.litigant_count
        return counts


class HundredSerializer(FlexFieldsModelSerializer):

    counts = serializers.SerializerMethodField()

    class Meta:
        model = models.Hundred
        fields = ('id', 'name', 'counts', 'county')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'county': (CountySerializer, {'source': 'county', 'fields': ['id', 'name']}),
        'villages': ('api.VillageSerializer', {'source': 'village_set', 'many': True, 'fields': ['id', 'name']})
    }

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['village'] = record.village_count
        return counts


class VillageSerializer(FlexFieldsModelSerializer):

    counts = serializers.SerializerMethodField()
    capitagium_payer_count = serializers.SerializerMethodField()
    fine_payer_count = serializers.SerializerMethodField()
    impercamentum_payer_count = serializers.SerializerMethodField()
    heriot_payer_count = serializers.SerializerMethodField()
    damaged_party_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Village
        fields = ('id', 'name', 'latitude', 'longitude', 'ancient_demesne', 'great_rumor', 'notes', 'counts', 'county',
                  'hundred', 'capitagium_payer_count', 'fine_payer_count', 'impercamentum_payer_count',
                  'heriot_payer_count', 'damaged_party_count')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'hundred': (HundredSerializer, {'source': 'hundred', 'fields': ['id','name']}),
        'county': (CountySerializer, {'source': 'county', 'fields': ['id', 'name']}),
    }

    @staticmethod
    def get_capitagium_payer_count(record):
        return record.capitagium_payer_count

    @staticmethod
    def get_fine_payer_count(record):
        return record.fine_payer_count

    @staticmethod
    def get_impercamentum_payer_count(record):
        return record.impercamentum_payer_count

    @staticmethod
    def get_heriot_payer_count(record):
        return record.heriot_payer_count

    @staticmethod
    def get_damaged_party_count(record):
        return record.damaged_party_count

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['case'] = record.case_count
        counts['resident'] = record.resident_count
        counts['litigant'] = record.litigant_count
        counts['session'] = record.session_count
        return counts


class SessionSerializer(FlexFieldsModelSerializer):

    law_term = serializers.SerializerMethodField()
    year = serializers.ReadOnlyField()
    human_date = serializers.ReadOnlyField()
    counts = serializers.SerializerMethodField()

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year', 'human_date', 'village', 'record', 'counts',)
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'village': (VillageSerializer, {'source': 'village', 'fields': ['id', 'name']}),
        'record': (RecordSerializer, {'source': 'record'}),
    }

    @staticmethod
    def get_counts(record):
        counts = dict()
        counts['case'] = record.case_count
        counts['litigant'] = record.litigant_count
        counts['land'] = record.land_case_count
        counts['capitagium_payer'] = record.capitagium_payer_count
        counts['impercamentum_payer'] = record.impercamentum_payer_count
        return counts

    @staticmethod
    def get_law_term(record):
        return record.get_law_term_display()


class PersonSerializer(FlexFieldsModelSerializer):

    # Use ReadOnlyField to pull in model functions:
    # https://stackoverflow.com/questions/24233988/django-serializer-method-field
    gender_display = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField()

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'relation_name', 'last_name', 'status', 'gender', 'tax_1332', 'tax_1379', 'notes',
                  'full_name', 'village', 'gender_display', 'status_display', 'earliest_case',
                  'latest_case')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'earliest_case': ('api.CaseSerializer', {'source': 'earliest_case', 'expand': ['session'], 'fields': ['id', 'session']}),
        'latest_case': ('api.CaseSerializer', {'source': 'latest_case', 'expand': ['session'], 'fields': ['id', 'session']}),
        'village': (VillageSerializer, {'source': 'village', 'fields': ['id', 'name']}),
        'cases': ('api.LitigantSerializer', {'source': 'cases', 'many': True, 'read_only': True,
                                                      'fields': ['case', 'role'],
                                                      'expand': ['case']}),
    }

    @staticmethod
    def get_counts(record):
        counts = dict()
        pledge_counts = dict()
        pledge_counts['given'] = record.pledges_given_count
        pledge_counts['received'] = record.pledges_received_count
        counts['pledge'] = pledge_counts
        counts['monetary'] = record.monetary_counts
        counts['relationship'] = record.relationship_count
        counts['position'] = record.position_count
        counts['litigation'] = record.case_count_litigation
        counts['all_cases'] = record.case_count_all

        return counts


class CornbotSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Cornbot
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'crop_type': (ChattelSerializer, {'source': 'crop_type'}),
        'price': (MoneySerializer, {'source': 'price'})
    }


class ExtrahuraSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Extrahura
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'animal': (ChattelSerializer, {'source': 'animal'}),
        'price': (MoneySerializer, {'source': 'price'}),
    }


class MurrainSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Murrain
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'animal': (ChattelSerializer, {'source': 'animal'}),
    }


class PlaceMentionedSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.PlaceMentioned
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'village': (VillageSerializer, {
            'source': 'village',
            'fields': ['id', 'name', 'county', 'great_rumor', 'ancient_demesne', 'counts'],
            'expand': ['county']
            }),
        'case': ('api.CaseSerializer', {
            'source': 'case',
            'expand': ['session']
        })
    }


class CaseSerializer(FlexFieldsModelSerializer):

    court_type = serializers.SerializerMethodField()
    litigant_count = serializers.SerializerMethodField()
    pledge_count = serializers.SerializerMethodField()
    case_type = CaseTypeSerializer()
    verdict = VerdictSerializer()

    class Meta:
        model = models.Case
        fields = ('id', 'active_sale', 'ad_legem', 'case_type', 'court_type', 'incidental_land', 'of_interest',
                  'session', 'summary', 'verdict', 'villeinage_mention', 'litigant_count', 'pledge_count')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'session': (SessionSerializer, {'source': 'session', 'expand': ['village'],
                                        'fields': ['id', 'human_date', 'law_term', 'village', 'year', 'date']}),
        'cornbot': (CornbotSerializer, {'source': 'cornbot', 'many': True, 'expand': ['crop_type', 'price']}),
        'extrahura': (ExtrahuraSerializer, {'source': 'extrahura', 'many': True, 'expand': ['animal', 'price']}),
        'murrain': (MurrainSerializer, {'source': 'murrain', 'many': True, 'expand': ['animal']}),
        'placementioned_set': (PlaceMentionedSerializer, {'source': 'placementioned_set', 'many': True,
                                                        'expand': ['village']}),
        'litigants': ('api.LitigantSerializer', {'source': 'litigants', 'many': True, 'expand': ['person']})
    }

    @staticmethod
    def get_court_type(record):
        return record.get_court_type_display()

    @staticmethod
    def get_litigant_list(record):
        return record.litigant_list

    @staticmethod
    def get_litigant_count(record):
        return record.litigant_count

    @staticmethod
    def get_pledge_count(record):
        return record.pledge_count


class LandSerializer(FlexFieldsModelSerializer):

    parcel_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Land
        name = 'land'
        fields = ('id', 'notes', 'parcel_list', 'earliest_case', 'latest_case')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'earliest_case': ('api.CaseSerializer', {'source': 'earliest_case'}),
        'latest_case': ('api.CaseSerializer', {'source': 'latest_case'}),
        'tenants': ('api.LandtoCaseSerializer', {'source': 'tenants', 'many': True, 'expand': ['litigant',]})
    }

    @staticmethod
    def get_parcel_list(record):
        return record.parcel_list


class LandSplitSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.LandSplit
        fields = ('id', 'old_land', 'new_land')
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'old_land': (LandSerializer, {'source': 'old_land'}),
        'new_land': (LandSerializer, {'source': 'new_land'}),
    }


class LandtoCaseSerializer(FlexFieldsModelSerializer):

    role = RoleSerializer()

    class Meta:
        model = models.LandtoCase
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'land': (LandSerializer, {'source': 'land'}),
        'litigant': ('api.LitigantSerializer', {'source': 'litigant'}),
    }


class LitigantSerializer(FlexFieldsModelSerializer):

    role = RoleSerializer()

    class Meta:
        model = models.Litigant
        fields = ('id', 'case', 'person', 'role', 'ad_proximum', 'distrained', 'attached', 'bail',)
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'case': (CaseSerializer, {'source': 'case', 'expand': ['session']}),
        'person': (PersonSerializer, {'source': 'person', 'expand': ['village']}),
        'amercements': (AmercementSerializer, {'source': 'amercements', 'many': True, 'expand': ['amercement']}),
        'capitagia': (CapitagiumSerializer, {'source': 'capitagia', 'many': True, 'expand': ['capitagium']}),
        'damages': (DamageSerializer, {'source': 'damages', 'many': True, 'expand': ['damage']}),
        'fines': (FineSerializer, {'source': 'fines', 'many': True, 'expand': ['fine']}),
        'heriots': (HeriotSerializer, {'source': 'heriots', 'many': True, 'expand': ['heriot', 'animal']}),
        'impercamenta': (ImpercamentumSerializer, {'source': 'impercamenta', 'many': True,
                                                   'expand': ['impercamentum', 'animal']}),
        'lands': (LandtoCaseSerializer, {'source': 'lands', 'many': True, 'expand': ['land']}),
        'pledges': ('api.PledgeSerializer', {'source': 'pledges', 'many': True, 'expand': ['giver']})
    }


class PledgeSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = models.Pledge
        fields = '__all__'
        datatables_always_serializer = ('id',)
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'giver': (PersonSerializer, {'source': 'giver'}),
        'receiver': (LitigantSerializer, {'source': 'receiver', 'expand': ['person', 'case']}),
    }


class PositionSerializer(FlexFieldsModelSerializer):

    title = PositionTypeSerializer()

    class Meta:
        model = models.Position
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'person': (PersonSerializer, {'source': 'person'}),
        'session': (SessionSerializer, {'source': 'session'})
    }


class RelationshipSerializer(FlexFieldsModelSerializer):

    relationship = RelationSerializer()
    confidence = serializers.SerializerMethodField()

    class Meta:
        model = models.Relationship
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'person_one': (PersonSerializer, {'source': 'person_one'}),
        'person_two': (PersonSerializer, {'source': 'person_two'}),
    }

    @staticmethod
    def get_confidence(record):
        return record.get_confidence_display()


class LandtoCaseSerializer(FlexFieldsModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = models.LandtoCase()
        fields = '__all__'
        datatables_always_serialize = ('id',)

    expandable_fields = {
        'land': (LandSerializer, {'source': 'land'}),
        'litigant': (LitigantSerializer, {'source': 'litigant', 'expand': ['person', 'case']}),
        'case': (CaseSerializer, {'source': 'case'}),
    }
