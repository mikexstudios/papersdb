from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('papers.views',
    url(r'^$', 'home', name='home'), #default url
    #url(r'^dashboard/$', 'dashboard', name='dashboard'),
)

#urlpatterns += patterns('',
#    url(r'^example/$', 'django.views.generic.simple.redirect_to', 
#                        {'url': '/', 'permanent': False}),
#)
