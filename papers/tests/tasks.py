from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from papers.models import Paper

#from .helpers import 
from papers import tasks

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re
import os
import shutil #for copy2
import random, string #for mocking string ids

import mock #for mocking corocodoc API

class GenerateThumbnailTest(TestCase):

    def setUp(self):
        #Bypass the celery daemon and directly test synchronously.
        settings.CELERY_ALWAYS_EAGER = True

        #Set Crocodoc upload method to POST
        settings.CROCODOC_UPLOAD_METHOD = 'post'

        #Create and login test user.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

        #Create a new paper entry with associated file.
        upload_filename = 'blank.pdf'
        self.data = {'user': self.user, 'title': 'Test Title', 'url':
                'http://example.com', 'journal': 'Journal of Test', 'year':
                '2011', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', 'file': upload_filename }

        self.p = Paper(**self.data) #unpack dictionary to arguments
        self.p.save()

        #Now let's copy the dummy upload file from the test files location path
        #to the uploaded file location
        to_path = self.p.get_file_dir()
        from_path = os.path.join(settings.SITE_ROOT, 'papers', 'tests',
                                 'files')
        os.makedirs(to_path, mode = 0755)
        shutil.copy2(os.path.join(from_path, upload_filename), to_path)
        self.uploaded_file = os.path.join(to_path, upload_filename)

    def tearDown(self):
        #Remove the user's upload directory recursively. This also gets rid of 
        #any test uploads.
        path = os.path.join(settings.UPLOAD_ROOT, self.user.username)
        shutil.rmtree(path)

    def test_generate_thumbnail(self):
        '''
        Call the generate thumbnail task on the new paper. The task should return
        True and the thumbnail should be generated.
        '''
        r = tasks.generate_paper_thumbnail.delay(self.p)
        self.assertTrue(r.get()) #wait until task is done and get result

        #Refresh paper object
        self.p = Paper.objects.get(pk = self.p.pk)
        self.assertTrue(self.p.has_thumbnail)

        paper_dir = self.p.get_file_dir()
        thumbnail_file = os.path.join(paper_dir, settings.THUMBNAIL_FILENAME % self.p.hash)
        self.assertTrue(os.path.exists(thumbnail_file))


class CrocodocTests(TestCase):
    '''
    NOTE: At the same time, we end up testing some of the Crocodoc model methods.
    It may be a good idea to just test the task here without going through the
    Crocodoc model, but there is just so much overlap.
    '''

    def setUp(self):
        #Bypass the celery daemon and directly test synchronously.
        settings.CELERY_ALWAYS_EAGER = True

        #Set Crocodoc upload method to POST
        settings.CROCODOC_UPLOAD_METHOD = 'post'
        
        #We want to mock the crocodoc API library so that our tests don't have
        #to actually issue HTTP requests.
        self.patcher = mock.patch('crocodoc.Crocodoc')
        Mock = self.patcher.start()
        self.crocodoc_instance = Mock.return_value
        self.crocodoc_instance.upload.return_value = {'shortId': 'yQZpPm', 
                'uuid': '8e5b0721-26c4-11df-b354-002170de47d3'}
        self.crocodoc_instance.get_session.return_value = {'sessionId': 
                'fgH9qWEwnsJUeB0'}
        self.crocodoc_instance.delete.return_value = True

        #Create and login test user.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

        #Create a new paper entry with associated file.
        upload_filename = 'blank.pdf'
        self.data = {'user': self.user, 'title': 'Test Title', 'url':
                'http://example.com', 'journal': 'Journal of Test', 'year':
                '2011', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', 'file': upload_filename }

        self.p = Paper(**self.data) #unpack dictionary to arguments
        self.p.save()
        #uploading to crocodoc will fail here since the file does not exist (we
        #add it below).

        #Now let's copy the dummy upload file from the test files location path
        #to the uploaded file location
        to_path = self.p.get_file_dir()
        from_path = os.path.join(settings.SITE_ROOT, 'papers', 'tests',
                                 'files')
        os.makedirs(to_path, mode = 0755)
        shutil.copy2(os.path.join(from_path, upload_filename), to_path)
        self.uploaded_file = os.path.join(to_path, upload_filename)

        #We should re-save the Paper here to automatically generate thumbnail
        #and upload to crocodoc. But we don't since we are testing the
        #uploading to crocodoc.

    def tearDown(self):
        #Delete the crocodoc uploaded paper
        try:
            self.p.crocodoc.delete()
        except AssertionError:
            #If we try to delete an already deleted object (like when we test
            #delete), we need to catch this error so that the test doesn't 
            #fail.
            pass

        #Remove the user's upload directory recursively. This also gets rid of 
        #any test uploads.
        path = os.path.join(settings.UPLOAD_ROOT, self.user.username)
        shutil.rmtree(path)

        #Stop patching process
        self.patcher.stop()

    def test_crocodoc_upload_paper_post(self):
        '''
        Call the upload task on the new paper. The task should return
        True and short_id and uuid of the paper should be set.

        NOTE: We are using the POST method of uploading papers because there
        is not an easy way of testing the url method of uploading.

        NOTE: This test may not be very necessary since the act of saving 
        the file above automatically uploads the paper to crocodoc.
        '''
        r = self.p.crocodoc.upload()
        self.assertTrue(r.get()) #wait until task is done and get result

        #Need to refresh our object because of the upload.
        self.p = Paper.objects.get(pk = self.p.pk)

        self.assertTrue(len(self.p.crocodoc.short_id) > 4)
        self.assertTrue(len(self.p.crocodoc.uuid) == 36)
        #And that we also have a session_id
        self.assertTrue(len(self.p.crocodoc.session_id) == 15)

    def test_crocodoc_get_session_id(self):
        '''
        Call the get_session_id task on the new paper. The task should return
        True and the session_id should be different.
        '''
        self.test_crocodoc_upload_paper_post()
        old_session_id = self.p.crocodoc.session_id

        self.crocodoc_instance.get_session.return_value = {'sessionId': 
                'fgH9qWEwnsJUeB1'} #set a different session ID
        r = self.p.crocodoc.refresh_session_id()
        self.assertTrue(r.get())

        #We have to refresh the paper object to get the new session_id
        self.p = Paper.objects.get(pk = self.p.pk)

        self.assertTrue(len(self.p.crocodoc.session_id) == 15)
        self.assertTrue(old_session_id != self.p.crocodoc.session_id)

    def test_crocodoc_delete(self):
        '''
        Call crocodoc_delete_uuid on the uploaded paper. short_id and
        uuid should be empty.
        '''
        self.test_crocodoc_upload_paper_post()
        self.p.crocodoc.delete()

        #When we delete the crocodoc object, the attributes still remain attached
        #to the paper.crocodoc object unless we refresh it.
        self.p = Paper.objects.get(pk = self.p.pk)

        self.assertTrue(len(self.p.crocodoc.short_id) == 0)
        self.assertTrue(len(self.p.crocodoc.uuid) == 0)
