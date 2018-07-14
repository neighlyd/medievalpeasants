from django.conf.urls import url, include

from rest_framework import routers

from api import views as api_views

# Use DRF router to easily direct API traffic.
router = routers.DefaultRouter()
router.register(r'archives', api_views.ArchiveViewSet, base_name='archive')
router.register(r'cases', api_views.CaseViewSet, base_name='case')
router.register(r'case_types', api_views.CaseTypeViewSet, base_name='case-type')
router.register(r'chattels', api_views.ChattelViewSet, base_name='chattel')
router.register(r'counties', api_views.CountyViewSet, base_name='county')
router.register(r'cornbot', api_views.CornbotViewSet, base_name='cornbot')
router.register(r'extrahura', api_views.ExtrahuraViewSet, base_name='extrahura')
router.register(r'hundreds', api_views.HundredViewSet, base_name='hundred')
router.register(r'lands', api_views.LandViewSet, base_name='land')
router.register(r'land_parcels', api_views.PlaceMentionedViewSet, base_name='land-parcel')
router.register(r'land_splits', api_views.LandSplitViewSet, base_name='land-split')
router.register(r'litigants', api_views.LitigantViewSet, base_name='litigant')
router.register(r'money', api_views.MoneyViewSet, base_name='money')
router.register(r'murrains', api_views.MurrainViewSet, base_name='murrain')
router.register(r'parcel_tenures', api_views.ParcelTenureViewSet, base_name='parcel-tenure')
router.register(r'parcel_types', api_views.ParcelTypeViewSet, base_name='parcel-type')
router.register(r'people', api_views.PersonViewSet, base_name='person')
router.register(r'places_mentioned', api_views.PlaceMentionedViewSet, base_name='places-mentioned')
router.register(r'pledges', api_views.PledgeViewSet, base_name='pledge')
router.register(r'positions', api_views.PositionViewSet, base_name='position')
router.register(r'position_titles', api_views.PositionTypeViewSet, base_name='position-title')
router.register(r'relationships', api_views.RelationshipViewSet, base_name='relationship')
router.register(r'relation_types', api_views.RelationshipViewSet, base_name='relation-type')
router.register(r'role_types', api_views.RoleViewSet, base_name='role-type')
router.register(r'records', api_views.RecordViewSet, base_name='record')
router.register(r'sessions', api_views.SessionViewSet, base_name='session')
router.register(r'verdicts', api_views.VerdictViewSet, base_name='verdict')
router.register(r'villages', api_views.VillageViewSet, base_name='village')
router.register(r'landtocase', api_views.LandtoCaseViewSet, base_name='landtocase')

urlpatterns = [
    url(r'^', include(router.urls))
]