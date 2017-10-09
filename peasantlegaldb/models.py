from django.db import models
from django.db.models import Max, Min, Avg, Count
from itertools import chain

class Archive(models.Model):
    name = models.CharField(max_length=50)
    website = models.URLField()
    notes = models.TextField()

    def __str__(self):
        return self.name


class Money(models.Model):
    amount = models.CharField(max_length=150)
    in_denarius = models.IntegerField()

    def __str__(self):
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

    def __str__(self):
        return self.name


class Land(models.Model):
    #   Change save condition to automagically update notes field w/ land owners from CasePeopleLand?
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
        return parcel_list    \

    @property
    def parcel_list_concat(self):
        parcel_list = ""
        queryset = self.parcels.all().prefetch_related('parcel_type', 'parcel_tenure')
        try:
            first = True
            for x in queryset:
                parcel_list = parcel_list + str(x.amount) + " " + x.parcel_type.parcel_type + " held by " + \
                              x.parcel_tenure.tenure + "<hr>"
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
    parcel_type = models.ForeignKey(ParcelType)
    parcel_tenure = models.ForeignKey(ParcelTenure)


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
    notes = models.TextField()

    @property
    def earliest_case(self):
        # get queryset for each area where person interacts with cases (i.e. litigant table, casepeopleland, pledges),
        # chain together and sort by date using a lambda if/else statement to differentiate between Case and other
        # instances (b/c Case date is at self.session.date while all others are at self.case.session.date, b/c they use
        # case as an FK). Pop earliest case off based on index [0]. Check instance for Case or other (again, due to
        # difference in FK relationship w/ Session), and then render date display appropriately. Unfortunately, it
        # isn't possible to simply pass the model to the template for rendering (and manipulation), because of the FK
        # difference. There may be a way, but it's beyond me.

        case_range = self.case_set.all()
        land_range = self.casepeopleland_set.all()
        pledge_giver_range= self.pledge_giver.all()
        pledge_receiver_range = self.pledge_receiver.all()

        try:
            earliest_case = sorted(chain(case_range, land_range, pledge_giver_range, pledge_receiver_range), key=lambda
                x: x.session.date if isinstance(x, Case) else x.case.session.date)[0]
            if isinstance(earliest_case, Case):
                earliest_date = earliest_case.session.get_law_term_display() + ' - ' + str(earliest_case.session.date.
                                                                                           year)
            else:
                earliest_date = earliest_case.case.session.get_law_term_display() + ' - ' + str(earliest_case.case.
                                                                                                session.date.year)
        except:
            earliest_date = 'None'

        return earliest_date
    @property
    def latest_case(self):
        # get queryset for each area where person interacts with cases (i.e. litigant table, casepeopleland, pledges),
        # chain together and sort by date using a lambda if/else statement to differentiate between Case and other
        # instances (b/c Case date is at self.session.date while all others are at self.case.session.date, b/c they use
        # case as an FK). Pop latest case off based on index [0]. Check instance for Case or other (again, due to
        # difference in FK relationship w/ Session), and then render date display appropriately. Unfortunately, it
        # isn't possible to simply pass the model to the template for rendering (and manipulation), because of the FK
        # difference. There may be a way, but it's beyond me.

        case_range = self.case_set.all()
        land_range = self.casepeopleland_set.all()
        pledge_giver_range= self.pledge_giver.all()
        pledge_receiver_range = self.pledge_receiver.all()

        try:
            sorted_date = sorted(chain(case_range, land_range, pledge_giver_range, pledge_receiver_range), key=lambda
                x: x.session.date if isinstance(x, Case) else x.case.session.date, reverse=True)

            latest_case = sorted_date[0]
            if isinstance(latest_case, Case):
                latest_date = latest_case.session.get_law_term_display() + ' - ' + str(latest_case.session.date.
                                                                                           year)
            else:
                latest_date = latest_case.case.session.get_law_term_display() + ' - ' + str(latest_case.case.
                                                                                                session.date.year)
        except:
            latest_date = 'None'

        return latest_date


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
    def case_info(self):
        return self.person_to_case.aggregate(Count('amercement'), Max('amercement__in_denarius'),
                                                   Min('amercement__in_denarius'), Avg('amercement__in_denarius'),
                                                   Count('fine'), Max('fine__in_denarius'), Min('fine__in_denarius'),
                                                   Avg('fine__in_denarius'), Count('damage'),
                                                   Max('damage__in_denarius'), Min('damage__in_denarius'),
                                                   Avg('damage__in_denarius'), Count('chevage'),
                                                   Max('chevage__in_denarius'), Min('chevage__in_denarius'),
                                                   Avg('chevage__in_denarius'), Count('heriot_assessment'),
                                                   Max('heriot_assessment__in_denarius'),
                                                   Min('heriot_assessment__in_denarius'),
                                                   Avg('heriot_assessment__in_denarius'),
                                                   Count('impercamentum_amercement'),
                                                   Max('impercamentum_amercement__in_denarius'),
                                                   Min('impercamentum_amercement__in_denarius'),
                                                   Avg('impercamentum_amercement__in_denarius'), )

    @property
    def case_count_litigation(self):
        qs = self.person_to_case.exclude(chevage__isnull=False).exclude(heriot_assessment__isnull=False).\
            exclude(impercamentum_amercement__isnull=False).values_list('case').distinct()
        case_count = len(qs)
        return case_count

    @property
    def case_count_all(self):
        qs = self.person_to_case.values_list('case').distinct()
        case_count = len(qs)
        return case_count

    @property
    def full_name(self):
        if self.relation_name:
            concated_name = self.first_name + ' ' + self.relation_name + ' ' + self.last_name
        else:
            concated_name = self.first_name + ' ' + self.last_name
        return concated_name

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
    reel = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return self.name


class Session(models.Model):
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

    def __str__(self):
        return '%s %s %s Session.' % (self.village.name, self.get_law_term_display(), self.date.year)


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
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
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
    lands = models.ManyToManyField(Land, through='CasePeopleLand')

    @property
    def litigant_list(self):
        litigant_list = []
        litigant_qs = self.case_to_person.all()
        land_qs = self.case_to_land.all()
        try:
            iteration_list = list(chain(litigant_qs, land_qs))
            for x in iteration_list:
                new_entry = {
                    "name" : x.person.full_name,
                    "role" : x.role.role
                }
                litigant_list.append(new_entry)

        except:
            pass
        return litigant_list

    @property
    def litigant_list_concat(self):
        litigant_list = ""
        queryset = self.case_to_person.all().order_by('person__last_name')
        # need to include the HTML for the list in the function, so it will be served through the Datatables child row
        # correctly. Looking for solution - https://datatables.net/forums/discussion/44919?
        try:
            for x in queryset:
                litigant_list = litigant_list + "<div class=d-flex justify-content-end><div class='mr-auto p-0'><u>Name:" \
                                                "</u> " + x.person.id + ")>" + x.person.full_name + "</a></div> <div class='p-0'><u>Role:</u> " + \
                                                x.role.role + "</div></div><hr>"
        except:
            pass
        return litigant_list

    @property
    def litigant_count(self):
        # create a list of all litigants across all types of litigation tables (litigants, chevage, heriot, land, etc.)
        # and check for duplicates to get an accurate count of unique litigants. This technique is required because Django
        # only allows for Count Distinct in queryset creation, which is called with the view. Since SPA doesn't call views,
        # this approach would clearly not work.
        litigants = []
        qs1 = self.case_to_person.values_list('person_id', flat=True)
        try:
            for x in qs1:
                litigants.append(x)
        except:
            pass
        qs2 = self.case_to_land.values_list('person_id', flat=True)
        try:
            for x in qs2:
                litigants.append(x)
        except:
            pass
        qs3 = self.case_to_pledge.values_list('pledge_giver_id', flat=True)
        try:
            for x in qs3:
                litigants.append(x)
        except:
            pass
        qs4 = self.case_to_pledge.values_list('pledge_receiver_id', flat=True)
        try:
            for x in qs4:
                litigants.append(x)
        except:
            pass
        litigants = set(litigants)
        num = len(litigants)
        return num

    def __str__(self):
        return 'Case %s | %s (%s / %s)' % (self.id, self.session.village.name, self.session.get_law_term_display(), self.session.date.year)


class Cornbot(models.Model):
    amount = models.CharField(max_length=50)
    crop_type = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    notes = models.TextField()


class Extrahura(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    price = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)


class Murrain(models.Model):
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
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
#   Added at Case 1189.
    attached = models.NullBooleanField()
#   Added at Case 1424
    bail = models.NullBooleanField()
    chevage = models.ForeignKey(Money, null=True, related_name='litigant_chevage')
    crossed = models.NullBooleanField()
    recessit = models.NullBooleanField()
    habet_terram = models.NullBooleanField()
    chevage_notes = models.TextField(null=True)
    heriot_quantity = models.CharField(max_length=25, null=True)
    heriot_animal = models.ForeignKey(Chattel, null=True, related_name='heriot_animal')
    heriot_assessment = models.ForeignKey(Money, null=True, related_name='heriot_assessment')
    impercamentum_quantity = models.IntegerField(null=True)
    impercamentum_animal = models.ForeignKey(Chattel, null=True, related_name='impercamentum_animal')
    impercamentum_amercement = models.ForeignKey(Money, null=True, related_name='impercamentum_amercement')
    impercamentum_notes = models.TextField(null=True)
    land = models.ForeignKey(Land, null=True, on_delete=models.CASCADE, related_name='case_to_land')
    land_villeinage = models.NullBooleanField()
    land_notes = models.TextField(null=True)



class CasePeopleLand(models.Model):

    class Meta:
        verbose_name = "Case to Person to Land"
        verbose_name_plural = "Cases to People to Land"

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_land')
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    role = models.ForeignKey(Role)
    villeinage = models.NullBooleanField()
    notes = models.TextField()


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
#   need to rework so relationships are more descriptive.
    relationship = models.ForeignKey(Relation)
    definitive = models.BooleanField(default=False)
