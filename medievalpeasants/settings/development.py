# Import all settings from _base.py and build upon them.
from ._base import *

# Debug for testing
DEBUG = True

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

# SITE_ID is used by django frameworks. To equal the ID of the site in the admin database under Sites/sites
# This value must equal the site's ID in Django's database.
# The documentation on this setting is absolute shit. See http://goo.gl/mqtNGn
SITE_ID = 2
