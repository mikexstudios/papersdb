from dagny.urls import resources

from django.conf.urls.defaults import *
from django.conf import settings #for MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'papers.views.home', name = 'home'), #default url


    (r'^papers/', resources('papers.resources.Paper', name='Paper')),
    (r'^papers/', include('papers.urls')), #includes additional dagny urls


    #Override for simple backend to redirect user to overview page on successful
    #registration.
    url(r'^accounts/register/$', 'registration.views.register',
        {'backend': 'registration.backends.simple.SimpleBackend', 
         'success_url': settings.LOGIN_REDIRECT_URL},
        name='registration_register'),
    #For django-registration. `default` backend means email activation. 
    #`simple` backend means immediate activation and login.
    (r'^accounts/', include('registration.backends.simple.urls')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #URLs for django-rpx-plus:                   
    #url(r'^accounts/$', 'django.views.generic.simple.redirect_to', 
    #                    {'url': '/accounts/profile/', 'permanent': False},
    #                    name='auth_home'),
    #url(r'^accounts/profile/$', 'subscription.views.edit_user_profile', name='edit_profile'),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', 
    #                  {'template_name': 'django_rpx_plus/logged_out.html'}, 
    #                  name='auth_logout'),
    #url(r'^accounts/associate/delete/(\d+)/$', subscription.views.delete_associated_login, name='delete-associated-login'),
    #(r'^accounts/', include('django_rpx_plus.urls')),

    #Temporary fix for serving static files in dev environment.
    #See: http://docs.djangoproject.com/en/dev/howto/static-files/
    #In production setting, the webserver automatically overrides this, 
    #so there is no need to take this out when in production:
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
)
