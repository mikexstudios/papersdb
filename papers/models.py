from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

#from django_extend_model.utils import decorator as extend_model

from annoying.fields import AutoOneToOneField
import crocodoc

import os #for path

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
    #If asap is set to True, then in the future, we should go back and update
    #this paper with the correct information.
    is_asap = models.BooleanField(default = False)
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

    def get_file_url(self, is_absolute = False):
        '''
        Returns the static url (starting with /) to the associated file, if
        exists. Otherwise, returns False. If is_absolute = True, the returns
        the full absolute path to the file (starting with http://).
        '''
        if not self.file:
            return False
        url = '%s/%s/%s/%s' % (settings.UPLOAD_URL, self.user.username,
                               self.hash, self.file)
        if is_absolute:
            url = 'http://%s%s' % (request.get_host(), url)
        return url

    def get_file_dir(self):
        '''
        Returns the full path to the directory of the uploaded file, if exists.
        '''
        if not self.file:
            return False
        return os.path.join(settings.UPLOAD_ROOT, self.user.username, 
                            self.hash)

    def get_file_path(self):
        '''
        Returns the full path of the uploaded file, if exists.
        '''
        if not self.file:
            return False
        return os.path.join(self.get_file_dir(), self.file)

    def generate_thumbnail(self):
        '''
        Calls thumbnail generation task on uploaded file, if exists.

        @return AsyncResult object from celery.
        '''
        if not self.file:
            return False

        #This task will automatically set has_thumbnail to True if successful.
        r = tasks.generate_paper_thumbnail.delay(self)
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

        #Refresh object
        self = Paper.objects.get(pk = self.pk)

        #If we don't already have a generated thumbnail, call paper thumbnail
        #generation task. Returns the AsyncResult object, which was don't use
        #here.
        #NOTE: We take care of the case where many calls to generate thumbnail
        #are created before has_thumbnail has been set by having the task 
        #perform an additional check to see if the paper has_thumbnail = True
        #in the time it took to get to the task in the queue.
        if not self.has_thumbnail and self.file:
            self.generate_thumbnail()

        #If the paper has not been uploaded to Crocodoc, do it. We need this
        #part after the real save so that the uploaded file can be saved 
        #first.
        if not self.crocodoc.uuid:
            self.crocodoc.upload()



class Crocodoc(models.Model):
    paper = AutoOneToOneField(Paper, primary_key = True)
    uuid = models.CharField(max_length = 36, blank = True)
    short_id = models.CharField(max_length = 7, blank = True) #ex. yQZpPm
    #The session_id allows viewing of privately uploaded Crocodoc documents.
    #They do not expire, but may only be accessed once. Thus, to not block
    #the request, we pre-populate the session_id for each document and then
    #grab and new one once the current one has been used.
    session_id = models.CharField(max_length = 15, blank = True)
    #is_viewable = models.BooleanField(default = False)

    def delete(self, *args, **kwargs):
        '''
        Deletes the Crocodoc upload before deleting self.

        NOTE: Will not be called when deleting objects in bulk.
        '''
        if self.uuid:
            tasks.crocodoc_delete_uuid.delay(self.uuid)

        super(Crocodoc, self).delete(*args, **kwargs)

    def upload(self, method = None):
        '''
        Uploads the paper (via URL or POST method) to Crocodoc by calling task.

        @return AsyncResult object from task/celery.
        '''
        r = tasks.crocodoc_upload_paper.delay(self.paper, 
                method = settings.CROCODOC_UPLOAD_METHOD)
        return r

    def refresh_session_id(self):
        '''
        Gets a new session_id by calling task.

        @return AsyncResult from task.
        '''
        r = tasks.crocodoc_get_session_id.delay(self.paper)
        return r

    def url(self):
        '''
        Returns a session-based url to the private document. Generates a new
        session_id at the same time (for subsequent use).
        '''
        url = crocodoc.Crocodoc.session_based_viewer_url(self.session_id)
        self.refresh_session_id()
        return url

    def embeddable_url(self):
        return crocodoc.Crocodoc.embeddable_viewer_url(self.short_id)


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
