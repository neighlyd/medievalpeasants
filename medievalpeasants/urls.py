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

from rest_framework import routers

# REMEMBER TO RUN .manage.py collectstatic_js_reverse when adding new URLs or django_js_reverse won't pick them up.
from django_js_reverse.views import urls_js

from peasantlegaldb.api import views as api_views
from peasantlegaldb import views as web_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^index', TemplateView.as_view(template_name='index.html'), name='index'),
]

# Map web views to URL Patterns

person_urls = [
    url(r'^$', web_views.PersonDetailView.as_view(template_name='person/person_detail.html'), name='person'),
    url(r'^case_list', web_views.PeopleListView.as_view(template_name='person/person_case_list.html'), name='person_case_list'),
    url(r'^pledge_list', web_views.PeopleListView.as_view(template_name='person/pledge_list.html'), name='pledge_list'),
    url(r'^relationship_list', web_views.PeopleListView.as_view(template_name='person/relationship_list.html'), name='relationship_list'),
    url(r'^position_list', web_views.PeopleListView.as_view(template_name='person/position_list.html'), name='position_list'),
    url(r'^land_list', web_views.PeopleListView.as_view(template_name='person/person_land_history_list.html'), name='person_land_history'),
    url(r'^stats', web_views.PersonDetailView.as_view(template_name='person/person_stats.html'), name='person_stats'),
]

case_urls = [
    url(r'^$', web_views.CaseDetailView.as_view(template_name='case/case_detail.html'), name='case'),
    url(r'^litigants', web_views.LitigantListView.as_view(template_name='case/litigant_list.html'), name='case_litigants'),
    url(r'^land', web_views.CaseListView.as_view(template_name='case/case_land.html'), name='case_land')
]

land_urls = [
    url(r'^$', web_views.LandDetailView.as_view(template_name='land/land_detail.html'), name='land'),
    url(r'^tenants', web_views.LandDetailView.as_view(template_name='land/tenant_history.html'), name='tenant_history'),
    url(r'^split_history', web_views.LandDetailView.as_view(template_name='land/land_split_history.html'), name='land_split_history'),
    url(r'^case_history', web_views.LandDetailView.as_view(template_name='land/land_case_history.html'), name='land_case_history'),
]

urlpatterns += [
    url(r'^person/(?P<pk>\d+)/', include(person_urls)),
    url(r'^case/(?P<pk>\d+)/', include(case_urls)),
    url(r'^land/(?P<pk>\d+)/', include(land_urls)),
    url(r'^people/$', web_views.PeopleListView.as_view(template_name='person/person_list.html'), name='person_list'),
    url(r'^cases/$', web_views.CaseListView.as_view(template_name='case/case_list.html'), name='case_list'),
]

# JS Reverse to make Django URL routing available in JS - https://github.com/ierror/django-js-reverse

urlpatterns += [
    url(r'^jsreverse/$', urls_js, name='js_reverse'),
]

# Use DRF router to easily direct API traffic.
router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

api_urls = [
    url(r'^archives', api_views.ArchiveViewSet.as_view({'get':'list'}), name='archive_api'),
    url(r'^money', api_views.MoneyViewSet.as_view({'get':'list'}), name='money_api'),
    url(r'^chattel', api_views.ChattelViewSet.as_view({'get':'list'}), name='chattel_api'),
    url(r'^case_types', api_views.CaseTypeViewSet.as_view({'get':'list'}), name='case_types_api'),
    url(r'^counties', api_views.CountyViewSet.as_view({'get':'list'}), name='counties_api'),
    url(r'^lands', api_views.LandViewSet.as_view({'get':'list'}), name='land_api'),
    url(r'^parcel_tenures', api_views.ParcelTenureViewSet.as_view({'get':'list'}), name='parcel_tenures_api'),
    url(r'^parcel_types', api_views.ParcelTypeViewSet.as_view({'get':'list'}), name='parcel_types_api'),
    url(r'^position_titles', api_views.PositionTypeViewSet.as_view({'get':'list'}), name='position_titles_api'),
    url(r'^relation_types', api_views.RelationViewSet.as_view({'get':'list'}), name='relation_types_api'),
    url(r'^role_types', api_views.RoleViewSet.as_view({'get':'list'}), name='role_types_api'),
    url(r'^verdicts', api_views.VerdictViewSet.as_view({'get':'list'}), name='verdicts_api'),
    url(r'^hundreds', api_views.HundredViewSet.as_view({'get':'list'}), name='hundreds_api'),
    url(r'^villages', api_views.VillageViewSet.as_view({'get':'list'}), name='villages_api'),
    url(r'^people', api_views.PersonViewSet.as_view({'get':'list'}), name='people_api'),
    url(r'^records', api_views.RecordViewSet.as_view({'get':'list'}), name='records_api'),
    url(r'^sessions', api_views.SessionViewSet.as_view({'get':'list'}), name='sessions_api'),
    url(r'^cornbots', api_views.CornbotViewSet.as_view({'get':'list'}), name='cornbots_api'),
    url(r'^extrahura', api_views.ExtrahuraViewSet.as_view({'get':'list'}), name='extrahura_api'),
    url(r'^murrains', api_views.MurrainViewSet.as_view({'get':'list'}), name='murrains_api'),
    url(r'^places_mentioned', api_views.PlaceMentionedViewSet.as_view({'get':'list'}), name='places_mentioned_api'),
    url(r'^land_parcels', api_views.LandParcelViewSet.as_view({'get':'list'}), name='land_parcels_api'),
    url(r'^pledges', api_views.PledgeViewSet.as_view({'get':'list'}), name='pledges_api'),
    url(r'^land_split', api_views.LandSplitViewSet.as_view({'get':'list'}), name='land_split_api'),
    url(r'^relationships', api_views.RelationshipViewSet.as_view({'get':'list'}), name='relationships_api'),
    url(r'^cases', api_views.CaseViewSet.as_view({'get':'list'}), name='case_list_api'),
    url(r'^positions', api_views.PositionViewSet.as_view({'get':'list'}), name='positions_api'),
    url(r'^litigants', api_views.LitigantViewSet.as_view({'get': 'list'}), name='litigants_api'),
    url(r'^relationships', api_views.RelationshipViewSet.as_view({'get':'list'}), name='relationships_api'),
    url(r'^case_people_land', api_views.CasePeopleLandViewSet.as_view({'get':'list'}), name='case_people_land_api')
]

urlpatterns += [
    url(r'^api/', include(api_urls)),
]
