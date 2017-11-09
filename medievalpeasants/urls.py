"""medievalpeasants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from rest_framework import routers

# REMEMBER TO RUN .manage.py collectstatic_js_reverse when adding new URLs or django_js_reverse won't pick them up.
from django_js_reverse.views import urls_js

from peasantlegaldb.api import views as api_views
from peasantlegaldb import views as web_views

from accounts import views as accounts_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^register/', accounts_views.register, name='register'),
    url(r'^register/', accounts_views.TemporaryRegistration.as_view(), name='register'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^index', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^reset/$', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'
    ),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'
    ),
]

# Map web views to URL Patterns

analysis_urls = [
    url(r'^chevage/(?P<village_pk>[0-9]+)/$', web_views.ChevageAnalysisListView.as_view(template_name='analysis/chevage.html'),
        name='chevage_analysis'
    ),
]

archive_urls = [
    url(r'^$', web_views.ArchiveDetailView.as_view(template_name='archive/_archive_detail.html'), name='archive'),
    url(r'^record_list$', web_views.ArchiveDetailView.as_view(template_name='archive/record_list.html'),
        name='record_list'),
]

case_urls = [
    url(r'^$', web_views.CaseDetailView.as_view(template_name='case/_case_detail.html'), name='case'),
    url(r'^litigant_list', web_views.LitigantListView.as_view(template_name='case/case_litigant_list.html'),
        name='case_litigant_list'),
    url(r'^land_list', web_views.CaseListView.as_view(template_name='case/case_land_list.html'), name='case_land_list'),
    url(r'^extrahura_list', web_views.CaseListView.as_view(template_name='case/case_extrahura_list.html'),
        name='case_extrahura_list'),
    url(r'^cornbot_list', web_views.CaseListView.as_view(template_name='case/case_cornbot_list.html'),
        name='case_cornbot_list'),
    url(r'^murrain_list', web_views.CaseListView.as_view(template_name='case/case_murrain_list.html'),
        name='case_murrain_list'),
    url(r'^place_mentioned_list', web_views.CaseListView.as_view(template_name='case/case_place_mentioned_list.html'),
        name='case_place_mentioned_list'),
    url(r'^pledge_list', web_views.CaseListView.as_view(template_name='case/case_pledge_list.html'),
        name='case_pledge_list'),
]

county_urls = [
    url(r'^$', web_views.CountyDetailView.as_view(template_name='county/_county_detail.html'), name='county'),
    url(r'^village_list$', web_views.CountyDetailView.as_view(template_name='county/county_village_list.html'),
        name='county_village_list'),
    url(r'^case_list$', web_views.CaseListView.as_view(template_name='county/county_case_list.html'),
        name='county_case_list'),
    url(r'^resident_list$', web_views.CaseListView.as_view(template_name='county/county_resident_list.html'),
        name='county_resident_list'),
    url(r'^litigant_list$', web_views.CaseListView.as_view(template_name='county/county_litigant_list.html'),
        name='county_litigant_list'),
    url(r'^hundred_list$', web_views.CaseListView.as_view(template_name='county/county_hundred_list.html'),
        name='county_hundred_list'),
]

hundred_urls = [
    url(r'^$', web_views.HundredDetailView.as_view(template_name='hundred/_hundred_detail.html'), name='hundred'),
    url(r'^case_list$', web_views.HundredListView.as_view(template_name='hundred/hundred_case_list.html'),
        name='hundred_case_list'),
    url(r'^resident_list$', web_views.CaseListView.as_view(template_name='hundred/hundred_resident_list.html'),
        name='hundred_resident_list'),
    url(r'^litigant_list$', web_views.CaseListView.as_view(template_name='hundred/hundred_litigant_list.html'),
        name='hundred_litigant_list'),
    url(r'^village_list$', web_views.CaseListView.as_view(template_name='hundred/hundred_village_list.html'),
        name='hundred_village_list'),
]

land_urls = [
    url(r'^$', web_views.LandDetailView.as_view(template_name='land/_land_detail.html'), name='land'),
    url(r'^tenants', web_views.LandDetailView.as_view(template_name='land/tenant_history.html'), name='tenant_history'),
    url(r'^split_history', web_views.LandDetailView.as_view(template_name='land/land_split_history.html'),
        name='land_split_history'),
    url(r'^case_history', web_views.LandDetailView.as_view(template_name='land/land_case_history.html'),
        name='land_case_history'),
]


person_detail_urls = [
    url(r'^$', web_views.PersonDetailView.as_view(template_name='person/_person_detail.html'), name='person'),
    url(r'^case_list', web_views.PeopleListView.as_view(template_name='person/person_case_list.html'),
        name='person_case_list'),
    url(r'^pledge_list', web_views.PeopleListView.as_view(template_name='person/pledge_list.html'), name='pledge_list'),
    url(r'^relationship_list', web_views.PeopleListView.as_view(template_name='person/relationship_list.html'),
        name='relationship_list'),
    url(r'^position_list', web_views.PeopleListView.as_view(template_name='person/position_list.html'), name='position_list'),
    url(r'^land_list', web_views.PeopleListView.as_view(template_name='person/person_land_history_list.html'),
        name='person_land_history'),
    url(r'^stats', web_views.PersonDetailView.as_view(template_name='person/person_stats.html'), name='person_stats'),
    url(r'^amercement_list', web_views.PersonDetailView.as_view(template_name='person/person_amercement_cases.html'),
        name='person_amercement_list'),
    url(r'^fine_list', web_views.PersonDetailView.as_view(template_name='person/person_fine_cases.html'),
        name='person_fine_list'),
    url(r'^damage_list', web_views.PersonDetailView.as_view(template_name='person/person_damage_cases.html'),
        name='person_damage_list'),
    url(r'^chevage_list', web_views.PersonDetailView.as_view(template_name='person/person_chevage_cases.html'),
        name='person_chevage_list'),
    url(r'^impercamentum_list', web_views.PersonDetailView.as_view(
        template_name='person/person_impercamentum_cases.html'), name='person_impercamentum_list'),
    url(r'^heriot_list', web_views.PersonDetailView.as_view(template_name='person/person_heriot_cases.html'),
        name='person_heriot_list'),
]

record_urls = [
    url(r'^$', web_views.RecordDetailView.as_view(template_name='record/_record_detail.html'), name='record'),
    url(r'^session_list$', web_views.RecordDetailView.as_view(template_name='record/record_session_list.html'),
        name='record_session_list'),
]

session_urls = [
    url(r'^$', web_views.SessionDetailView.as_view(template_name='session/_session_detail.html'), name='session'),
    url(r'^case_list$', web_views.CaseListView.as_view(template_name='session/session_case_list.html'),
        name='session_case_list'),
]

village_urls = [
    url(r'^$', web_views.VillageDetailView.as_view(template_name='village/_village_detail.html'), name='village'),
    url(r'^case_list$', web_views.CaseListView.as_view(template_name='village/village_case_list.html'),
        name='village_case_list'),
    url(r'^resident_list$', web_views.PersonDetailView.as_view(template_name='village/village_resident_list.html'),
        name='village_resident_list'),
    url(r'^litigant_list$', web_views.PersonDetailView.as_view(template_name='village/village_litigant_list.html'),
        name='village_litigant_list'),
    url(r'^places_mentioned_list$', web_views.VillageListView.as_view(template_name='village/village_place_mentioned_list.html'),
        name='village_places_mentioned_list'),
    url(r'^related_places$', web_views.VillageListView.as_view(template_name='village/village_related_places_list.html'),
        name='village_related_places_list'),

]


urlpatterns += [
    url(r'^archive/(?P<pk>\d+)/', include(archive_urls)),
    url(r'^case/(?P<pk>\d+)/', include(case_urls)),
    url(r'^county/(?P<pk>\d+)/', include(county_urls)),
    url(r'^hundred/(?P<pk>\d+)/', include(hundred_urls)),
    url(r'^land/(?P<pk>\d+)/', include(land_urls)),
    url(r'^person/(?P<pk>\d+)/', include(person_detail_urls)),
    url(r'^record/(?P<pk>\d+)/', include(record_urls)),
    url(r'^session/(?P<pk>\d+)/', include(session_urls)),
    url(r'^village/(?P<pk>\d+)/', include(village_urls)),
    url(r'^analysis/', include(analysis_urls)),
    url(r'^archives/$', web_views.ArchiveListView.as_view(template_name='archive/_archive_list.html'),
        name='archive_list'),
    url(r'^people/$', web_views.PeopleListView.as_view(template_name='person/_person_list.html'), name='person_list'),
    url(r'^cases/$', web_views.CaseListView.as_view(template_name='case/_case_list.html'), name='case_list'),
    url(r'^counties/$', web_views.CountyListView.as_view(template_name='county/_county_list.html'),
        name='county_list'),
    url(r'^hundreds/$', web_views.HundredListView.as_view(template_name='hundred/_hundred_list.html'),
        name='hundred_list'),

    url(r'^villages/$', web_views.VillageListView.as_view(template_name='village/_village_list.html'),
        name='village_list'),
    url(r'^archives/$', web_views.ArchiveListView.as_view(template_name='archive/_archive_list.html'),
        name='archive_list'),
    url(r'^records/$', web_views.RecordListView.as_view(template_name='record/_record_list.html'), name='record_list'),
    url(r'^sessions/$', web_views.SessionListView.as_view(template_name='session/_session_list.html'),
        name='session_list'),
    url(r'^lands/$', web_views.LandListView.as_view(template_name='land/_land_list.html'), name='land_list'),
]

# JS Reverse to make Django URL routing available in JS - https://github.com/ierror/django-js-reverse

urlpatterns += [
    url(r'^jsreverse/$', urls_js, name='js_reverse'),
]

# Use DRF router to easily direct API traffic.
router = routers.DefaultRouter()
router.register(r'lands', api_views.LandViewSet)
router.register(r'archives', api_views.ArchiveViewSet)
router.register(r'money', api_views.MoneyViewSet)
router.register(r'chattels', api_views.ChattelViewSet)
router.register(r'case_types', api_views.CaseTypeViewSet, base_name='case-type')
router.register(r'counties', api_views.CountyViewSet)
router.register(r'parcel_tenures', api_views.ParcelTenureViewSet, base_name='parcel-tenure')
router.register(r'parcel_types', api_views.ParcelTypeViewSet, base_name='parcel-type')
router.register(r'position_titles', api_views.PositionTypeViewSet, base_name='position-title')
router.register(r'relation_types', api_views.RelationshipViewSet, base_name='relation-type')
router.register(r'role_types', api_views.RoleViewSet, base_name='role-type')
router.register(r'verdicts', api_views.VerdictViewSet)
router.register(r'hundreds', api_views.HundredViewSet)
router.register(r'villages', api_views.VillageViewSet)
router.register(r'people', api_views.PersonViewSet, base_name='person')
router.register(r'records', api_views.RecordViewSet)
router.register(r'sessions', api_views.SessionViewSet)
router.register(r'cornbot', api_views.CornbotViewSet)
router.register(r'extrahura', api_views.ExtrahuraViewSet)
router.register(r'murrains', api_views.MurrainViewSet)
router.register(r'places_mentioned', api_views.PlaceMentionedViewSet, base_name='places-mentioned')
router.register(r'land_parcels', api_views.PlaceMentionedViewSet, base_name='land-parcel')
router.register(r'pledges', api_views.PledgeViewSet)
router.register(r'land_splits', api_views.LandSplitViewSet, base_name='land-split')
router.register(r'relationships', api_views.RelationshipViewSet, base_name='relationship')
router.register(r'cases', api_views.CaseViewSet, base_name='case')
router.register(r'positions', api_views.PositionViewSet, base_name='position')
router.register(r'litigants', api_views.LitigantViewSet, base_name='litigant')

urlpatterns += [
    url(r'^api/', include(router.urls, namespace='api')),
]
