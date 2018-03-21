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
    url(r'^list/$', views.ArchiveListView.as_view(template_name='archive/_archive_list.html'),
        name='list'),
    url(r'^(?P<pk>\d+)/$', views.ArchiveDetailView.as_view(template_name='archive/_archive_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/record_list', views.ArchiveDetailView.as_view(template_name='archive/record_list.html'),
        name='records'),
    url(r'^add/$', views.ArchiveAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', views.ArchiveEditView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.ArchiveDeleteView.as_view(), name='delete'),

]

case_urls = [
    url(r'^list/$', views.CaseListView.as_view(template_name='case/_case_list.html'), name='list'),
    url(r'^(?P<pk>\d+)/$', views.CaseDetailView.as_view(template_name='case/_case_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/litigant_list', views.case_lists,
        name='litigants'),
    url(r'^(?P<pk>\d+)/land_list', views.CaseListView.as_view(template_name='case/case_land_list.html'), name='land'),
    url(r'^(?P<pk>\d+)/extrahura_list', views.CaseListView.as_view(template_name='case/case_extrahura_list.html'),
        name='extrahura'),
    url(r'^(?P<pk>\d+)/cornbot_list', views.CaseListView.as_view(template_name='case/case_cornbot_list.html'),
        name='cornbot'),
    url(r'^(?P<pk>\d+)/murrain_list', views.CaseListView.as_view(template_name='case/case_murrain_list.html'),
        name='murrain'),
    url(r'^(?P<pk>\d+)/place_mentioned_list', views.CaseListView.as_view(template_name='case/case_place_mentioned_list.html'),
        name='places_mentioned'),
    url(r'^(?P<pk>\d+)/pledge_list', views.CaseListView.as_view(template_name='case/case_pledge_list.html'),
        name='pledges'),
    url(r'^add/$', views.add_case, name='add'),
    url(r'^(?P<pk>\d+)/edit/$', views.CaseEditView, name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.CaseDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/litigants/$', views.LitigantListforAddCase.as_view(template_name='case/litigant_table_body_for_case.html')
        , name='litigant_list_for_add_case'),
    url(r'^(?P<pk>\d+)/add_litigant/$', views.add_litigant, name='add_litigant'),
    url(r'^ajax/load_case_types/', views.load_case_types, name='ajax_case_types'),
    url(r'^ajax/load_verdict_types/', views.load_verdict_types, name='ajax_verdict_types'),
]

county_urls = [
    url(r'^(?P<pk>\d+)/$', views.CountyDetailView.as_view(template_name='county/_county_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/village_list$', views.CountyDetailView.as_view(template_name='county/county_village_list.html'),
        name='villages'),
    url(r'^(?P<pk>\d+)/case_list$', views.CaseListView.as_view(template_name='county/county_case_list.html'),
        name='cases'),
    url(r'^(?P<pk>\d+)/resident_list$', views.CaseListView.as_view(template_name='county/county_resident_list.html'),
        name='residents'),
    url(r'^(?P<pk>\d+)/litigant_list$', views.CaseListView.as_view(template_name='county/county_litigant_list.html'),
        name='litigants'),
    url(r'^(?P<pk>\d+)/hundred_list$', views.CaseListView.as_view(template_name='county/county_hundred_list.html'),
        name='hundreds'),
    url(r'^list/$', views.CountyListView.as_view(template_name='county/_county_list.html'),
        name='list'),
]

hundred_urls = [
    url(r'^(?P<pk>\d+)/$', views.HundredDetailView.as_view(template_name='hundred/_hundred_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/case_list$', views.HundredListView.as_view(template_name='hundred/hundred_case_list.html'),
        name='cases'),
    url(r'^(?P<pk>\d+)/resident_list$', views.CaseListView.as_view(template_name='hundred/hundred_resident_list.html'),
        name='residents'),
    url(r'^(?P<pk>\d+)/litigant_list$', views.CaseListView.as_view(template_name='hundred/hundred_litigant_list.html'),
        name='litigants'),
    url(r'^(?P<pk>\d+)/village_list$', views.CaseListView.as_view(template_name='hundred/hundred_village_list.html'),
        name='villages'),
    url(r'^list/$', views.HundredListView.as_view(template_name='hundred/_hundred_list.html'),
        name='list'),
]

land_urls = [
    url(r'^(?P<pk>\d+)/$', views.LandDetailView.as_view(template_name='land/_land_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/tenants', views.LandDetailView.as_view(template_name='land/tenant_history.html'), name='tenants'),
    url(r'^(?P<pk>\d+)/split_history', views.LandDetailView.as_view(template_name='land/land_split_history.html'),
        name='split_history'),
    url(r'^(?P<pk>\d+)/case_history', views.LandDetailView.as_view(template_name='land/land_case_history.html'),
        name='cases'),
    url(r'^list/$', views.LandListView.as_view(template_name='land/_land_list.html'), name='list'),
]

litigant_urls = [
    url(r'^(?P<pk>\d+)/delete', views.delete_litigant, name='delete'),
    url(r'^(?P<pk>\d+)/edit', views.edit_litigant, name='edit'),
]

person_detail_urls = [
    url(r'^(?P<pk>\d+)/$', views.PersonDetailView.as_view(template_name='person/_person_detail.html'),
        name='detail'),
    url(r'^(?P<pk>\d+)/amercement_list', views.person_lists,
        name='amercements'),
    url(r'^(?P<pk>\d+)/case_list', views.person_lists,
        name='cases'),
    url(r'^(?P<pk>\d+)/capitagium_list', views.person_lists,
        name='capitagium'),
    url(r'^(?P<pk>\d+)/damage_list', views.person_lists,
        name='damages'),
    url(r'^(?P<pk>\d+)/fine_list', views.person_lists,
        name='fines'),
    url(r'^(?P<pk>\d+)/heriot_list', views.person_lists,
        name='heriots'),
    url(r'^(?P<pk>\d+)/impercamentum_list', views.person_lists,
        name='impercamenta'),
    url(r'^(?P<pk>\d+)/land_list', views.person_lists,
        name='lands'),
    url(r'^(?P<pk>\d+)/pledges', views.person_lists,
        name='pledges'),
    url(r'^(?P<pk>\d+)/pledges_given_list', views.person_lists,
        name='pledges_given'),
    url(r'^(?P<pk>\d+)/pledges_received_list', views.person_lists,
        name='pledges_received'),
    url(r'^(?P<pk>\d+)/position_list', views.person_lists,
        name='positions'),
    url(r'^(?P<pk>\d+)/relationship_list', views.person_lists,
        name='relationships'),
    url(r'^(?P<pk>\d+)/stats_list', views.PersonDetailView.as_view(template_name='person/stats_list.html'),
        name='stats'),
    url(r'^list/$', views.PeopleListView.as_view(template_name='person/_person_list.html'),
        name='list'),
]

record_urls = [
    url(r'^(?P<pk>\d+)/$', views.RecordDetailView.as_view(template_name='record/_record_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/session_list$', views.RecordDetailView.as_view(template_name='record/record_session_list.html'),
        name='sessions'),
    url(r'^add/$', views.RecordAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', views.RecordEditView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.RecordDeleteView.as_view(), name='delete'),
    url(r'^list/$', views.RecordListView.as_view(template_name='record/_record_list.html'), name='list'),
]

session_urls = [
    url(r'^list/$', views.SessionListView.as_view(template_name='session/_session_list.html'),
        name='list'),
    url(r'^(?P<pk>\d+)/$', views.SessionDetailView.as_view(template_name='session/_session_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/case_list$', views.CaseListView.as_view(template_name='session/session_case_list.html'),
        name='cases'),
    url(r'^add/$', views.SessionAddView.as_view(), name='add'),
    url(r'^(?P<pk>\d+)/edit/$', views.SessionEditView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.SessionDeleteView.as_view(), name='delete'),
]

village_urls = [
    url(r'^(?P<pk>\d+)/$', views.VillageDetailView.as_view(template_name='village/_village_detail.html'), name='detail'),
    url(r'^(?P<pk>\d+)/case_list$', views.CaseListView.as_view(template_name='village/village_case_list.html'),
        name='cases'),
    url(r'^(?P<pk>\d+)/resident_list$', views.PersonDetailView.as_view(template_name='village/village_resident_list.html'),
        name='residents'),
    url(r'^(?P<pk>\d+)/litigant_list$', views.PersonDetailView.as_view(template_name='village/village_litigant_list.html'),
        name='litigants'),
    url(r'^(?P<pk>\d+)/places_mentioned_list$', views.VillageListView.as_view(
        template_name='village/village_place_mentioned_list.html'), name='places_mentioned'),
    url(r'^(?P<pk>\d+)/related_places$', views.VillageListView.as_view(template_name='village/village_related_places_list.html'),
        name='related_places'),
    url(r'^(?P<pk>\d+)/session_list$', views.SessionListView.as_view(template_name='village/village_session_list.html'),
        name='sessions'),
    url(r'^list/$', views.VillageListView.as_view(template_name='village/_village_list.html'),
        name='list'),

]

# consolidation of detail views.
urlpatterns = [
    url(r'^', include(index_urls)),
    url(r'^archive/', include(archive_urls, namespace='archive')),
    url(r'^case/', include(case_urls, namespace='case')),
    url(r'^county/', include(county_urls, namespace='county')),
    url(r'^hundred/', include(hundred_urls, namespace='hundred')),
    url(r'^land/', include(land_urls, namespace='land')),
    url(r'^litigant/', include(litigant_urls, namespace='litigant')),
    url(r'^person/', include(person_detail_urls, namespace='person')),
    url(r'^record/', include(record_urls, namespace='record')),
    url(r'^session/', include(session_urls, namespace='session')),
    url(r'^village/', include(village_urls, namespace='village')),
    url(r'^analysis/', include(analysis_urls))
]

# list views.
urlpatterns += [


]