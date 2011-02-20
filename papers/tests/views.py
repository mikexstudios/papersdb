from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from papers.models import Paper

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re
import os

class AddPaperViewTest(TestCase):

    def setUp(self):
        #Create and login test user.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

    def tearDown(self):
        #TODO: Remove the sample uploaded file.
        pass

    def test_valid_form_manual(self):
        '''
        When valid form is submitted, database entry should be created, then
        redirect to dashboard.
        NOTE: For manual adding.
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

        r = self.client.post('/papers/new/manual/', data)
        upload_file.close()
        self.assertRedirects(r, reverse('dashboard'))

        #Also make sure information is saved to database. If not saved, will
        #raise DoesNotExist.
        #NOTE: We don't check all of the fields. We assume that if the Paper
        #      object exists, the information was saved correctly.
        p = Paper.objects.get(title = data['title'], authors = data['authors'])

        #Make sure that the added paper is associated with logged in user.
        self.assertEqual(p.user, self.user)

        #Check that a hash was generated for the paper
        self.assertEqual(len(p.hash), 32)

        #Check that filename was saved to database.
        self.assertEquals(p.file, upload_filename)

        #Check that the file was saved to disk with format:
        #/<upload files location>/username/<hash>/filename.ext
        path = os.path.join(settings.UPLOAD_ROOT, p.user.username, p.hash, p.file)
        self.assertTrue(os.path.exists(path))


class DashboardViewTest(TestCase):

    def setUp(self):
        #Create and login test user.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

        self.data = {'user': self.user, 'title': 'Test Title', 'url':
                'http://example.com', 'journal': 'Journal of Test', 'year':
                '2011', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', }

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

    def test_display_only_user_own_papers(self):
        '''
        Make sure that the list of papers only displays the ones that the logged
        in user has added (and not someone else's papers).
        '''
        #Add another paper under a different user (than the currently logged in 
        #one).
        data = self.data.copy()
        second_user = User.objects.create_user('test2', 'test2@example.com', 'test2')
        data['user'] = second_user
        data['title'] = 'Second Unique Title'
        p = Paper(**data) #unpack dictionary to arguments
        p.save()

        #Make sure that the added paper does not show up in dashboard.
        r = self.client.get('/dashboard/', {})
        self.assertNotContains(r, data['title'])


class AccountsRegisterTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_upload_dir_created(self):
        '''
        When user signs up, an upload directory for that user should be created.
        
        ex. /<uploads path>/username/
        '''
        #Create new test user.
        new_user = User.objects.create_user('test', 'test@example.com', 'test')

        path = os.path.join(settings.UPLOAD_ROOT, new_user.username)
        self.assertTrue(os.path.exists(path))
