from django.db import models
#from django.contrib.auth.models import User

#from django_extend_model.utils import decorator as extend_model

#import datetime

class Paper(models.Model):
    '''
    Describes a paper entry.
    '''
    #id is auto-defined and is auto-incrementing
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

    def __unicode__(self):
        return '%s' % self.id
