from django.conf.urls.defaults import *
#from django.conf import settings

#from .models import 

urlpatterns = patterns('papers.views',
    url(r'^$', 'home', name='home'), #default url
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^papers/new/$', 'new_paper', name='new_paper'),
)

urlpatterns += patterns('',
    url(r'^papers/$', 'django.views.generic.simple.redirect_to', 
                        {'url': '/dashboard/', 'permanent': False}),
)
