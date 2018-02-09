from django.conf.urls import url, include
from django.views.generic import TemplateView

from peasantlegaldb import views

index_urls = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]

analysis_urls = [
    url(r'^chevage/(?P<village_pk>[0-9]+)/$', views.ChevageAnalysisListView.as_view(
        template_name='analysis/chevage.html'), name='chevage_analysis'),
]

archive_urls = [
    url(r'^$', views.ArchiveDetailView.as_view(template_name='archive/_archive_detail.html'), name='archive'),
    url(r'^record_list$', views.ArchiveDetailView.as_view(template_name='archive/record_list.html'),
        name='record_list'),
    url(r'^edit/$', views.ArchiveEditView.as_view(), name='edit_archive'),
    url(r'^delete/$', views.ArchiveDeleteView.as_view(), name='delete_archive'),
]

case_urls = [
    url(r'^$', views.CaseDetailView.as_view(template_name='case/_case_detail.html'), name='case'),
    url(r'^litigant_list', views.LitigantListView.as_view(template_name='case/case_litigant_list.html'),
        name='case_litigant_list'),
    url(r'^land_list', views.CaseListView.as_view(template_name='case/case_land_list.html'), name='case_land_list'),
    url(r'^extrahura_list', views.CaseListView.as_view(template_name='case/case_extrahura_list.html'),
        name='case_extrahura_list'),
    url(r'^cornbot_list', views.CaseListView.as_view(template_name='case/case_cornbot_list.html'),
        name='case_cornbot_list'),
    url(r'^murrain_list', views.CaseListView.as_view(template_name='case/case_murrain_list.html'),
        name='case_murrain_list'),
    url(r'^place_mentioned_list', views.CaseListView.as_view(template_name='case/case_place_mentioned_list.html'),
        name='case_place_mentioned_list'),
    url(r'^pledge_list', views.CaseListView.as_view(template_name='case/case_pledge_list.html'),
        name='case_pledge_list'),
    url(r'^edit/$', views.CaseEditView, name='edit_case'),
    url(r'^delete/$', views.CaseDeleteView.as_view(), name='delete_case'),
    url(r'^litigants/$', views.LitigantListforAddCase.as_view(template_name='case/case_litigant_list_for_add_case.html')
        , name='litigant_list_for_add_case')
]

county_urls = [
    url(r'^$', views.CountyDetailView.as_view(template_name='county/_county_detail.html'), name='county'),
    url(r'^village_list$', views.CountyDetailView.as_view(template_name='county/county_village_list.html'),
        name='county_village_list'),
    url(r'^case_list$', views.CaseListView.as_view(template_name='county/county_case_list.html'),
        name='county_case_list'),
    url(r'^resident_list$', views.CaseListView.as_view(template_name='county/county_resident_list.html'),
        name='county_resident_list'),
    url(r'^litigant_list$', views.CaseListView.as_view(template_name='county/county_litigant_list.html'),
        name='county_litigant_list'),
    url(r'^hundred_list$', views.CaseListView.as_view(template_name='county/county_hundred_list.html'),
        name='county_hundred_list'),
]

hundred_urls = [
    url(r'^$', views.HundredDetailView.as_view(template_name='hundred/_hundred_detail.html'), name='hundred'),
    url(r'^case_list$', views.HundredListView.as_view(template_name='hundred/hundred_case_list.html'),
        name='hundred_case_list'),
    url(r'^resident_list$', views.CaseListView.as_view(template_name='hundred/hundred_resident_list.html'),
        name='hundred_resident_list'),
    url(r'^litigant_list$', views.CaseListView.as_view(template_name='hundred/hundred_litigant_list.html'),
        name='hundred_litigant_list'),
    url(r'^village_list$', views.CaseListView.as_view(template_name='hundred/hundred_village_list.html'),
        name='hundred_village_list'),
]

land_urls = [
    url(r'^$', views.LandDetailView.as_view(template_name='land/_land_detail.html'), name='land'),
    url(r'^tenants', views.LandDetailView.as_view(template_name='land/tenant_history.html'), name='tenant_history'),
    url(r'^split_history', views.LandDetailView.as_view(template_name='land/land_split_history.html'),
        name='land_split_history'),
    url(r'^case_history', views.LandDetailView.as_view(template_name='land/land_case_history.html'),
        name='land_case_history'),
]

litigant_urls = [
    url(r'^add', views.add_litigant, name='add_litigant'),
    url(r'^edit/(?P<id>\d+)/', views.edit_litigant, name='edit_litigant'),
]


person_detail_urls = [
    url(r'^$', views.PersonDetailView.as_view(template_name='person/_person_detail.html'), name='person'),
    url(r'^case_list', views.PeopleListView.as_view(template_name='person/person_case_list.html'),
        name='person_case_list'),
    url(r'^pledge_list', views.PeopleListView.as_view(template_name='person/pledge_list.html'), name='pledge_list'),
    url(r'^relationship_list', views.PeopleListView.as_view(template_name='person/relationship_list.html'),
        name='relationship_list'),
    url(r'^position_list', views.PeopleListView.as_view(template_name='person/position_list.html'),
        name='position_list'),
    url(r'^land_list', views.PeopleListView.as_view(template_name='person/person_land_history_list.html'),
        name='person_land_history'),
    url(r'^stats', views.PersonDetailView.as_view(template_name='person/person_stats.html'), name='person_stats'),
    url(r'^amercement_list', views.PersonDetailView.as_view(template_name='person/person_amercement_cases.html'),
        name='person_amercement_list'),
    url(r'^fine_list', views.PersonDetailView.as_view(template_name='person/person_fine_cases.html'),
        name='person_fine_list'),
    url(r'^damage_list', views.PersonDetailView.as_view(template_name='person/person_damage_cases.html'),
        name='person_damage_list'),
    url(r'^chevage_list', views.PersonDetailView.as_view(template_name='person/person_chevage_cases.html'),
        name='person_chevage_list'),
    url(r'^impercamentum_list', views.PersonDetailView.as_view(
        template_name='person/person_impercamentum_cases.html'), name='person_impercamentum_list'),
    url(r'^heriot_list', views.PersonDetailView.as_view(template_name='person/person_heriot_cases.html'),
        name='person_heriot_list'),
]

record_urls = [
    url(r'^$', views.RecordDetailView.as_view(template_name='record/_record_detail.html'), name='record'),
    url(r'^session_list$', views.RecordDetailView.as_view(template_name='record/record_session_list.html'),
        name='record_session_list'),
    url(r'^edit/$', views.RecordEditView.as_view(), name='edit_record'),
    url(r'^delete/$', views.RecordDeleteView.as_view(), name='delete_record'),
]

session_urls = [
    url(r'^$', views.SessionDetailView.as_view(template_name='session/_session_detail.html'), name='session'),
    url(r'^case_list$', views.CaseListView.as_view(template_name='session/session_case_list.html'),
        name='session_case_list'),
    url(r'^edit/$', views.SessionEditView.as_view(), name='edit_session'),
    url(r'^delete/$', views.SessionDeleteView.as_view(), name='delete_session'),
]

village_urls = [
    url(r'^$', views.VillageDetailView.as_view(template_name='village/_village_detail.html'), name='village'),
    url(r'^case_list$', views.CaseListView.as_view(template_name='village/village_case_list.html'),
        name='village_case_list'),
    url(r'^resident_list$', views.PersonDetailView.as_view(template_name='village/village_resident_list.html'),
        name='village_resident_list'),
    url(r'^litigant_list$', views.PersonDetailView.as_view(template_name='village/village_litigant_list.html'),
        name='village_litigant_list'),
    url(r'^places_mentioned_list$', views.VillageListView.as_view(
        template_name='village/village_place_mentioned_list.html'), name='village_places_mentioned_list'),
    url(r'^related_places$', views.VillageListView.as_view(template_name='village/village_related_places_list.html'),
        name='village_related_places_list'),
    url(r'^session_list$', views.SessionListView.as_view(template_name='village/village_session_list.html'),
        name='village_session_list'),

]

# consolidation of detail views.
urlpatterns = [
    url(r'^', include(index_urls)),
    url(r'^archive/(?P<pk>\d+)/', include(archive_urls)),
    url(r'^archive/add/$', views.ArchiveAddView.as_view(), name='add_archive'),
    url(r'^case/(?P<pk>\d+)/', include(case_urls)),
    url(r'^case/add/$', views.CaseAddView, name='add_case'),
    url(r'^county/(?P<pk>\d+)/', include(county_urls)),
    url(r'^hundred/(?P<pk>\d+)/', include(hundred_urls)),
    url(r'^land/(?P<pk>\d+)/', include(land_urls)),
    url(r'^litigant/', include(litigant_urls)),
    url(r'^person/(?P<pk>\d+)/', include(person_detail_urls)),
    url(r'^record/(?P<pk>\d+)/', include(record_urls)),
    url(r'^record/add/$', views.RecordAddView.as_view(), name='add_record'),
    url(r'^session/(?P<pk>\d+)/', include(session_urls)),
    url(r'^session/add/$', views.SessionAddView.as_view(), name='add_session'),
    url(r'^village/(?P<pk>\d+)/', include(village_urls)),
    url(r'^analysis/', include(analysis_urls))
]

# list views.
urlpatterns += [
    url(r'^archives/$', views.ArchiveListView.as_view(template_name='archive/_archive_list.html'),
        name='archive_list'),
    url(r'^people/$', views.PeopleListView.as_view(template_name='person/_person_list.html'), name='person_list'),
    url(r'^cases/$', views.CaseListView.as_view(template_name='case/_case_list.html'), name='case_list'),
    url(r'^counties/$', views.CountyListView.as_view(template_name='county/_county_list.html'),
        name='county_list'),
    url(r'^hundreds/$', views.HundredListView.as_view(template_name='hundred/_hundred_list.html'),
        name='hundred_list'),

    url(r'^villages/$', views.VillageListView.as_view(template_name='village/_village_list.html'),
        name='village_list'),
    url(r'^archives/$', views.ArchiveListView.as_view(template_name='archive/_archive_list.html'),
        name='archive_list'),
    url(r'^records/$', views.RecordListView.as_view(template_name='record/_record_list.html'), name='record_list'),
    url(r'^sessions/$', views.SessionListView.as_view(template_name='session/_session_list.html'),
        name='session_list'),
    url(r'^lands/$', views.LandListView.as_view(template_name='land/_land_list.html'), name='land_list'),
]