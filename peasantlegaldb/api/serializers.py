from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from peasantlegaldb import models


class ArchiveSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Archive
        fields = ('id', 'name', 'website', 'notes')


class RecordSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    record_type = serializers.SerializerMethodField()
    archive = ArchiveSerializer()

    class Meta:
        model = models.Record
        fields = ('name','archive','record_type','reel','notes')

    def get_record_type(self, obj):
        return obj.get_record_type_display()



class VillageSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Village
        fields = ('id','name', 'latitude', 'longitude', 'hundred', 'county', 'ancient_demesne',
                  'great_rumor', 'notes')


class SessionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    village = VillageSerializer()
    record = RecordSerializer()
    law_term = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'law_term', 'folio', 'record', 'village', 'notes', 'year')

    def get_law_term(self, obj):
        return obj.get_law_term_display()

    def get_year(self, obj):
        return obj.date.year


class MoneySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Money
        fields = ('amount', 'in_denarius')


class ChattelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Chattel
        fields = ('name',)


class CaseTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.CaseType
        fields = ('case_type',)


class CountySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.County
        fields = ('name', 'abbreviation')


class LandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Land
        fields = ('id', 'notes', 'owner_chain')


class ParcelTenureSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.ParcelTenure
        fields = ('tenure',)


class ParcelTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.ParcelType
        fields = ('parcel_type',)


class PositionTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.PositionType
        fields = ('title',)


class RelationSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Relation
        fields = ('relation',)


class RoleSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = ('role',)


class VerdictSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Verdict
        fields = ('verdict',)


class HundredSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Hundred
        fields = ('id', 'name', 'county')


class CasePeopleLandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):


    class Meta:
        model = models.CasePeopleLand
        fields = ('person', 'case', 'land', 'role', 'villeinage', 'notes')


class PersonSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

#   Use ReadOnlyField to pull in model functions: https://stackoverflow.com/questions/24233988/django-serializer-method-field
    full_name = serializers.ReadOnlyField()

    village = VillageSerializer()
    gender = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    case_count = serializers.ReadOnlyField()
    earliest_case = serializers.ReadOnlyField()
    latest_case = serializers.ReadOnlyField()
    case_info = serializers.ReadOnlyField()

    class Meta:
        model = models.Person
        fields = ('id','first_name', 'relation_name', 'last_name', 'village', 'status', 'gender',
                  'tax_1332', 'tax_1379', 'notes', 'full_name', 'case_count', 'earliest_case', 'latest_case', 'case_info')

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_status(self, obj):
        return obj.get_status_display()


class LitigantSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    person = PersonSerializer()
    role = RoleSerializer()
    fine = MoneySerializer()
    amercement = MoneySerializer()
    damage = MoneySerializer()

    class Meta:
        model = models.Litigant
        fields = ('id', 'person', 'case', 'role', 'fine', 'amercement', 'damage', 'damage_notes',
                  'ad_proximum', 'distrained', 'attached', 'bail', 'chevage', 'crossed', 'recessit', 'habet_terram',
                  'chevage_notes', 'heriot_quantity', 'heriot_animal', 'heriot_assessment', 'impercamentum_quantity',
                  'impercamentum_animal', 'impercamentum_amercement', 'impercamentum_notes')


class CaseSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    litigant_count = serializers.ReadOnlyField()
    session = SessionSerializer()
    case_type = CaseTypeSerializer()
    verdict = VerdictSerializer()
    court_type = serializers.SerializerMethodField()

    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'session', 'case_type', 'court_type', 'verdict', 'of_interest',
                  'ad_legem', 'villeinage_mention', 'active_sale', 'incidental_land','litigant_count')

    def get_court_type(self, obj):
        return obj.get_court_type_display()


class PledgeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Pledge
        fields = ('id', 'case', 'pledge_giver', 'pledge_receiver')


class CornbotSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Cornbot
        fields = '__all__'


class ExtrahuraSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Extrahura
        fields = '__all__'


class MurrainSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Murrain
        fields = '__all__'


class PlaceMentionedSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.PlaceMentioned
        fields = '__all__'


class LandParcelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.LandParcel
        fields = '__all__'


class LandSplitSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.LandSplit
        fields = '__all__'


class PositionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = '__all__'


class RelationshipSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Relationship
        fields = '__all__'

