from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('papers.views',
    url(r'^$', 'home', name='home'), #default url
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^papers/new/$', 'new_paper', name='new_paper'),
    url(r'^papers/import/url/$', 'papers_import_url', name='import_url'),
    #TODO: The [-\w] is a UUID. Should be more specific.
    url(r'^papers/import/url/([-\w]+)/$', 'papers_import_url_poll', name='import_url_poll'),
)

urlpatterns += patterns('',
    url(r'^papers/$', 'django.views.generic.simple.redirect_to', 
                        {'url': '/dashboard/', 'permanent': False}),
)
