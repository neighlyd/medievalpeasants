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
from rest_framework import routers
from peasantlegaldb import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'archives', views.ArchiveViewSet)
router.register(r'money', views.MoneyViewSet)
router.register(r'chattel', views.ChattelViewSet)
router.register(r'case_types', views.CaseTypeViewSet)
router.register(r'counties', views.CountyViewSet)
router.register(r'lands', views.LandViewSet)
router.register(r'parcel_tenures', views.ParcelTenureViewSet)
router.register(r'parcel_types', views.ParcelTypeViewSet)
router.register(r'position_titles', views.PositionTypeViewSet)
router.register(r'relation_types', views.RelationViewSet)
router.register(r'role_types', views.RoleViewSet)
router.register(r'verdicts', views.VerdictViewSet)
router.register(r'hundreds', views.HundredViewSet)
router.register(r'villages', views.VillageViewSet)
router.register(r'people', views.PersonViewSet)
router.register(r'records', views.RecordViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'cases', views.CaseViewSet)
router.register(r'chevages', views.ChevageViewSet)
router.register(r'cornbots', views.CornbotViewSet)
router.register(r'extrahuras', views.ExtrahuraViewSet)
router.register(r'heriots', views.HeriotViewSet)
router.register(r'impercamenta', views.ImpercamentumViewSet)
router.register(r'murrains', views.MurrainViewSet)
router.register(r'places_mentioned', views.PlaceMentionedViewSet)
router.register(r'land_parcels', views.LandParcelViewSet)
router.register(r'litigants', views.LitigantViewSet)
router.register(r'people_to_land', views.CasePeopleLandViewSet)
router.register(r'pledges', views.PledgeViewSet)
router.register(r'land_split', views.LandSplitViewSet)
router.register(r'positions', views.PositionViewSet)
router.register(r'relationships', views.RelationshipViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/', include(router.urls)),
]
