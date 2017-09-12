from django.db import models
from django.db.models import Count


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
        ('V', 'Villein'),
        ('F', 'Free'),
        ('U', 'Unknown'),
        ('I', 'Institution')
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
    gender = models.IntegerField(choices=GENDER_CHOICES)
    # both taxes are to be input in denari.
    tax_1332 = models.FloatField()
    tax_1379 = models.FloatField()
    notes = models.TextField()

    def name_concat(self):
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
    ad_legem = models.BooleanField(default=False)
    villeinage_mention = models.BooleanField(default=False)
    active_sale = models.BooleanField(default=False)
    incidental_land = models.BooleanField(default=False)
    litigants = models.ManyToManyField(Person, through='Litigant')

    @property
    def litigant_count(self):
        # create a list of all litigants across all types of litigation tables (litigants, chevage, heriot, land, etc.)
        # and check for duplicates to get an accurate count of unique litigants. This technique is required because Django
        # only allows for Count Distinct in queryset creation, which is called with the view. Since SPA doesn't call views,
        # this approach would clearly not work.
        litigants = []
        a = self.case_to_person.values_list('person_id', flat=True)
        try:
            for x in a:
                litigants.append(x)
        except:
            pass
        b = self.case_to_chevage.values_list('person_id', flat=True)
        try:
            for x in b:
                litigants.append(x)
        except:
            pass
        c = self.case_to_heriot.values_list('person_id', flat=True)
        try:
            for x in c:
                litigants.append(x)
        except:
            pass
        d = self.case_to_impercamentum.values_list('person_id', flat=True)
        try:
            for x in d:
                litigants.append(x)
        except:
            pass
        e = self.case_to_land.values_list('person_id', flat=True)
        try:
            for x in e:
                litigants.append(x)
        except:
            pass
        f = self.case_to_pledge.values_list('pledge_giver_id', flat=True)
        try:
            for x in f:
                litigants.append(x)
        except:
            pass
        g = self.case_to_pledge.values_list('pledge_receiver_id', flat=True)
        try:
            for x in g:
                litigants.append(x)
        except:
            pass
        litigants = set(litigants)
        num = len(litigants)
        return num

    def __str__(self):
        return 'Case %s | %s (%s)' % (self.id, self.session.village.name, self.session.date.year)


class Chevage(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    amercement = models.ForeignKey(Money)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_chevage')
    cross = models.BooleanField(default=False)
    recessit = models.BooleanField(default=False)
    habet_terram = models.BooleanField(default=False)
    notes = models.TextField()


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


class Heriot(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_heriot')
    amount = models.CharField(max_length=25)
    animal = models.ForeignKey(Chattel)
    assessment = models.ForeignKey(Money)


class Impercamentum(models.Model):

    class Meta:
        verbose_name_plural = "Impercamenta"

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_impercamentum')
    amount = models.IntegerField()
    animal = models.ForeignKey(Chattel)
    amercement = models.ForeignKey(Money)
    notes = models.TextField()


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


class LandParcel(models.Model):

    class Meta:
        verbose_name = "Land Parcel"
        verbose_name_plural = "Land Parcels"

    #   fix null in land_id
    land = models.ForeignKey(Land, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    parcel_type = models.ForeignKey(ParcelType)
    parcel_tenure = models.ForeignKey(ParcelTenure)


class Litigant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_to_case')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_person')
    role = models.ForeignKey(Role, related_name='litigant_role')
    fine = models.ForeignKey(Money, null=True, related_name='litigant_fine')
    amercement = models.ForeignKey(Money, null=True, related_name='litigant_amercement')
    damage = models.ForeignKey(Money, null=True, related_name='litigant_damages')
    damage_notes = models.TextField()
    ad_proximum = models.BooleanField(default=False)
    distrained = models.BooleanField(default=False)
#   Added at Case 1189.
    attached = models.BooleanField(default=False)
#   Added at Case 1424
    bail = models.BooleanField(default=False)


class CasePeopleLand(models.Model):

    class Meta:
        verbose_name = "Case to Person to Land"
        verbose_name_plural = "Cases to People to Land"

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='case_to_land')
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    role = models.ForeignKey(Role)
    villeinage = models.BooleanField(default=False)
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

    def __str__(self):
        return "Old Land ID %s, New Land ID %s" % (self.old_land, self.new_land)

class Position(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.ForeignKey(PositionType)
    # rework so this is per case not per session.
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    definitive = models.BooleanField(default=False)

    def __str__(self):
        return self.PositionType.title


class Relationship(models.Model):
    person_one = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_one')
    person_two = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_two')
#   need to rework so relationships are more descriptive.
    relationship = models.ForeignKey(Relation)
    definitive = models.BooleanField(default=False)
