from django.db.models import Count, Max, Min, Avg, Sum

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
        expandable_fields = dict(
            info=serializers.SerializerMethodField
        )

    def get_info(self, record):
        try:
            archive_info = {}

            archive_info['record_count'] = record.record_count

            archive_info['session_count'] = record.session_count

            archive_info['case_count'] = record.case_count

            return archive_info


        except:
            return None


class SessionsForRecordsSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    law_term = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    case_count = serializers.ReadOnlyField()
    human_date = serializers.ReadOnlyField()

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year', 'village', 'case_count', 'human_date')
        depth = 2

    def get_law_term(self, obj):
        return obj.get_law_term_display()

    def get_year(self, obj):
        return obj.date.year


class RecordSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    record_type = serializers.SerializerMethodField()
    date_range = serializers.ReadOnlyField()

    class Meta:
        model = models.Record
        fields = ('id', 'name', 'record_type', 'reel', 'notes', 'date_range',)
        expandable_fields = dict(
            archive=ArchiveSerializer,
            session_set = dict(
                serializer = SessionsForRecordsSerializer,
                many = True,
                id_source = 'record_id'
            ),
            session_info=serializers.SerializerMethodField,
        )

    def get_session_info(self, record):
        try:
            session_info = {}

            earliest_session = record.earliest_session
            session_info['earliest'] = self.represent_child(
                name='earliest',
                serializer=SessionsForRecordsSerializer,
                instance=earliest_session
            )

            latest_session = record.latest_session
            session_info['latest'] = self.represent_child(
                name='latest',
                serializer=SessionsForRecordsSerializer,
                instance=latest_session
            )

            session_info['session_count'] = record.session_count

            session_info['case_count'] = record.case_count

            return session_info


        except:
            return None

    def get_record_type(self, obj):
        return obj.get_record_type_display()



class CountySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.County
        fields = ('id', 'name', 'abbreviation')
        expandable_fields = dict(
            counts=serializers.SerializerMethodField,
        )

    def get_counts(self, record):
        counts={}
        counts['hundred'] = record.hundred_count
        counts['village']= record.village_count
        counts['great_rumor'] = record.great_rumor_count
        counts['ancient_demesne'] = record.ancient_demesne_count
        counts['session']= record.session_count
        counts['case'] = record.case_count
        counts['resident'] = record.resident_count
        counts['litigant'] = record.litigant_count
        return counts


class HundredSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Hundred
        fields = ('id', 'name')
        expandable_fields = dict(
            county=CountySerializer,
            counts=serializers.SerializerMethodField,
        )

    def get_counts(self, obj):
        counts={}
        counts['village']=obj.village_set.count()
        return counts


class VillageSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Village
        fields = ('id', 'name', 'latitude', 'longitude', 'ancient_demesne', 'great_rumor', 'notes')
        expandable_fields = dict(
            hundred=HundredSerializer,
            county=CountySerializer,
            counts=serializers.SerializerMethodField,
        )

    # Because SerializerExtensionsMixin doesn't serialize ReadOnlyFields (i.e. calculated fields in models, but only in
    # serializers themselves, enabling the calculation to occur in both serializer and model requires breaking DRY. To
    # get around this would either require calculating the field every time the serializer is called (way too many db
    # hits for something as common as models.Village and models.Case), or simply just having the calculation in both
    # model and serializer as I have chosen here. There HAS to be a better way, but short of adding a
    # serializers.SerializerReadOnlyField definition to the SerializersExtensionMixin, I can't think of one.
    def get_counts(self, obj):
        counts={}
        counts['case']=models.Case.objects.all().filter(session__village_id=obj.id).distinct().count()
        counts['resident']=obj.person_set.filter(village=obj).distinct().count()
        counts['litigant']=len(set(models.Litigant.objects.all().filter(case__session__village_id=obj.id).values_list('person', flat=True)))
        counts['session']=obj.session_set.count()

        return counts



class SessionSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    law_term = serializers.SerializerMethodField()
    year = serializers.ReadOnlyField()
    case_count = serializers.ReadOnlyField()
    human_date = serializers.ReadOnlyField()

    class Meta:
        model = models.Session
        fields = ('id', 'date', 'folio', 'notes', 'law_term', 'year', 'case_count', 'human_date')
        expandable_fields = dict(
            village=VillageSerializer,
            record=RecordSerializer,
        )



    def get_law_term(self, obj):
        return obj.get_law_term_display()

class CaseforLandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    litigant_count = serializers.ReadOnlyField()
    court_type = serializers.SerializerMethodField()
    litigant_list = serializers.ReadOnlyField()
    session = SessionSerializer(read_only=True)
    case_type=CaseTypeSerializer(read_only=True)
    verdict=VerdictSerializer(read_only=True)

    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'court_type', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale',
                  'incidental_land', 'litigant_count', 'litigant_list', 'session', 'verdict',
                  'case_type')

    def get_court_type(self, obj):
        return obj.get_court_type_display()



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
    pledges_given_count = serializers.ReadOnlyField()
    pledges_received_count = serializers.ReadOnlyField()

    class Meta:
        model = models.Person
        fields = ('id', 'first_name', 'relation_name', 'last_name', 'status', 'gender', 'tax_1332', 'tax_1379', 'notes',
                  'full_name', 'case_count_litigation', 'case_count_all', 'earliest_case', 'latest_case',
                  'pledges_given_count', 'pledges_received_count',)
        expandable_fields = dict(
            village=VillageSerializer,
            case_info=serializers.SerializerMethodField
        )

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_case_info(self, obj):
        return obj.person_to_case.aggregate(Count('amercement'), Max('amercement__in_denarius'),
                                             Min('amercement__in_denarius'), Avg('amercement__in_denarius'),
                                             Sum('amercement__in_denarius'), Count('fine'), Max('fine__in_denarius'),
                                             Min('fine__in_denarius'), Avg('fine__in_denarius'),
                                             Sum('fine__in_denarius'), Count('damage'), Max('damage__in_denarius'),
                                             Min('damage__in_denarius'), Avg('damage__in_denarius'),
                                             Sum('damage__in_denarius'), Count('chevage'), Max('chevage__in_denarius'),
                                             Min('chevage__in_denarius'), Avg('chevage__in_denarius'),
                                             Sum('chevage__in_denarius'), Count('heriot'), Max('heriot__in_denarius'),
                                             Min('heriot__in_denarius'), Avg('heriot__in_denarius'),
                                             Sum('heriot__in_denarius'), Count('impercamentum'),
                                             Max('impercamentum__in_denarius'), Min('impercamentum__in_denarius'),
                                             Avg('impercamentum__in_denarius'), Sum('impercamentum__in_denarius'), )


class PersonforLandListSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    full_name = serializers.ReadOnlyField()
    residency = serializers.ReadOnlyField()

    class Meta:
        model = models.Person
        fields = ('id', 'full_name', 'residency')



class LitigantforLandListSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    fine = MoneySerializer()
    person = PersonforLandListSerializer()
    role = RoleSerializer()
    case = CaseforLandSerializer()

    class Meta:
        model = models.Litigant
        fields = ('id', 'fine',  'land_notes', 'land_villeinage', 'person', 'case', 'role')


class LandSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    parcel_list = serializers.ReadOnlyField()

    class Meta:
        model = models.Land
        fields = ('id', 'notes', 'owner_chain', 'parcel_list')
        expandable_fields = dict(
            earliest_case=serializers.SerializerMethodField,
            latest_case=serializers.SerializerMethodField,
            tenant_list=serializers.SerializerMethodField,
            tenant_history=serializers.SerializerMethodField,
            case_info = serializers.SerializerMethodField,
            )

    def get_case_info(self, record):
        try:
            case_info = {}
            earliest_case = record.earliest_case
            case_info['earliest'] = self.represent_child(
                name='earliest',
                serializer=CaseforLandSerializer,
                instance=earliest_case
            )
            latest_case = record.latest_case
            case_info['latest'] = self.represent_child(
                name='latest',
                serializer=CaseforLandSerializer,
                instance=latest_case
            )
            return case_info
        except:
            return None

    def get_tenant_history(self, record):

        tenant_list = record.case_to_land.order_by('case__session__date')
        return self.represent_child(
            name='tenants',
            serializer=LitigantforLandListSerializer,
            instance=tenant_list,
            many=True,
        )

class CaseSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):

    litigant_count = serializers.ReadOnlyField()
    court_type = serializers.SerializerMethodField()
    litigant_list = serializers.ReadOnlyField()

    class Meta:
        model = models.Case
        fields = ('id', 'summary', 'court_type', 'of_interest', 'ad_legem', 'villeinage_mention', 'active_sale',
                  'incidental_land', 'litigant_count', 'litigant_list')
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
    heriot= MoneySerializer()
    impercamentum_animal = ChattelSerializer()
    impercamentum = MoneySerializer()

    class Meta:
        model = models.Litigant
        fields = ('id', 'damage_notes', 'ad_proximum', 'distrained', 'attached', 'bail', 'chevage', 'crossed',
                  'recessit', 'habet_terram', 'chevage_notes', 'heriot_quantity', 'impercamentum_quantity',
                  'impercamentum_notes', 'amercement', 'fine', 'damage', 'chevage', 'heriot_animal', 'heriot',
                  'impercamentum_animal', 'impercamentum', 'land_notes', 'land_villeinage')
        expandable_fields = dict(
            case=CaseSerializer,
            person=PersonSerializer,
            role=RoleSerializer,
            fine=MoneySerializer,
            amercement=MoneySerializer,
            damage=MoneySerializer,
            chevage=MoneySerializer,
            heriot=MoneySerializer,
            heriot_animal=ChattelSerializer,
            impercamentum=MoneySerializer,
            impercamentum_animal=ChattelSerializer,
            land=LandSerializer,
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
