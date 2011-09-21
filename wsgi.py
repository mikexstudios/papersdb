import os, sys

#Adding current directory to path because wsgi expects our project to be in a 
#sub-directory.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
