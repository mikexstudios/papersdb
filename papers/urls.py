from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('papers.views',
    url(r'^$', 'home', name='home'), #default url
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    #We want to match urls that end like: /+authors/ or /-date/
    url(r'^dashboard/sortby/((?:\+|-)\w+)/$', 'dashboard', name='dashboard'),

    #url(r'^papers/(\d+)/$', 'papers_view', name='papers_view'),
    #url(r'^papers/new/$', 'new_paper_auto', name='new_paper'),
    #TODO: The [-\w] is a UUID. Should be more specific.
    #url(r'^papers/new/status/([-\w]+)/$', 'new_paper_status', name='new_paper_status'),
    #url(r'^papers/new/manual/$', 'new_paper_manual', name='new_paper_manual'),
    #url(r'^papers/new/manual/([-\w]+)/$', 'new_paper_manual', name='new_paper_manual'),
    #url(r'^papers/import/url/$', 'papers_import_url', name='import_url'),
    url(r'^papers/import/url/([-\w]+)/$', 'papers_import_url_poll', name='import_url_poll'),

    url(r'^papers/(\d+)/edit/$', 'papers_edit', name='papers_edit'),
)

#urlpatterns += patterns('',
#    url(r'^papers/$', 'django.views.generic.simple.redirect_to', 
#                        {'url': '/dashboard/', 'permanent': False}),
#)
