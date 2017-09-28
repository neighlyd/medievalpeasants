from rest_framework import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from peasantlegaldb import models


# Normalized tables section
class ParcelTenureSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.ParcelTenure
        fields = ('id', 'tenure',)


class ParcelTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.ParcelType
        fields = ('id', 'parcel_type',)


class PositionTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.PositionType
        fields = ('id', 'title',)


class RelationSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Relation
        fields = ('id', 'relation',)


class RoleSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = ('id', 'role',)


class VerdictSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Verdict
        fields = ('id', 'verdict',)


class MoneySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Money
        fields = ('id', 'amount', 'in_denarius')


class ChattelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Chattel
        fields = ('id', 'name',)


class CaseTypeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.CaseType
        fields = ('id', 'case_type',)

# Begin Data-Entry tables


class ArchiveSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Archive
        fields = ('id', 'name', 'website', 'notes')


class RecordSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    record_type = serializers.SerializerMethodField()

    class Meta:
        model = models.Record
        fields = ('id', 'name', 'record_type', 'reel', 'notes')
        expandable_fields = dict(
            archive=ArchiveSerializer,
        )

    def get_record_type(self, obj):
        return obj.get_record_type_display()


class CountySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.County
        fields = ('id', 'name', 'abbreviation')


class HundredSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Hundred
        fields = ('id', 'name')
        expandable_fields = dict(
            county=CountySerializer,
        )


class VillageSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Village
        fields = ('id', 'name', 'latitude', 'longitude', 'ancient_demesne', 'great_rumor', 'notes')
        expandable_fields = dict(
            hundred=HundredSerializer,
            county=CountySerializer,
        )


class SessionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    law_term = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year')
        expandable_fields = dict(
            village=VillageSerializer,
            record=RecordSerializer,
        )

    def get_law_term(self, obj):
        return obj.get_law_term_display()

    def get_year(self, obj):
        return obj.date.year


class LandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Land
        fields = ('id', 'notes', 'owner_chain')


class PersonSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    # Use ReadOnlyField to pull in model functions:
    # https://stackoverflow.com/questions/24233988/django-serializer-method-field
    full_name = serializers.ReadOnlyField()

    gender = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    case_count_litigation = serializers.ReadOnlyField()
    case_count_all = serializers.ReadOnlyField()
    earliest_case = serializers.ReadOnlyField()
    latest_case = serializers.ReadOnlyField()
    case_info = serializers.ReadOnlyField()
    pledges_given_count = serializers.ReadOnlyField()
    pledges_received_count = serializers.ReadOnlyField()

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'relation_name', 'last_name', 'status', 'gender', 'tax_1332', 'tax_1379', 'notes',
                  'full_name', 'case_count_litigation', 'case_count_all', 'earliest_case', 'latest_case', 'case_info',
                  'pledges_given_count', 'pledges_received_count')
        expandable_fields = dict(
            village=VillageSerializer,
        )

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_status(self, obj):
        return obj.get_status_display()


class CaseSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    litigant_count = serializers.ReadOnlyField()
    court_type = serializers.SerializerMethodField()
    litigant_list = serializers.ReadOnlyField()
    litigant_list_concat = serializers.ReadOnlyField()

    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'court_type', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale',
                  'incidental_land', 'litigant_count', 'litigant_list', 'litigant_list_concat')
        expandable_fields = dict(
            session=SessionSerializer,
            case_type=CaseTypeSerializer,
            verdict=VerdictSerializer,
            litigants=dict(
                serializer=PersonSerializer,
                many=True
            )
        )

    def get_court_type(self, obj):
        return obj.get_court_type_display()


class LitigantSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    amercement = MoneySerializer()
    fine = MoneySerializer()
    damage = MoneySerializer()
    chevage = MoneySerializer()
    heriot_animal = ChattelSerializer
    heriot_assessment = MoneySerializer()
    impercamentum_animal = ChattelSerializer()
    impercamentum_amercement = MoneySerializer()



    class Meta:
        model = models.Litigant
        fields = ('id', 'damage_notes', 'ad_proximum', 'distrained', 'attached', 'bail', 'chevage', 'crossed',
                  'recessit', 'habet_terram', 'chevage_notes', 'heriot_quantity', 'impercamentum_quantity',
                  'impercamentum_notes', 'amercement', 'fine', 'damage', 'chevage', 'heriot_animal', 'heriot_assessment',
                  'impercamentum_animal', 'impercamentum_amercement')
        expandable_fields = dict(
            case=CaseSerializer,
            person=PersonSerializer,
            role=RoleSerializer,
            fine=MoneySerializer,
            amercement=MoneySerializer,
            damage=MoneySerializer,
            chevage=MoneySerializer,
            heriot_assessment=MoneySerializer,
            heriot_animal=ChattelSerializer,
            impercamentum_amercement=MoneySerializer,
            impercamentum_animal=ChattelSerializer,
        )


class CasePeopleLandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.CasePeopleLand
        fields = ('id', 'villeinage', 'notes', 'person', 'case', 'land', 'role')
        expandable_fields = dict(
            person=PersonSerializer,
            case=CaseSerializer,
            land=LandSerializer,
            role=RoleSerializer
        )


class PledgeSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Pledge
        fields = ('id',)
        expandable_fields = dict(
            pledge_giver=PersonSerializer,
            pledge_receiver=PersonSerializer,
            case=CaseSerializer,
        )


class CornbotSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Cornbot
        fields = ('id', 'amount', 'notes')
        expandable_fields = dict(
            case=CaseSerializer,
            crop_type=ChattelSerializer,
            price=MoneySerializer,
        )


class ExtrahuraSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Extrahura
        fields = ('id', 'amount')
        expandable_fields = dict(
            animal=ChattelSerializer,
            price=MoneySerializer,
            case=CaseSerializer,
        )


class MurrainSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Murrain
        fields = ('id', 'amount', 'notes')
        expandable_fields = dict(
            animal=ChattelSerializer,
            case=CaseSerializer
        )


class PlaceMentionedSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.PlaceMentioned
        fields = ('id', 'notes')
        expandable_fields = dict(
            case=CaseSerializer,
            village=VillageSerializer,
        )


class LandParcelSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.LandParcel
        fields = ('id', 'amount')
        expandable_fields = dict(
            parcel_type=ParcelTypeSerializer,
            parcel_tenure=ParcelTenureSerializer,
        )


class LandSplitSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.LandSplit
        fields = ('id',)
        expandable_fields = dict(
            old_land=LandSerializer,
            new_land=LandSerializer,
        )


class PositionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Position
        fields = ('id', 'definitive')
        expandable_fields = dict(
            person=PersonSerializer,
            title=PositionTypeSerializer,
            session=SessionSerializer,
        )


class RelationshipSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Relationship
        fields = ('id', 'definitive')
        expandable_fields = dict(
            person_one=PersonSerializer,
            person_two=PersonSerializer,
            relationship=RelationSerializer,
        )
