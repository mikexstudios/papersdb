from django.conf import settings
#import django.contrib.messages as messages
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#from .models import 

#import registration.signals as registration_signals

#import datetime
import os

#For django-register

#def handle_user_registered(sender, user, request, **kwargs):
#    #TODO: Use queue to send confirmation email.
#
#
#    messages.success(request, 'Thanks for registering! Hope you will enjoy using subscripter!')
#registration_signals.user_registered.connect(handle_user_registered)


def create_user_upload_dir(sender, instance, created, **kwargs):
    '''
    Creates an upload directory with the user's username if this is the first
    time the user is created.
    '''
    user = instance
    user_upload_path = os.path.join(settings.UPLOAD_ROOT, user.username)

    if created and not os.path.exists(user_upload_path):
        os.mkdir(user_upload_path, 0755)
post_save.connect(create_user_upload_dir, sender = User)

