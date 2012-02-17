# ****************************** #
#        CVAM HOURS LOGGER       #
#         Django settings        #
# ****************************** #

# ********
# SOME MAGIC
# We collect project paths to keep the app automatically relative
import sys, os
from string import replace

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = replace(PROJECT_PATH, '\\','/')
sys.path.append(PROJECT_PATH + '/')



# ********
# SETTINGS that apply to all servers
# or default settings that are overriden in settings_local

PROJECT_URL = ''
SERVER_PROD = False
PREPEND_WWW = False
MEDIA_URL = '/media/'

# ********
# SETTINGS that apply to a specific server for
# database, filesystem and URLs
# are included from settings_local.py
from settings_local import *



# *******
# GENERIC settings, not likely to be changed
# *******

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Site ID, as found on the django_site table.
SITE_ID = 1

# PATHS we can figure out without asking    
MEDIA_ROOT = replace(PROJECT_PATH, '/hours/hours','/hours/media')
ADMIN_MEDIA_PREFIX = '%s/admin/' % MEDIA_URL

# SETTINGS for debugging
if not SERVER_PROD:
	DEBUG = True
	TEMPLATE_DEBUG = DEBUG
else:
	DEBUG = False


MANAGERS = ADMINS


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	'%s/templates' % PROJECT_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'log'
)


