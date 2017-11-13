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

from django_js_reverse.views import urls_js

from accounts import urls as account_urls
from api import urls as api_urls
from peasantlegaldb import urls as peasantlegal_urls

# Route the admin site.
urlpatterns = [
    url(r'^westminster/', admin.site.urls),
    # registration is currently disabled. Uncomment later to enable registration.
    # url(r'^register/', accounts_views.register, name='register'),

]

# Account urls (e.g. registration, pw reset, login, etc.) are in accounts/urls.py. They are then imported to the main
# urls.py and routed with this statement.

urlpatterns += [
    url(r'^accounts/', include(account_urls)),
]

# Peasant Legal urls are defined within peasantlegaldb/urls.py. They are then imported to the main urls.py and routed
# with this statement.
urlpatterns += [
    url(r'^', include(peasantlegal_urls)),
]


# JS Reverse to make Django URL routing available in JS - https://github.com/ierror/django-js-reverse
urlpatterns += [
    url(r'^jsreverse/$', urls_js, name='js_reverse'),
]


# API urls are defined within api/urls.py. They are then imported to the main urls.py and routed with this statement.
urlpatterns += [
    url(r'^api/', include(api_urls, namespace='api')),
]
