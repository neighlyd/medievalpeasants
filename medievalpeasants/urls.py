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

from peasantlegaldb.api import views as api_views
from peasantlegaldb import views as web_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^index', TemplateView.as_view(template_name='index.html'), name='index'),
]

# Map web views to URL Patterns
urlpatterns += [
    url(r'^people/$', web_views.PeopleListView.as_view(template_name='person_list.html'), name='person_list'),
    url(r'^person/(?P<pk>\d+)/$', web_views.PersonView.as_view(template_name='person_detail.html'), name='person'),
    url(r'^case/(?P<pk>\d+)/$', web_views.CaseView.as_view(template_name='case_detail.html'), name='case'),
    url(r'^cases/$', web_views.CaseListView.as_view(template_name='case_list.html'), name='case_list'),
    url(r'^litigants/(?P<case>\d+)/$', web_views.LitigantListView.as_view(template_name='litigant_list.html'), name='litigant_list')
]

# Use DRF router to easily direct API traffic.
router = routers.DefaultRouter()
router.register(r'archives', api_views.ArchiveViewSet)
router.register(r'money', api_views.MoneyViewSet)
router.register(r'chattel', api_views.ChattelViewSet)
router.register(r'case_types', api_views.CaseTypeViewSet)
router.register(r'counties', api_views.CountyViewSet)
router.register(r'lands', api_views.LandViewSet)
router.register(r'parcel_tenures', api_views.ParcelTenureViewSet)
router.register(r'parcel_types', api_views.ParcelTypeViewSet)
router.register(r'position_titles', api_views.PositionTypeViewSet)
router.register(r'relation_types', api_views.RelationViewSet)
router.register(r'role_types', api_views.RoleViewSet)
router.register(r'verdicts', api_views.VerdictViewSet)
router.register(r'hundreds', api_views.HundredViewSet)
router.register(r'villages', api_views.VillageViewSet)
router.register(r'people', api_views.PersonViewSet)
router.register(r'records', api_views.RecordViewSet)
router.register(r'sessions', api_views.SessionViewSet)
router.register(r'cases', api_views.CaseViewSet)
router.register(r'cornbots', api_views.CornbotViewSet)
router.register(r'extrahuras', api_views.ExtrahuraViewSet)
router.register(r'murrains', api_views.MurrainViewSet)
router.register(r'places_mentioned', api_views.PlaceMentionedViewSet)
router.register(r'land_parcels', api_views.LandParcelViewSet)
router.register(r'people_to_land', api_views.CasePeopleLandViewSet)
router.register(r'pledges', api_views.PledgeViewSet)
router.register(r'land_split', api_views.LandSplitViewSet)
router.register(r'positions', api_views.PositionViewSet)
router.register(r'relationships', api_views.RelationshipViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api/archivelist', api_views.ArchiveListEndpoint.as_view(), name='archive-list'),
    url(r'^api/litigants', api_views.LitigantViewSet.as_view(), name='litigant_api_list'),
    url(r'^api/litigants/(?P<case>\d+/$)', api_views.LitigantViewSet.as_view(), name='litigants_by_case_list')
]
