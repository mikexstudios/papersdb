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

class GenerateThumbnailTest(TestCase):

    def setUp(self):
        #Bypass the celery daemon and directly test synchronously.
        settings.CELERY_ALWAYS_EAGER = True

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

    def test_generate_thumbnail(self):
        '''
        Call the generate thumbnail task on the new paper. The task should return
        True and the thumbnail should be generated.
        '''
        r = generate_paper_thumbnail.delay(self.p)
        self.assertTrue(r.get()) #wait until task is done and get result

        paper_dir = os.path.join(settings.UPLOAD_ROOT, self.p.user.username, self.p.hash)
        thumbnail_file = os.path.join(paper_dir, settings.THUMBNAIL_FILENAME % self.p.hash)
        self.assertTrue(os.path.exists(thumbnail_file))

