from django.contrib import admin
from django.forms import Textarea
from .models import *

# Register non-m2m models
singularModels = [Archive, Money, Chattel, CaseType, ParcelTenure,
                  ParcelType, PositionType, Relation, Role, Verdict,
                  Hundred, Cornbot, Extrahura, Murrain, PlaceMentioned, CasePeopleLand,
                  Position, Relationship, Pledge, LandSplit, LandParcel,]

admin.site.register(singularModels)

# m2m models here


class HundredInline(admin.TabularInline):
    model = Hundred
    extra = 1


class LitigantInline(admin.TabularInline):
    model = Litigant
    extra = 1
    classes = ['collapse']


class CaseInline(admin.TabularInline):
    model = Case
    extra = 1
    classes = ['collapse']


class CasePeopleLandInline(admin.TabularInline):
    model = CasePeopleLand
    extra = 1
    classes = ['collapse']


class PeopleInline(admin.TabularInline):
    model = Person
    extra = 1
    classes = ['collapse']


class RelationshipInline(admin.TabularInline):
    model = Relationship
    fk_name = 'person_one'
    extra = 1
    classes = ['collapse']

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    classes = ['collapse']


class PlaceMentionedInline(admin.TabularInline):
    model = PlaceMentioned
    extra = 1
    classes = ['collapse']


class CornbotInline(admin.TabularInline):
    model = Cornbot
    extra = 1
    classes = ['collapse']

class ExtrahuraInline(admin.TabularInline):
    model = Extrahura
    extra = 1
    classes = ['collapse']


class MurrainInline(admin.TabularInline):
    model = Murrain
    extra = 1
    classes = ['collapse']

class LandInline(admin.TabularInline):
    model = Land
    extra = 1
    classes = ['collapse']


class LandSplitInline(admin.TabularInline):
    model = LandSplit
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    inlines = [
        LitigantInline,
        RelationshipInline,
    ]


class LandAdmin(admin.ModelAdmin):
    inlines = [
        CasePeopleLandInline,
    ]


class CountyAdmin(admin.ModelAdmin):
    inlines = [
        HundredInline,
    ]


class VillageAdmin(admin.ModelAdmin):
    inlines = [
        PeopleInline,
    ]


class RecordAdmin(admin.ModelAdmin):
    inlines = [
        SessionInline,
    ]


class SessionAdmin(admin.ModelAdmin):
    inlines = [
        CaseInline,
    ]


class CaseAdmin(admin.ModelAdmin):
    inlines = [
        LitigantInline,
        PlaceMentionedInline,
        CornbotInline,
        ExtrahuraInline,
        MurrainInline,

    ]

class LandParcelAdmin(admin.ModelAdmin):
    inlines = [
        CasePeopleLandInline,
    ]

class PledgeAdmin(admin.ModelAdmin):
    inlines = [
        PeopleInline,
    ]

class LandSplitAdmin(admin.ModelAdmin):
    inlines = [
        LandInline,
        CasePeopleLandInline,
    ]

class RelationshipAdmin(admin.ModelAdmin):
    inlines = [
        PeopleInline,
    ]

admin.site.register(Case, CaseAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Session, SessionAdmin)