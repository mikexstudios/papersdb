from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

#from django.contrib.auth.models import User
from papers.models import Paper

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re
import os

class AddPaperViewTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_valid_form(self):
        '''
        When valid form is submitted, database entry should be created, then
        redirect to dashboard.
        '''
        data = {'title': 'Test Title', 'url': 'http://example.com', 'journal':
        'Journal of Test', 'year': '2011', 'submit': 'Submit', 'volume': '1',
        'authors': "Author One\nAuthor Two\nAuthor Three",
        'issue': '2', 'pages': '3-4', }

        #Also add a file to upload. This is a dummy blank pdf.
        self.TEST_FILES_PATH = os.path.join(settings.SITE_ROOT, 'papers',
                                            'tests', 'files')
        upload_filename = 'blank.pdf'
        upload_file = open(os.path.join(self.TEST_FILES_PATH, upload_filename), 'rb')
        data['file'] = upload_file

        r = self.client.post('/papers/new/', data)
        upload_file.close()
        self.assertRedirects(r, reverse('dashboard'))

        #Also make sure information is saved to database. If not saved, will
        #raise DoesNotExist.
        #NOTE: We don't check all of the fields. We assume that if the Paper
        #      object exists, the information was saved correctly.
        p = Paper.objects.get(title = data['title'], authors = data['authors'])

        #Check that filename was saved to database.
        self.assertEquals(p.file, upload_filename)



class DashboardViewTest(TestCase):

    def setUp(self):
        self.data = {'title': 'Test Title', 'url': 'http://example.com', 'journal':
        'Journal of Test', 'year': '2011', 'volume': '1', 'authors': 
        "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages': '3-4', }

        p = Paper(**self.data) #unpack dictionary to arguments
        p.save()

    def tearDown(self):
        pass

    def test_that_paper_is_listed(self):
        '''
        A paper was added in setUp. Now check if it is shown on the dashboard
        page.
        '''
        r = self.client.get('/dashboard/', {})
        #Assume that if we find the title of the dummy paper that the rest of
        #the information is there too.
        self.assertContains(r, self.data['title'], count = 1)


