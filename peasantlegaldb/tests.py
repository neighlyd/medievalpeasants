from django.test import TestCase
import factory, random
from .utils.choiceprovider import *
from .models import *
from django.core.urlresolvers import reverse

# include a faker provider to integrate Django's choice fields.
factory.Faker.add_provider(ChoiceProvider)
# included a faker for my relation_name and folio field, unique to my DB structure.
factory.Faker.add_provider(RelationProvider)
factory.Faker.add_provider(FolioProvider)

'''
    Factories for models created here using factory_boy (http://factoryboy.readthedocs.io/en/latest/introduction.html)
    Notes on Faker providers are located - https://faker.readthedocs.io/en/latest/providers.html
    
    To run tests:
    >>> coverage run manage.py test [APPNAMEHERE] -v 2
'''

class ArchiveFactory(factory.DjangoModelFactory):
    class Meta:
        model = Archive

    name = factory.Faker('company')
    website = factory.Faker('url')
    notes = factory.Faker('sentence')


class MoneyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Money

    amount = 'iij s ix d'
    in_denarius = 45


class ChattelFactory(factory.DjangoModelFactory):
    class Meta:
        model = Chattel

    name = factory.Faker('word')


class CaseTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = CaseType

    case_type = factory.Faker('word')


class CountyFactory(factory.DjangoModelFactory):
    class Meta:
        model = County

    name = factory.Faker('word')
    abbreviation = factory.Sequence(lambda n: 'abrv%d' % n)


class LandFactory(factory.DjangoModelFactory):
    class Meta:
        model = Land

    notes = factory.Faker('paragraph')
    owner_chain = factory.Faker('sentence')


class ParcelTenureFactory(factory.DjangoModelFactory):
    class Meta:
        model = ParcelTenure

    tenure = factory.Faker('word')


class ParcelTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = ParcelType

    parcel_type = factory.Faker('word')


class PositionTypeFactory(factory.DjangoModelFactory):
    class Meta:
        model = PositionType

    title = factory.Faker('job')


class RelationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Relation

    relation = factory.Faker('word')


class RoleFactory(factory.DjangoModelFactory):
    class Meta:
        model = Role

    role = factory.Faker('word')


class VerdictFactory(factory.DjangoModelFactory):
    class Meta:
        model = Verdict

    verdict = factory.Faker('word')


class HundredFactory(factory.DjangoModelFactory):
    class Meta:
        model = Hundred

    name = factory.Faker('word')
    county = factory.SubFactory(CountyFactory)


class VillageFactory(factory.DjangoModelFactory):
    class Meta:
        model = Village

    name = factory.Faker('word')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    # rework so County info is normalized in Hundred table.
    county = factory.SubFactory(CountyFactory)
    hundred = factory.SubFactory(HundredFactory)
    # listed as Ancient Demesne in 1334 Feudal Aid.
    ancient_demesne = False
    # Part of the "Great Rumor" petition of 1377.
    great_rumor = False
    notes = factory.Faker('paragraph')


class PersonFactory(factory.DjangoModelFactory):
    class Meta:
        model = Person

    first_name = factory.Faker('first_name')
    relation_name = factory.Faker('relation_choice')
    last_name = factory.Faker('last_name')
    status = factory.Faker('random_choice', choices=Person.STATUS_CHOICES)
    village = factory.SubFactory(VillageFactory)
    gender = factory.Faker('random_choice', choices=Person.GENDER_CHOICES)
    tax_1332 = 0
    tax_1379 = 0
    notes = factory.Faker('paragraph')


class RecordFactory(factory.DjangoModelFactory):
    class Meta:
        model = Record

    name = factory.Faker('word')
    archive = factory.SubFactory(ArchiveFactory)
    record_type = factory.Faker('random_choice', choices=Record.RECORD_TYPE)
    reel = random.randint(1, 45)
    notes = factory.Faker('paragraph')


class SessionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Session

    date = factory.Faker('date')
    law_term = factory.Faker('random_choice', choices=Session.TERM_CHOICES)
    folio = factory.Faker('folio')
    record = factory.SubFactory(RecordFactory)
    village = factory.SubFactory(VillageFactory)
    notes = factory.Faker('paragraph')


class ArchiveWithRecordFactory(RecordFactory):
    m2m_archive = factory.RelatedFactory(ArchiveFactory, 'archive')


class CaseFactory(factory.DjangoModelFactory):
    class Meta:
        model = Case

    summary = factory.Faker('paragraph')
    session = factory.SubFactory(SessionFactory)
    case_type = factory.SubFactory(CaseTypeFactory)
    court_type = factory.Faker('random_choice', choices=Case.COURT_TYPES)
    verdict = factory.SubFactory(VerdictFactory)
    of_interest = False
    ad_legem = False
    villeinage_mention = False
    active_sale = False
    incidental_land = False


class CornbotFactory(factory.DjangoModelFactory):
    class Meta:
        model = Cornbot

    amount = random.randint(1, 10)
    crop_type = factory.SubFactory(ChattelFactory)
    price = factory.SubFactory(MoneyFactory)
    case = factory.SubFactory(CaseFactory)
    notes = factory.Faker('paragraph')


class ExtrahuraFactory(factory.DjangoModelFactory):
    class Meta:
        model = Extrahura

    amount = random.randint(1, 10)
    animal = factory.SubFactory(ChattelFactory)
    price = factory.SubFactory(MoneyFactory)
    case = factory.SubFactory(CaseFactory)


class MurrainFactory(factory.DjangoModelFactory):
    class Meta:
        model = Murrain

    amount = random.randint(1, 10)
    animal = factory.SubFactory(ChattelFactory)
    case = factory.SubFactory(CaseFactory)
    notes = factory.Faker('paragraph')


class PlaceMentionedFactory(factory.DjangoModelFactory):
    class Meta:
        model = PlaceMentioned

    case = factory.SubFactory(CaseFactory)
    village = factory.SubFactory(VillageFactory)
    notes = factory.Faker('paragraph')


class LandParcelFactory(factory.DjangoModelFactory):
    class Meta:
        model = LandParcel

    land = factory.SubFactory(LandFactory)
    amount = random.randint(1, 5)
    parcel_type = factory.SubFactory(ParcelTypeFactory)
    parcel_tenure = factory.SubFactory(ParcelTenureFactory)


class LitigantFactory(factory.DjangoModelFactory):
    class Meta:
        model = Litigant

    person = factory.SubFactory(PersonFactory)
    case = factory.SubFactory(CaseFactory)
    role = factory.SubFactory(RoleFactory)
    fine = factory.SubFactory(MoneyFactory)
    amercement = factory.SubFactory(MoneyFactory)
    damage = factory.SubFactory(MoneyFactory)
    damage_notes = factory.Faker('sentence')
    ad_proximum = False
    distrained = False
    attached = False
    bail = False
    chevage = factory.SubFactory(MoneyFactory)
    crossed = False
    recessit = False
    habet_terram = False
    chevage_notes = factory.Faker('sentence')
    heriot_quantity = random.randint(1,5)
    heriot_animal = factory.SubFactory(ChattelFactory)
    heriot = factory.SubFactory(MoneyFactory)
    impercamentum_quantity = random.randint(1,5)
    impercamentum_animal = factory.SubFactory(ChattelFactory)
    impercamentum = factory.SubFactory(MoneyFactory)
    impercamentum_notes = factory.Faker('sentence')
    land = factory.SubFactory(Land)
    land_villeinage = False
    land_notes = factory.Faker('sentence')

    class PledgeFactory(factory.DjangoModelFactory):

        class Meta:
            model = Pledge

        case = factory.SubFactory(CaseFactory)
        pledge_giver = factory.SubFactory(PersonFactory)
        pledge_receiver = factory.SubFactory(PersonFactory)


    class LandSplitFactory(factory.DjangoModelFactory):

        class Meta:
            model = LandSplit

        old_land = factory.SubFactory(LandFactory)
        new_land = factory.SubFactory(LandFactory)


    class PositionFactory(factory.DjangoModelFactory):

        class Meta:
            model = Position

        person = factory.SubFactory(PersonFactory)
        title = factory.SubFactory(PositionTypeFactory)
        session = factory.SubFactory(SessionFactory)
        definitive = False


    class RelationshipFactory(factory.DjangoModelFactory):

        class Meta:
            model = Relationship

        person_one = factory.SubFactory(PersonFactory)
        person_two = factory.SubFactory(PersonFactory)
        relationship = factory.SubFactory(RelationFactory)
        definitive = False


'''
Tests go below here. They use the factories to create junk data.
'''



class Full_Test_PeasantLegalDB(TestCase):

    def test_case_creation(self):
        s = SessionFactory.create()
        c = CaseFactory.create()
        self.assertTrue(isinstance(c, Case))




'''
    def test_create_archive(self):
        w = self.create_archive()
        self.assertTrue(isinstance(w, Archive))
        self.assertEqual(w.__str__(), w.name)

    def create_case_type(self, case_type='test casetype'):
        return CaseType.objects.create(case_type=case_type)

    def test_create_case_type(self):
        w = self.create_case_type()
        self.assertTrue(isinstance(w, CaseType))
        self.assertEqual(w.__str__(), w.case_type)

    def create_county(self, name='test county', abbreviation='tstcnty'):
        return County.objects.create(name=name, abbreviation=abbreviation)

    def test_create_county(self):
        w = self.create_county()
        self.assertTrue(isinstance(w, County))
        self.assertEqual(w.__str__(), w.name)

    def create_parcel_tenure(self, tenure='test tenure type'):
        return ParcelTenure.objects.create(tenure=tenure)

    def test_create_parcel_tenure(self):
        w = self.create_parcel_tenure()
        self.assertTrue(isinstance(w, ParcelTenure))
        self.assertEqual(w.__str__(), w.tenure)

    def create_parcel_type(self, parcel_type='test parcel type'):
        return ParcelType.objects.create(parcel_type=parcel_type)

    def test_create_parcel_type(self):
        w = self.create_parcel_type()
        self.assertTrue(isinstance(w, ParcelType))
        self.assertEqual(w.__str__(), w.parcel_type)

    def create_position_type(self, title='test position'):
        return PositionType.objects.create(title=title)

    def test_create_position_type(self):
        w = self.create_position_type()
        self.assertTrue(isinstance(w, PositionType))
        self.assertEqual(w.__str__(), w.title)

    def create_relation(self, relation='test relation'):
        return Relation.objects.create(relation=relation)

    def test_create_relation(self):
        w = self.create_relation()
        self.assertTrue(isinstance(w, Relation))
        self.assertEqual(w.__str__(), w.relation)

    def create_role(self, role='test role'):
        return Role.objects.create(role=role)

    def test_create_role(self):
        w = self.create_role()
        self.assertTrue(isinstance(w, Role))
        self.assertEqual(w.__str__(), w.role)

    def create_verdict(self, verdict='test verdict'):
        return Verdict.objects.create(verdict=verdict)

    def test_create_verdict(self):
        w = self.create_verdict()
        self.assertTrue(isinstance(w, Verdict))
        self.assertEqual(w.__str__(), w.verdict)

    def create_hundred(self, hundred='test hundred', county=):
'''
