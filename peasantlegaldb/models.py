from django.db import models
from django.db.models import Count, Max, Min, Avg, Sum

from decimal import *

from datetime import date


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

def median_value(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count > 0:
        if count % 2 == 1:
            return values[int(round(count/2))]
        else:
            return sum(values[count/2-1:count/2+1])/Decimal(2.0)
    else:
        return None

class Archive(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    @property
    def record_count(self):
        return self.record_set.count()

    @property
    def session_count(self):
        # .aggregate(Count('<FIELD>')) returns a dict of {'<FIELD>__count': amount}. Then use .get('<FIELD>__count') to
        # get the value for the API.
        return self.record_set.aggregate(Count('session')).get('session__count')

    @property
    def case_count(self):
        return self.record_set.aggregate(Count('session__case')).get('session__case__count')

    def __str__(self):
        return self.name


class Money(models.Model):
    amount = models.CharField(max_length=150)
    in_denarius = models.IntegerField(null=True, blank=True)

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
        return self.village_set.aggregate(Count('session__case')).get('session__case__count')

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
    owner_chain = models.TextField(blank=True)
    earliest_case = models.ForeignKey('Case', null=True, blank=True, related_name='land_to_earliest_case+')
    latest_case = models.ForeignKey('Case', null=True, blank=True, related_name='land_to_latest_case+')

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
    hundred = models.ForeignKey(Hundred, null=True, blank=True,)
    # listed as Ancient Demesne in 1334 Feudal Aid.
    ancient_demesne = models.BooleanField(default=False)
    # Part of the "Great Rumor" petition of 1377.
    great_rumor = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    @property
    def case_count(self):
        return self.session_set.aggregate(Count('case')).get('case__count')

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

    @property
    def monetary_counts(self):
        return self.session_set.aggregate(amercement_count=Count('case__litigants__amercement'),
                                          amercement_max=Max('case__litigants__amercement__in_denarius'),
                                          amercement_min=Min('case__litigants__amercement__in_denarius'),
                                          amercement_avg=Avg('case__litigants__amercement__in_denarius'),
                                          amercement_sum=Sum('case__litigants__amercement__in_denarius'),
                                          fine_count=Count('case__litigants__fine'),
                                          fine_max=Max('case__litigants__fine__in_denarius'),
                                          fine_min=Min('case__litigants__fine__in_denarius'),
                                          fine_avg=Avg('case__litigants__fine__in_denarius'),
                                          fine_sum=Sum('case__litigants__fine__in_denarius'),
                                          damage_count=Count('case__litigants__damage'),
                                          damage_avg=Avg('case__litigants__damage__in_denarius'),
                                          damage_sum=Sum('case__litigants__damage__in_denarius'),
                                          chevage_count=Count('case__litigants__chevage'),
                                          chevage_max=Max('case__litigants__chevage__in_denarius'),
                                          chevage_min=Min('case__litigants__chevage__in_denarius'),
                                          chevage_avg=Avg('case__litigants__chevage__in_denarius'),
                                          chevage_sum=Sum('case__litigants__chevage__in_denarius'),
                                          heriot_count=Count('case__litigants__heriot'),
                                          heriot_max=Max('case__litigants__heriot__in_denarius'),
                                          heriot_min=Min('case__litigants__heriot__in_denarius'),
                                          heriot_avg=Avg('case__litigants__heriot__in_denarius'),
                                          heriot_sum=Sum('case__litigants__heriot__in_denarius'),
                                          impercamentum_count=Count('case__litigants__impercamentum'),
                                          impercamentum_max=Max('case__litigants__impercamentum__in_denarius'),
                                          impercamentum_min=Min('case__litigants__impercamentum__in_denarius'),
                                          impercamentum_avg=Avg('case__litigants__impercamentum__in_denarius'),
                                          impercamentum_sum=Sum('case__litigants__impercamentum__in_denarius') )

    @property
    def median_chevage(self):
        queryset = Litigant.objects.all().filter(case__session__village=self.id).filter(chevage__isnull=False)
        return median_value(queryset, 'chevage__in_denarius')

    @property
    def median_heriot(self):
        queryset = Litigant.objects.all().filter(case__session__village=self.id).filter(heriot__isnull=False)
        return median_value(queryset, 'heriot__in_denarius')

    @property
    def median_damage(self):
        queryset = Litigant.objects.all().filter(case__session__village=self.id).filter(damage__isnull=False)
        return median_value(queryset, 'damage__in_denarius')

    @property
    def median_fine(self):
        queryset = Litigant.objects.all().filter(case__session__village=self.id).filter(fine__isnull=False)
        return median_value(queryset, 'fine__in_denarius')

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
    relation_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)
    status = models.IntegerField(choices=STATUS_CHOICES)
    village = models.ForeignKey(Village)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    # both taxes are to be input in denari.
    tax_1332 = models.FloatField(null=True, blank=True)
    tax_1379 = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    earliest_case = models.ForeignKey('Case', null=True, blank=True, related_name='person_to_earliest_case+')
    latest_case = models.ForeignKey('Case', null=True, blank=True, related_name='person_to_latest_case+')

    # Used to check if a person has amercements, fines, etc. in templates.
    # TODO: Update to reflect change in amercement, fines, etc. model structure.
    @property
    def pledges_given_count(self):
        return self.pledge_giver.all().count()

    @property
    def pledges_received_count(self):
        pledge_count = self.cases.aggregate(pledge_count=Count('pledges', distinct=True))
        pledge_count = pledge_count['pledge_count']
        return pledge_count

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
        return self.cases.exists()

    @property
    def land_exists(self):
        return self.cases.filter(land__isnull=False).exists()

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
        pledge_exists = False
        pledge_given = self.pledge_giver.exists()
        pledge_received = False
        for case in self.cases.all():
            if case.pledges.exists():
                pledge_received = True
        if pledge_given or pledge_received:
            return True
        else:
            return False

    @property
    def monetary_counts(self):
        return self.cases.aggregate(amercement_count=Count('amercements'),
                                             amercement_max=Max('amercements__in_denarius'),
                                             amercement_min=Min('amercements__in_denarius'),
                                             amercement_avg=Avg('amercements__in_denarius'),
                                             amercement_sum=Sum('amercements__in_denarius'), fine_count=Count('fines'),
                                             fine_max=Max('fines__in_denarius'), fine_min=Min('fines__in_denarius'),
                                             fine_avg=Avg('fines__in_denarius'), fine_sum=Sum('fines__in_denarius'),
                                             damage_count=Count('damages'), damage_max=Max('damages__in_denarius'),
                                             damage_min=Min('damages__in_denarius'),
                                             damage_avg=Avg('damages__in_denarius'),
                                             damage_sum=Sum('damages__in_denarius'), capitagium_count=Count('capitagia'),
                                             capitagium_max=Max('capitagia__in_denarius'),
                                             capitagium_min=Min('capitagia__in_denarius'),
                                             capitagium_avg=Avg('capitagia__in_denarius'),
                                             capitagium_sum=Sum('capitagia__in_denarius'), heriot_count=Count('heriots'),
                                             heriot_max=Max('heriots__in_denarius'),
                                             heriot_min=Min('heriots__in_denarius'),
                                             heriot_avg=Avg('heriots__in_denarius'),
                                             heriot_sum=Sum('heriots__in_denarius'),
                                             impercamentum_count=Count('impercamenta'),
                                             impercamentum_max=Max('impercamenta__in_denarius'),
                                             impercamentum_min=Min('impercamenta__in_denarius'),
                                             impercamentum_avg=Avg('impercamenta__in_denarius'),
                                             impercamentum_sum=Sum('impercamenta__in_denarius') )

    @property
    def amercement_exists(self):
        return self.cases.filter(amercements__isnull=False).exists()

    @property
    def fine_exists(self):
        return self.cases.filter(fines__isnull=False).exists()

    @property
    def damage_exists(self):
        return self.cases.filter(damages__isnull=False).exists()

    @property
    def chevage_exists(self):
        return self.cases.filter(capitagia__isnull=False).exists()

    @property
    def impercamentum_exists(self):
        return self.cases.filter(impercamenta__isnull=False).exists()

    @property
    def heriot_exists(self):
        return self.cases.filter(heriots__isnull=False).exists()

    @property
    def case_count_litigation(self):
        case_count = self.cases.exclude(capitagia__isnull=False).values_list('case').distinct().count()
        return case_count

    @property
    def capitagium_count(self):
        capitagium_count = self.cases.exclude(capitagia__isnull=True).values_list('case').distinct().count()
        return capitagium_count

    @property
    def case_count_all(self):
        case_count = len(set(self.cases.values_list('case')))
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
    reel = models.IntegerField(null=True, blank=True)
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
        return self.session_set.aggregate(Count('case')).get('case__count')


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
    notes = models.TextField(blank=True)

    @property
    def case_count(self):
        return self.case_set.count()

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
        return '%s - %s, %s %s' % (self.id, self.village.name, self.get_law_term_display(), self.date.year)


class Case(models.Model):

    COURT_TYPES = {
        (1, 'Hallmoot'),
        (2, 'Tourn'),
        (3, 'Impercamentum'),
        (4, 'Chevage'),
        (5, 'Unknown'),
        (6, 'Account Roll'),
    }

    summary = models.TextField(blank=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    case_type = models.ForeignKey(CaseType)
    court_type = models.IntegerField(choices=COURT_TYPES)
    verdict = models.ForeignKey(Verdict)
    of_interest = models.BooleanField()
#   started ad legem at Case 578.
    ad_legem = models.BooleanField()
    villeinage_mention = models.BooleanField()
    active_sale = models.BooleanField()
    incidental_land = models.BooleanField()

    @property
    def litigant_list(self):
        # iterate through a case's litigant set (litigants) and create a list of dictionaries containing the  name
        # and role for each person.
        litigant_list = [{"id": person.person.id, "name": person.person.full_name, "role": person.role.role} for person in self.litigants.all()]
        return litigant_list

    @property
    def litigant_count(self):
        litigants = [(x) for x in self.litigants.values_list('person_id', flat=True)]
        number_of_litigants = len(set(litigants))
        return number_of_litigants

    @property
    def pledge_count(self):
        pledge_count = []
        for case in self.litigants.all():
            for pledge in case.pledges.all():
                pledge_count.append(pledge.giver_id)
                pledge_count.append(pledge.receiver_id)
        pledge_count = len(set(pledge_count))
        return pledge_count

    @property
    def litigant_exist(self):
        return self.litigants.filter(person__isnull=False).exists()

    @property
    def land_exist(self):
        return self.litigants.filter(land__isnull=False).exists()

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
        pledge_exists = False
        for case in self.litigants.all():
            if case.pledges.exists():
                pledge_exists = True
        return pledge_exists

    def __str__(self):
        return 'Case %s | %s (%s / %s)' % (self.id, self.session.village.name, self.session.get_law_term_display(), self.session.date.year)


class Cornbot(models.Model):
    amount = models.CharField(max_length=50)
    crop_type = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='cornbot')
    notes = models.TextField(blank=True)


class Extrahura(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='extrahura')


class Murrain(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='murrain')
    notes = models.TextField(blank=True)


class PlaceMentioned(models.Model):

    class Meta:
        verbose_name_plural = "Places Mentioned"

    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)


class Litigant(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='cases')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='litigants')
    role = models.ForeignKey(Role, related_name='litigant_role')
    fine = models.ForeignKey(Money, null=True, blank=True, related_name='litigant_fine')
    amercement = models.ForeignKey(Money, null=True, blank=True, related_name='litigant_amercement')
    damage = models.ForeignKey(Money, null=True, blank=True, related_name='litigant_damages')
    damage_notes = models.TextField(blank=True,)
    ad_proximum = models.BooleanField()
    distrained = models.BooleanField()
    # Added at Case 1189.
    attached = models.BooleanField()
    # Added at Case 1424
    bail = models.BooleanField()
    chevage = models.ForeignKey(Money, null=True, blank=True, related_name='litigant_chevage')
    crossed = models.NullBooleanField()
    recessit = models.NullBooleanField()
    habet_terram = models.NullBooleanField()
    chevage_notes = models.TextField(blank=True)
    heriot_quantity = models.CharField(max_length=25, blank=True,)
    heriot_animal = models.ForeignKey(Chattel, null=True, related_name='heriot_animal')
    heriot = models.ForeignKey(Money, null=True, blank=True, related_name='heriot_assessment')
    impercamentum_quantity = models.IntegerField(null=True, blank=True,)
    impercamentum_animal = models.ForeignKey(Chattel, null=True, blank=True, related_name='impercamentum_animal')
    impercamentum = models.ForeignKey(Money, null=True, blank=True, related_name='impercamentum_amercement')
    impercamentum_notes = models.TextField(blank=True,)
    land = models.ForeignKey(Land, null=True, blank=True, on_delete=models.CASCADE, related_name='case_to_land')
    land_villeinage = models.NullBooleanField()
    land_notes = models.TextField(blank=True,)

    # Used to check if a litigant has amercements, fines, etc. in templates.
    @property
    def amercement_exists(self):
        return self.amercements.exists()
    
    @property
    def damage_exists(self):
        return self.damages.exists()
    
    @property
    def capitagium_exists(self):
        return self.capitagia.exists()

    @property
    def fine_exists(self):
        return self.fines.exists()
    
    @property
    def heriot_exists(self):
        return self.heriots.exists()
    
    @property
    def impercamentum_exists(self):
        return self.impercamenta.exists()
    
    @property
    def land_exists(self):
        return self.lands.exists()

    @property
    def pledge_exists(self):
        return self.pledges.exists()

    def save(self, *args, **kwargs):
        person = Person.objects.get(id=self.person_id)
        try:
            earliest_case = person.earliest_case
            if self.case.session.date <= earliest_case.session.date:
                person.earliest_case = self.case
                person.save()
        except:
            person.earliest_case = self.case
            person.save()
        try:
            latest_case = person.latest_case
            if self.case.session.date >= latest_case.session.date:
                person.latest_case = self.case
                person.save()
        except:
            person.latest_case = self.case
            person.save()
        super(Litigant, self).save(*args, **kwargs)


class Fine(models.Model):

    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='fines')
    fine = models.ForeignKey(Money)


class Amercement(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='amercements')
    amercement = models.ForeignKey(Money)


class Damage(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='damages')
    damage = models.ForeignKey(Money)
    notes = models.TextField(blank=True)


class Capitagium(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='capitagia')
    capitagium = models.ForeignKey(Money)
    notes = models.TextField(blank=True,)
    crossed = models.NullBooleanField()
    recessit = models.NullBooleanField()
    habet_terram = models.NullBooleanField()
    mortuus = models.NullBooleanField()


class Heriot(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='heriots')
    quantity = models.CharField(max_length=25, blank=True,)
    animal = models.ForeignKey(Chattel, null=True)
    heriot = models.ForeignKey(Money)


class Impercamentum(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='impercamenta')
    quantity = models.IntegerField(null=True, blank=True)
    animal = models.ForeignKey(Chattel, null=True, blank=True)
    impercamentum = models.ForeignKey(Money)
    notes = models.TextField(blank=True)


class LandtoCase(models.Model):
    litigant = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='lands')
    land = models.ForeignKey(Land, null=True, blank=True, on_delete=models.CASCADE)
    villeinage = models.NullBooleanField()
    notes = models.TextField(blank=True,)


class Pledge(models.Model):
    giver = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='pledge_giver')
    receiver = models.ForeignKey(Litigant, on_delete=models.CASCADE, related_name='pledges')

    def __str__(self):
        return "%s pledged %s" % (self.giver.full_name, self.receiver.person.full_name)


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
