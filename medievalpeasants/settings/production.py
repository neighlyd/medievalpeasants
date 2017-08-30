# Import all settings from _base.py and build upon them.
from ._base import *

# Turn off Debug for production
DEBUG = False

# Set allowed hosts to url.
#ALLOWED_HOSTS = ['<PUTHOSTSHERE>']

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 3
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Prevents a frame from serving content from another frame. Suggested to set as false for production, but may change with content generation. We will see.
X_FRAME_OPTIONS = 'DENY'

# Location of static files. This path must be an absolute path.
#STATIC_ROOT = "~/<WHATEVERTHEURLWILLBE>/public/static"
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


# SITE_ID is used by django frameworks. To equal the ID of the site in the admin database under Sites/sites
# This value must equal the site's ID in Django's database.
# The documentation on this setting is absolute shit. See http://goo.gl/mqtNGn
SITE_ID = 3
