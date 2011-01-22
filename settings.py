# Django settings for project.
import os
import django
import sys

# Path of Django framework files (no trailing /):
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
# Path of this "site" (no trailing /):
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mmjsh(tm2ky2+bt^-m-+vn-03*o*)fczt2=0zw6mbb#@0_o@wv'

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
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',

    'annoying', #django-annoying
    'south', #migrations
    #'django_rpx_plus', 
    #'celery', #messaging queue
    'registration', #for email activation
    #Must come before admin app to override those templates.
    'registration_defaults', #django-registration default templates

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

)

#The following is not in the default generated settings.py file:

#AUTHENTICATION_BACKENDS = (
#    #'django_rpx_plus.backends.RpxBackend', 
#    'django.contrib.auth.backends.ModelBackend', #default django auth
#)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request', #for request object
    'django.contrib.messages.context_processors.messages',
    #Above are the default template context processors
    #'yourapp.helpers.context_processor',
)

#Additional user data (ie. User Profile)
#AUTH_PROFILE_MODULE = 'yourapp.UserProfile'

# Here are some settings related to auth urls. django has default values for them
# as specified on page: http://docs.djangoproject.com/en/dev/ref/settings/. You
# can override them if you like.
#LOGIN_REDIRECT_URL = '' #default: '/accounts/profile/'
#LOGIN_URL = '' #default: '/accounts/login/'
#LOGOUT_URL = '' #default: '/accounts/logout/'

#SMTP is the default backend so no need to specify
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_PORT = 587 #TLS
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'appname <do-not-reply@appname.com>'
#Defines email addresses that error/admin messages come from
SERVER_EMAIL = 'appname admin <root@appname.com>'

#Keep from getting 404 messages about favicon.ico
SEND_BROKEN_LINK_EMAILS = False

####################
# papers settings: #
####################


###################
# south settings: #
###################

#We want to disable migrations during tests. Use syncdb instead.
SOUTH_TESTS_MIGRATE = False

####################
# celery settings: #
####################

#CELERY_BACKEND = 'database' #default = database

#BROKER_HOST = 'localhost'
#BROKER_PORT = 5672
#BROKER_USER = 'dev'
#BROKER_PASSWORD = 'testtest'
#BROKER_VHOST = 'mXs-MBP'

#If True, tasks are executed locally and never sent to queue.
#CELERY_ALWAYS_EAGER = True
#CELERYD_LOG_LEVEL = 'INFO'

################################
#django-registration settings: #
################################

#Needed if using default backend that requires activation.
#ACCOUNT_ACTIVATION_DAYS = 30 

#If False, new registration of accounts are closed. (default = True)
#REGISTRATION_OPEN = False


#Import any local settings (ie. production environment) that will override
#these development environment settings.
try:
    from local_settings import *
except ImportError:
    pass 
