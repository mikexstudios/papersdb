from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

#from django.contrib.auth.models import User
from .papers.models import Paper

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re

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

        r = self.client.post('/papers/new/', data)
        self.assertRedirects(r, reverse('dashboard'))

        #Also make sure information is saved to database. If not saved, will
        #raise DoesNotExist.
        Paper.objects.get(title = data['title'], authors = data['authors'])

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


