import datetime

from django.db import models
from django.db.models import Count, Max, Min, Avg, Sum
from itertools import chain


'''
TODO:
1) establish Manor model
    Fields: [name, village, coterminous, owner (one-to-many - Owner model)]
        Owner Model:
            Fields: [name (one-to-one - Person model), person certainty, begin date, begin date certainty, end date, 
            end date certainty, notes, references (one-to-many?)]
2) Move Village from Session to Manor
3) Move Session counts to Manor from Village
'''

class Archive(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    @property
    def record_count(self):
        return self.record_set.count()

    @property
    def session_count(self):
        return self.record_set.aggregate(Count('session')).get('session__count')

    @property
    def case_count(self):
        return self.record_set.aggregate(Count('session__cases')).get('session__cases__count')

    def __str__(self):
        return self.name


class Money(models.Model):
    amount = models.CharField(max_length=150)
    in_denarius = models.IntegerField(null=True)

    def __str__(self):
        if not self.in_denarius:
            return '%s (no price)' % (self.amount)
        else:
            return '%s (%s d.)' % (self.amount, self.in_denarius)


class Chattel(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class CaseType(models.Model):

    class Meta:
        verbose_name = "Case Type"
        verbose_name_plural = "Case Types"

    case_type = models.CharField(max_length=150)

    def __str__(self):
        return self.case_type


class County(models.Model):

    class Meta:
        verbose_name_plural = "Counties"

    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=15)

    @property
    def hundred_count(self):
        return self.hundred_set.count()

    @property
    def village_count(self):
        return self.village_set.count()

    @property
    def great_rumor_count(self):
        return self.village_set.filter(great_rumor=True).count()

    @property
    def ancient_demesne_count(self):
        return self.village_set.filter(ancient_demesne=True).count()

    @property
    def session_count(self):
        return self.village_set.aggregate(Count('session')).get('session__count')

    @property
    def case_count(self):
        return self.village_set.aggregate(Count('session__cases')).get('session__cases__count')

    @property
    def resident_count(self):
        return self.village_set.aggregate(Count('person')).get('person__count')

    @property
    def litigant_count(self):
        return len(set(Litigant.objects.all().filter(case__session__village__county_id=self).values_list('person', flat=True)))

    def __str__(self):
        return self.name


class Land(models.Model):
    #   Change save condition to automagically update notes field w/ land owners from Litigants?
    notes = models.TextField()
    owner_chain = models.TextField()

    @property
    def parcel_list(self):
        parcel_list = []
        queryset = self.parcels.all().prefetch_related('parcel_type', 'parcel_tenure')
        try:
            for x in queryset:
                new_entry = {
                    "amount": x.amount,
                    "type": x.parcel_type.parcel_type,
                    "tenure": x.parcel_tenure.tenure,
                }
                parcel_list.append(new_entry)
        except:
            pass

        return parcel_list

    @property
    def earliest_case(self):
        try:
            earliest = self.case_to_land.earliest('case__session__date')
        except:
            earliest = None
        if not earliest:
            earliest_case = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'date': None,
                'year': None,
            }
        else:
            earliest_case = {
                'id': earliest.case.session.id,
                'village': {'name': earliest.case.session.village.name},
                'law_term': earliest.case.session.get_law_term_display(),
                'date': earliest.case.session.date,
                'year': earliest.case.session.date.year,
                }
        return earliest_case

    @property
    def latest_case(self):
        try:
            latest = self.case_to_land.latest('case__session__date')
        except:
            latest = None
        if not latest:
            latest_case = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'date': None,
                'year': None,
            }
        else:
            latest_case = {
                'id': latest.case.session.id,
                'village': {'name': latest.case.session.village.name},
                'law_term': latest.case.session.get_law_term_display(),
                'date': latest.case.session.date,
                'year': latest.case.session.date.year,
            }

        return latest_case

    def __str__(self):
        return "Land ID: %s" % (self.id)


class ParcelTenure(models.Model):

    class Meta:
        verbose_name = "Parcel Tenure"
        verbose_name_plural = "Parcel Tenures"

    tenure = models.CharField(max_length=50)

    def __str__(self):
        return self.tenure


class ParcelType(models.Model):
    class Meta:
        verbose_name = "Parcel Type"
        verbose_name_plural = "Parcel Types"

    parcel_type = models.CharField(max_length=50)

    def __str__(self):
        return self.parcel_type


class LandParcel(models.Model):

    class Meta:
        verbose_name = "Land Parcel"
        verbose_name_plural = "Land Parcels"

    #   fix null in land_id
    land = models.ForeignKey(Land, null=True, on_delete=models.CASCADE, related_name="parcels")
    amount = models.FloatField()
    parcel_type = models.ForeignKey(ParcelType, verbose_name='type')
    parcel_tenure = models.ForeignKey(ParcelTenure, verbose_name='tenure')


class PositionType(models.Model):
    class Meta:
        verbose_name = "Position Name"
        verbose_name_plural = "Position Names"

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Relation(models.Model):
    class Meta:
        verbose_name = "Relation Type"
        verbose_name_plural = "Relation Types"

    relation = models.CharField(max_length=25)

    def __str__(self):
        return self.relation


class Role(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class Verdict(models.Model):
    verdict = models.CharField(max_length=150)

    def __str__(self):
        return self.verdict


class Hundred(models.Model):
    name = models.CharField(max_length=50)
    county = models.ForeignKey(County)

    @property
    def village_count(self):
        return self.village_set.count()

    def __str__(self):
        return '%s, %s' % (self.name, self.county)


class Village(models.Model):

    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    # rework so County info is normalized in Hundred table.
    county = models.ForeignKey(County)
    hundred = models.ForeignKey(Hundred, null=True)
    # listed as Ancient Demesne in 1334 Feudal Aid.
    ancient_demesne = models.BooleanField(default=False)
    # Part of the "Great Rumor" petition of 1377.
    great_rumor = models.BooleanField(default=False)
    notes = models.TextField()

    @property
    def case_count(self):
        return self.session_set.aggregate(Count('cases')).get('cases__count')

    @property
    def litigant_count(self):
        # retrieve a list of all people who are in Litigant table associated with a particular village, use set() to
        # remove duplicates, and len() to find length.
        return len(set(Litigant.objects.all().filter(case__session__village_id=self.id).values_list('person', flat=True)))

    @property
    def resident_count(self):
        return self.person_set.count()

    @property
    def session_count(self):
        return self.session_set.count()
    
    @property
    def chevage_payer_count(self):
        return len(set(Litigant.objects.all().filter(chevage__isnull=False, case__session__village_id=self.id).values_list('person', flat=True)))

    @property
    def fine_payer_count(self):
        return len(set(Litigant.objects.all().filter(fine__isnull=False, case__session__village_id=self.id).values_list('person', flat=True)))

    @property
    def impercamentum_payer_count(self):
        return len(set(Litigant.objects.all().filter(impercamentum__isnull=False, case__session__village_id=self.id).values_list('person', flat=True)))

    @property
    def heriot_payer_count(self):
        return len(set(Litigant.objects.all().filter(heriot__isnull=False, case__session__village_id=self.id).values_list('person', flat=True)))

    @property
    def damaged_party_count(self):
        return len(set(Litigant.objects.all().filter(damage__isnull=False, case__session__village_id=self.id).values_list('person', flat=True)))

    def __str__(self):
        return '%s | %s' % (self.name, self.county)


class Person(models.Model):

    class Meta:
        verbose_name_plural = "People"

    STATUS_CHOICES = {
        (1, 'Villein'),
        (2, 'Free'),
        (3, 'Unknown'),
        (4, 'Institution')
    }

    GENDER_CHOICES = {
        ('M', 'Male'),
        ('F', 'Female'),
        ('I', 'Institution'),
        ('U', 'Unknown')
    }

    first_name = models.CharField(max_length=250)
    relation_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    status = models.IntegerField(choices=STATUS_CHOICES)
    village = models.ForeignKey(Village)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # both taxes are to be input in denari.
    tax_1332 = models.FloatField()
    tax_1379 = models.FloatField()

    class Meta:
        verbose_name_plural = "People"

    STATUS_CHOICES = {
        (1, 'Villein'),
        (2, 'Free'),
        (3, 'Unknown'),
        (4, 'Institution')
    }

    GENDER_CHOICES = {
        ('M', 'Male'),
        ('F', 'Female'),
        ('I', 'Institution'),
        ('U', 'Unknown')
    }

    first_name = models.CharField(max_length=250)
    relation_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    status = models.IntegerField(choices=STATUS_CHOICES)
    village = models.ForeignKey(Village)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # both taxes are to be input in denari.
    tax_1332 = models.FloatField()
    tax_1379 = models.FloatField()
    notes = models.TextField()
    notes = models.TextField()

    @property
    def earliest_case(self):
        # get queryset for each area where person interacts with cases (i.e. litigant table, pledges),
        # append together in a list and sort by date using a lambda. Pop earliest case off based on index [0].
        case_list = []
        try:
            case_list.append(self.person_to_case.earliest('case__session__date'))
        except:
            pass
        try:
            case_list.append(self.pledge_giver.earliest('case__session__date'))
        except:
            pass
        try:
            case_list.append(self.pledge_receiver.earliest('case__session__date'))
        except:
            pass
        if not case_list:
            earliest = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'year': None,
                'date': None,
            }
        else:
            earliest = sorted(case_list, key=lambda x: x.case.session.date)[0]
            earliest = {
                'id': earliest.case.id,
                'village': {'name': earliest.case.session.village.name},
                'law_term': earliest.case.session.get_law_term_display(),
                'year': earliest.case.session.year,
                'date': earliest.case.session.date,
                
            }
        return earliest


    @property
    def latest_case(self):
        # see earliest_case for explanation.
        case_list = []
        try:
            case_list.append(self.person_to_case.latest('case__session__date'))
        except:
            pass
        try:
            case_list.append(self.pledge_giver.latest('case__session__date'))
        except:
            pass
        try:
            case_list.append(self.pledge_receiver.latest('case__session__date'))
        except:
            pass
        if not case_list:
            latest = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'year': None,
                'date': None,
            }
        else:
            latest = sorted(case_list, key=lambda x: x.case.session.date, reverse=True)[0]
            latest = {
                'id': latest.case.id,
                'village': {'name': latest.case.session.village.name},
                'law_term': latest.case.session.get_law_term_display(),
                'year': latest.case.session.year,
                'date': latest.case.session.date,

            }
        return latest

    @property
    def pledges_given_count(self):
        return self.pledge_giver.all().count()

    @property
    def pledges_received_count(self):
        return self.pledge_receiver.all().count()

    @property
    def relationship_count(self):
        queryset1 = self.relationship_person_one.all().count()
        queryset2 = self.relationship_person_two.all().count()
        return queryset1 + queryset2

    @property
    def position_count(self):
        return self.position.all().count()

    @property
    def case_exists(self):
        return self.person_to_case.exists()

    @property
    def land_exists(self):
        return self.person_to_case.filter(land__isnull=False).exists()

    @property
    def relationship_exists(self):
        relation_one = self.relationship_person_one.exists()
        relation_two = self.relationship_person_two.exists()
        if relation_one or relation_two:
            return True
        else:
            return False

    @property
    def position_exists(self):
        return self.position.exists()

    @property
    def pledge_exists(self):
        pledge_given = self.pledge_giver.exists()
        pledge_received = self.pledge_receiver.exists()
        if pledge_given or pledge_received:
            return True
        else:
            return False

    @property
    def monetary_counts(self):
        return self.person_to_case.aggregate(amercement_count=Count('amercement'),
                                             amercement_max=Max('amercement__in_denarius'),
                                             amercement_min=Min('amercement__in_denarius'),
                                             amercement_avg=Avg('amercement__in_denarius'),
                                             amercement_sum=Sum('amercement__in_denarius'), fine_count=Count('fine'),
                                             fine_max=Max('fine__in_denarius'), fine_min=Min('fine__in_denarius'),
                                             fine_avg=Avg('fine__in_denarius'), fine_sum=Sum('fine__in_denarius'),
                                             damage_count=Count('damage'), damage_max=Max('damage__in_denarius'),
                                             damage_min=Min('damage__in_denarius'),
                                             damage_avg=Avg('damage__in_denarius'),
                                             damage_sum=Sum('damage__in_denarius'), chevage_count=Count('chevage'),
                                             chevage_max=Max('chevage__in_denarius'),
                                             chevage_min=Min('chevage__in_denarius'),
                                             chevage_avg=Avg('chevage__in_denarius'),
                                             chevage_sum=Sum('chevage__in_denarius'), heriot_count=Count('heriot'),
                                             heriot_max=Max('heriot__in_denarius'),
                                             heriot_min=Min('heriot__in_denarius'),
                                             heriot_avg=Avg('heriot__in_denarius'),
                                             heriot_sum=Sum('heriot__in_denarius'),
                                             impercamentum_count=Count('impercamentum'),
                                             impercamentum_max=Max('impercamentum__in_denarius'),
                                             impercamentum_min=Min('impercamentum__in_denarius'),
                                             impercamentum_avg=Avg('impercamentum__in_denarius'),
                                             impercamentum_sum=Sum('impercamentum__in_denarius') )

    @property
    def amercement_exists(self):
        return self.person_to_case.filter(amercement__isnull=False).exists()

    @property
    def fine_exists(self):
        return self.person_to_case.filter(fine__isnull=False).exists()

    @property
    def damage_exists(self):
        return self.person_to_case.filter(damage__isnull=False).exists()

    @property
    def chevage_exists(self):
        return self.person_to_case.filter(chevage__isnull=False).exists()

    @property
    def impercamentum_exists(self):
        return self.person_to_case.filter(impercamentum__isnull=False).exists()

    @property
    def heriot_exists(self):
        return self.person_to_case.filter(heriot__isnull=False).exists()

    @property
    def case_count_litigation(self):
        case_count = self.person_to_case.exclude(chevage__isnull=False).values_list('case').distinct().count()
        return case_count

    @property
    def case_count_all(self):
        case_count = len(set(self.person_to_case.values_list('case')))
        return case_count

    @property
    def residency(self):
        return self.village.name

    @property
    def relationships(self):
        queryset_1 = self.relationship_person_one.all()
        queryset_2 = self.relationship_person_two.all()
        union = (queryset_1 | queryset_2).distinct()
        data = []
        for x in union:
            new_entry={
                'id': x.id,
                'person_one': str(x.person_one),
                'person_two': str(x.person_two),
                'relationship': str(x.relationship),
            }
            data.append(new_entry)
        return data

    @property
    def full_name(self):
        if self.relation_name:
            concated_name = self.first_name + ' ' + self.relation_name + ' ' + self.last_name
        else:
            concated_name = self.first_name + ' ' + self.last_name
        return concated_name

    @property
    def status_display(self):
        return self.get_status_display()

    @property
    def gender_display(self):
        return self.get_gender_display()

    @property
    def name_and_village(self):
        if self.relation_name:
            concated_name = self.first_name + ' ' + self.relation_name + ' ' + self.last_name + ' | ' + self.village.name
        else:
            concated_name = self.first_name + ' ' + self.last_name + ' | ' + self.village.name
        return concated_name

    def __str__(self):
        if self.relation_name:
            return self.first_name + ' ' + self.relation_name + ' ' + self.last_name + ' | ' + self.village.name
        else:
            return self.first_name + ' ' + self.last_name + ' | ' + self.village.name


class Record(models.Model):
    RECORD_TYPE = {
        (1, 'Court Roll'),
        (2, 'Extant'),
        (3, 'Survey'),
        (4, 'Custumal'),
        (5, 'Patent Roll'),
        (6, 'Account Roll'),
    }

    name = models.CharField(max_length=25)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE)
    record_type = models.IntegerField(choices=RECORD_TYPE)
    reel = models.IntegerField(blank=True)
    notes = models.TextField(blank=True)

    @property
    def earliest_session(self):
        try:
            earliest = self.session_set.filter(date__isnull=False).earliest('date')
        except:
            earliest = None
        if not earliest:
            earliest_session = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'year': None,
                'date': None,
            }
        else:
            earliest_session = {
                'id': earliest.id,
                'village': {'name': earliest.village.name},
                'law_term': earliest.get_law_term_display(),
                'year': earliest.year,
                'date': earliest.date,
            }
        return earliest_session

    @property
    def latest_session(self):
        try:
            latest = self.session_set.filter(date__isnull=False).latest('date')
        except:
            latest = None
        if not latest:
            latest_session = {
                'id': None,
                'village': {'name': None},
                'law_term': None,
                'year': None,
                'date': None,
            }
        else:
            latest_session = {
                'id': latest.id,
                'village': {'name': latest.village.name},
                'law_term': latest.get_law_term_display(),
                'year': latest.year,
                'date': latest.date,
            }
        return latest_session

    @property
    def session_count(self):
        return self.session_set.count()

    @property
    def case_count(self):
        return self.session_set.aggregate(Count('cases')).get('cases__count')


    def __str__(self):
        return self.name


class Session(models.Model):

    class Meta:
        get_latest_by = 'date'

    TERM_CHOICES = {
        (1, 'Hilary'),
        (2, 'Easter'),
        (3, 'Trinity'),
        (4, 'Michaelmas')
    }
    # Hilary - January to April
    # Easter - April to May (Hockday in Glastonbury Records)
    # Trinity - June to July
    # Michaelas - October to December
    date = models.DateField()
    law_term = models.IntegerField(choices=TERM_CHOICES)
    folio = models.CharField(max_length=50)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    village = models.ForeignKey(Village)
    notes = models.TextField()

    @property
    def case_count(self):
        return self.cases.count()

    @property
    def litigant_count(self):
        return len(set(Litigant.objects.filter(case__session=self.id)))

    @property
    def land_case_count(self):
        return len(set(Litigant.objects.filter(case__session=self.id, land__isnull=False).values_list('case', flat=True)))

    @property
    def chevage_payer_count(self):
        return len(set(Litigant.objects.filter(case__session=self.id, chevage__isnull=False).values_list('person', flat=True)))

    @property
    def impercamentum_payer_count(self):
        return len(set(Litigant.objects.filter(case__session=self.id, impercamentum__isnull=False).values_list('person', flat=True)))


    @property
    def human_date(self):
        date = self.date
        date = date.strftime('%b %d, %Y')
        return date

    @property
    def year(self):
        year = self.date.year
        return year

    def __str__(self):
        return '%s Session: | %s, %s %s Session.' % (self.village.name, self.id, self.get_law_term_display(), self.human_date)


class Case(models.Model):

    COURT_TYPES = {
        (1, 'Hallmoot'),
        (2, 'Tourn'),
        (3, 'Impercamentum'),
        (4, 'Chevage'),
        (5, 'Unknown'),
        (6, 'Account Roll'),
    }

    summary = models.TextField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='cases')
    case_type = models.ForeignKey(CaseType)
    court_type = models.IntegerField(choices=COURT_TYPES)
    verdict = models.ForeignKey(Verdict)
    of_interest = models.BooleanField(default=False)
#   started ad legem at Case 578.
    ad_legem = models.NullBooleanField(default=False)
    villeinage_mention = models.BooleanField(default=False)
    active_sale = models.BooleanField(default=False)
    incidental_land = models.BooleanField(default=False)
    litigants = models.ManyToManyField(Person, through='Litigant')

    @property
    def litigant_list(self):
        # iterate through a case's litigant set (case_to_person) and create a list of dictionaries containing the  name
        # and role for each person.
        litigant_list = [{"id": person.person.id, "name": person.person.full_name, "role": person.role.role} for person in self.case_to_person.all()]
        return litigant_list

    @property
    def litigant_count(self):
        litigants = [(x) for x in self.case_to_person.values_list('person_id', flat=True)]
        number_of_litigants = len(set(litigants))
        return number_of_litigants

    @property
    def pledge_count(self):
        pledge_count = len(set(self.case_to_pledge.all()))
        return pledge_count

    @property
    def litigant_exist(self):
        return self.case_to_person.filter(person__isnull=False).exists()

    @property
    def land_exist(self):
        return self.case_to_person.filter(land__isnull=False).exists()

    @property
    def cornbot_exist(self):
        return self.cornbot.filter(case=self).exists()

    @property
    def extrahura_exist(self):
        return self.extrahura.filter(case=self).exists()

    @property
    def murrain_exist(self):
        return self.murrain.filter(case=self).exists()

    @property
    def mentioned_exist(self):
        return self.placementioned_set.filter(case=self).exists()

    @property
    def pledge_exist(self):
        return self.case_to_pledge.filter(case=self).exists()

    def __str__(self):
        return 'Case %s | %s (%s / %s)' % (self.id, self.session.village.name, self.session.get_law_term_display(), self.session.date.year)


class Cornbot(models.Model):
    amount = models.CharField(max_length=50)
    crop_type = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='cornbot')
    notes = models.TextField()


class Extrahura(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='extrahura')


class Murrain(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='murrain')
    notes = models.TextField()


class PlaceMentioned(models.Model):

    class Meta:
        verbose_name_plural = "Places Mentioned"

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    notes = models.TextField()


class Litigant(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_to_case')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_person')
    role = models.ForeignKey(Role, related_name='litigant_role')
    fine = models.ForeignKey(Money, null=True, related_name='litigant_fine')
    amercement = models.ForeignKey(Money, null=True, related_name='litigant_amercement')
    damage = models.ForeignKey(Money, null=True, related_name='litigant_damages')
    damage_notes = models.TextField(null=True)
    ad_proximum = models.NullBooleanField()
    distrained = models.NullBooleanField()
    # Added at Case 1189.
    attached = models.NullBooleanField()
    # Added at Case 1424
    bail = models.NullBooleanField()
    chevage = models.ForeignKey(Money, null=True, related_name='litigant_chevage')
    crossed = models.NullBooleanField()
    recessit = models.NullBooleanField()
    habet_terram = models.NullBooleanField()
    chevage_notes = models.TextField(null=True)
    heriot_quantity = models.CharField(max_length=25, null=True)
    heriot_animal = models.ForeignKey(Chattel, null=True, related_name='heriot_animal')
    heriot = models.ForeignKey(Money, null=True, related_name='heriot_assessment')
    impercamentum_quantity = models.IntegerField(null=True)
    impercamentum_animal = models.ForeignKey(Chattel, null=True, related_name='impercamentum_animal')
    impercamentum = models.ForeignKey(Money, null=True, related_name='impercamentum_amercement')
    impercamentum_notes = models.TextField(null=True)
    land = models.ForeignKey(Land, null=True, on_delete=models.CASCADE, related_name='case_to_land')
    land_villeinage = models.NullBooleanField()
    land_notes = models.TextField(null=True)


class Pledge(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_pledge')
    pledge_giver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='pledge_giver')
    pledge_receiver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='pledge_receiver')

    def __str__(self):
        return "%s pledged %s, Case %s" % (self.pledge_giver, self.pledge_receiver, self.case)


class LandSplit(models.Model):

    class Meta:
        verbose_name = "Land Split"
        verbose_name_plural = "Land Splits"

    old_land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='old_land_parcel')
    new_land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='new_land_parcel')
    # add Case so I can track timing... I'm an idiot!

    def __str__(self):
        return "Old Land ID %s, New Land ID %s" % (self.old_land, self.new_land)


class Position(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='position')
    title = models.ForeignKey(PositionType)
    # rework so this is per case not per session.
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    definitive = models.BooleanField(default=False)

    def __str__(self):
        return self.PositionType.title


class Relationship(models.Model):
    person_one = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationship_person_one')
    person_two = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='relationship_person_two')
    # need to rework so relationships are more descriptive, including when (which case) it was revealed..
    relationship = models.ForeignKey(Relation)
    definitive = models.BooleanField(default=False)
