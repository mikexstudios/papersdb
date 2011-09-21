import os, sys

#Adding papersdb directory to path because all of the project paths are 
#relative to this directory.
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                                'papersdb'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
