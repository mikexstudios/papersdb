from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from papers.models import Paper

#from .helpers import 
from papers.tasks import generate_paper_thumbnail

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re
import os
import shutil #for copy2

import mock #for mocking corocodoc API

class PaperModelTest(TestCase):

    def setUp(self):
        #Bypass the celery daemon and directly test synchronously.
        settings.CELERY_ALWAYS_EAGER = True

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

        #Now let's copy the dummy upload file from the test files location path
        #to the uploaded file location
        #NOTE: Even though we may not generate a thumbnail. It is still good to 
        #      place a dummy file so that the thumbnail generation task can run
        #      successfully if called in the right conditions.
        to_path = os.path.join(settings.UPLOAD_ROOT, self.p.user.username, self.p.hash)
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

        #Stop patching process
        self.patcher.stop()

    def test_generate_thumbnail_no_file(self):
        '''
        Call the generate thumbnail task on the new paper with no file associated
        with that paper. We expect nothing to occur and that the task returns 
        False.
        '''
        self.p.file = ''
        self.p.save()

        r = self.p.generate_thumbnail()
        self.assertFalse(r)
        self.assertFalse(self.p.has_thumbnail)
