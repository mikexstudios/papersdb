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


#For dotcloud only
IS_DOTCLOUD = False #flag that helps us separate dotcloud from local
import json
try:
    with open('/home/dotcloud/environment.json') as f:
      env = json.load(f)
    IS_DOTCLOUD = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'template1', #default dotcloud database
            'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
            'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
            'HOST': env['DOTCLOUD_DB_SQL_HOST'],
            'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
        }
    }
except IOError:
    #We are developing on local environment or non-dotcloud server
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'development.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
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
if IS_DOTCLOUD:
    MEDIA_ROOT = '/home/dotcloud/data/media/'
else:
    MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
if IS_DOTCLOUD:
    STATIC_ROOT = '/home/dotcloud/data/static/'
else:
    STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

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

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Our app must come before registration to override their templates.
    'papers',

    'annoying', #django-annoying
    'south', #migrations
    #'django_rpx_plus', 
    'djcelery', #messaging queue
    'djkombu', #for using orm as ghetto queue
    'registration', #for email activation
    #Must come before admin app to override those templates.
    'registration_defaults', #django-registration default templates

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#The following is not in the default generated settings.py file:

#AUTHENTICATION_BACKENDS = (
#    #'django_rpx_plus.backends.RpxBackend', 
#    'django.contrib.auth.backends.ModelBackend', #default django auth
#)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request', #for request object
    'django.contrib.messages.context_processors.messages',
    #Above are the default template context processors
    'papers.context_processors.sitename',
    #'yourapp.helpers.context_processor',
)

#Additional user data (ie. User Profile)
AUTH_PROFILE_MODULE = 'papers.UserProfile'

# Here are some settings related to auth urls. django has default values for them
# as specified on page: http://docs.djangoproject.com/en/dev/ref/settings/. You
# can override them if you like.
LOGIN_REDIRECT_URL = '/dashboard/' #default: '/accounts/profile/'
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

#Defines the name of the site/webapp. Templates use this variable.
SITENAME = 'PapersDB'

#Allowed file extensions for uploaded papers.
ALLOWED_UPLOAD_EXTENSIONS = ('pdf', )

#Maximum uploaded file size (in bytes)
#NOTE: 1 megabyte = 1048576 bytes
#      1 kilobyte = 1024 bytes
MAXIMUM_UPLOAD_SIZE_MB = 10
MAXIMUM_UPLOAD_SIZE_BYTES = MAXIMUM_UPLOAD_SIZE_MB * 1048576 

#Absolute path to the directory that holds uploads
UPLOAD_ROOT = os.path.join(SITE_ROOT, 'uploads')

#Url to where the uploads can be accessed. No trailing slash.
UPLOAD_URL = MEDIA_URL + 'papers'

#CiteULike parser driver.tcl path (no trailing /):
PARSER_PATH = ''

#ImageMagick command (put in %(document)s and $(thumbnail)s):
IMAGEMAGICK_CMD = "convert -colorspace rgb %(document)s[0] -resize '180' " +\
                  "%(thumbnail)s"
#The format describing the thumbnail filename. Use '%s' to insert the hash.
THUMBNAIL_FILENAME = 'thumb_%s.png'

#Method for uploading documents to Crocodoc service. 'url' method is preferred
#for scalibility and simplicity, but 'post' is good for unit-testing.
CROCODOC_UPLOAD_METHOD = 'post' #url or post

###################
# south settings: #
###################

#We want to disable migrations during tests. Use syncdb instead.
SOUTH_TESTS_MIGRATE = False

######################
# djcelery settings: #
######################

import djcelery
djcelery.setup_loader()

#Result store settings.
CELERY_RESULT_BACKEND = 'database' #default = database
#CELERY_RESULT_DBURI = 'mysql://%s:%s@%s/%s' % ()
CELERY_RESULT_DBURI = 'sqlite://celerydb.sqlite'

BROKER_BACKEND = 'djkombu.transport.DatabaseTransport'
#BROKER_HOST = 'localhost'
#BROKER_PORT = 5672
#BROKER_USER = 'dev'
#BROKER_PASSWORD = 'testtest'
#BROKER_VHOST = 'mXs-MBP'

#If True, tasks are executed locally and never sent to queue.
#CELERY_ALWAYS_EAGER = True
#CELERYD_LOG_LEVEL = 'INFO'

#CELERYD_CONCURRENCY = '2' #default = number of CPU

#List of modules to import when celery starts.
CELERY_IMPORTS = ('papers.tasks', )

################################
#django-registration settings: #
################################

#Needed if using default backend that requires activation.
#ACCOUNT_ACTIVATION_DAYS = 30 

#If False, new registration of accounts are closed. (default = True)
#REGISTRATION_OPEN = False

######################
# crocodoc settings: #
######################

CROCODOC_API_KEY = ''


#Import any local settings (ie. production environment) that will override
#these development environment settings.
try:
    from local_settings import *
except ImportError:
    pass 
