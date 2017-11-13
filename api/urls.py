from django.conf.urls import url, include

from rest_framework import routers

from api import views as api_views

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

urlpatterns = [
    url(r'^', include(router.urls))
]