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
        kwargs = {'action': 'new_manual'},
        name='Paper#new_manual'),
    url(r'^new/manual/([-\w]+)/$', 'Paper', 
        kwargs = {'action': 'new_manual'},
        name='Paper#new_manual'),
    url(r'^create/manual/$', 'Paper', 
        kwargs = {'action': 'create_manual'},
        name='Paper#create_manual'),

    url(r'^import/url/([-\w]+)/$', 'Paper', 
        kwargs = {'action': 'import_url_poll'},
        name='Paper#import_url_poll'),

    #Additional actions on paper
    url(r'^(\d+)/quickview/$', 'Paper', 
        kwargs = {'action': 'quickview'},
        name='Paper#quickview'),

    #url(r'^(\d+)/download/$', 'Paper', 
    #    kwargs = {'action': 'download'},
    #    name='Paper#download'),

)
