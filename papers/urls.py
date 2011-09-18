from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

#urlpatterns = patterns('papers.views',
#    url(r'^$', 'home', name='home'), #default url
#)

#Additional dagny urls:
urlpatterns = patterns('papers.resources',

    url(r'^create/status/([-\w]+)/$', 'Paper', 
        kwargs = {'action': 'create_status'},
        name='Paper#create_status'),

    url(r'^new/manual/$', 'Paper', 
        kwargs = {'methods': {'GET': 'new_manual'}},
        name='Paper#new_manual'),
    url(r'^new/manual/([-\w]+)/$', 'Paper', 
        kwargs = {'methods': {'GET': 'new_manual'}},
        name='Paper#new_manual'),
    url(r'^create/manual/$', 'Paper', 
        kwargs = {'methods': {'POST': 'create_manual'}},
        name='Paper#create_manual'),

    url(r'^import/url/([-\w]+)/$', 'Paper', 
        kwargs = {'methods': {'GET': 'import_url_poll'}},
        name='Paper#import_url_poll'),

    #Additional actions on paper
    url(r'^(\d+)/quickview/$', 'Paper', 
        kwargs = {'methods': {'GET': 'quickview'}},
        name='Paper#quickview'),
    url(r'^(\d+)/download/$', 'Paper', 
        kwargs = {'methods': {'GET': 'download'}},
        name='Paper#download'),

)
