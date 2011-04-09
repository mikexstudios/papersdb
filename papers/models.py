from django.db import models
from django.contrib.auth.models import User

#from django_extend_model.utils import decorator as extend_model

from .helpers import random_md5
import papers.tasks as tasks


#import datetime

class Paper(models.Model):
    '''
    Describes a paper entry.
    '''
    #id is auto-defined and is auto-incrementing
    #local_id is not autoincrementing, but we fake that in save().
    local_id = models.IntegerField(db_index = True, blank = True, editable = False)
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User)
    hash = models.CharField(db_index = True, max_length = 32) #Random MD5 hash

    title = models.TextField()
    authors = models.TextField()
    journal = models.CharField(blank = True, max_length = 255)
    year = models.PositiveSmallIntegerField(null = True, blank = True)
    #NOTE: Volume and issue may not necessarily be numbers.
    volume = models.CharField(blank = True, max_length = 255)
    issue = models.CharField(blank = True, max_length = 255)
    pages = models.CharField(blank = True, max_length = 255)
    url = models.URLField(default = '', blank = True, 
                          verify_exists = False, max_length = 1000)
    
    #Longest valid filename roughly around 300 characters.
    file = models.CharField(blank = True, max_length = 305) 
    has_thumbnail = models.BooleanField(default = False)

    def __unicode__(self):
        return '%s' % self.id

    def generate_thumbnail(self):
        '''
        Calls thumbnail generation task on uploaded file, if exists.

        @return AsyncResult object from celery.
        '''
        if not file:
            return False

        #This task will automatically set has_thumbnail to True if successful.
        r = tasks.generate_paper_thumbnail(self)
        return r

    def save(self, *args, **kwargs):
        '''
        We want to have the local_id automatically set before save.
        '''
        #Check to see if this object is new. Note that this isn't a foolproof
        #way of checking for a new object since pk can be manually set. See:
        #http://goo.gl/33PwD
        if self.pk is None:
            #Generate a random hash that will be used as a non-guessable ID
            #for this paper.
            self.hash = random_md5()

        #Only set local_id for new objects.
        if self.local_id == None:
            self.local_id = self.user.profile.get_next_paper_id()
        super(Paper, self).save(*args, **kwargs)


class UserProfile(models.Model):
    '''
    Extended fields for User Profile.
    '''
    user = models.OneToOneField(User, primary_key = True)
    #Keeps track of what is the next track number.
    paper_increment = models.PositiveIntegerField(default = 1)

    def get_next_paper_id(self):
        next_id = self.paper_increment
        self.paper_increment += 1
        self.save()
        return next_id
#Auto-create profile if doesn't exist. Also enables the access of UserProfile by
#User.profile.
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


# We handle signals in handlers.py. Make sure they are registered by importing:
import handlers
