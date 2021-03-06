from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth.models import User
from papers.models import Paper

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re

class LoginRequiredTest(TestCase):
    '''
    Tests that specified pages require login. Since we have a universal decorator
    that automatically sets login_required on all paper/* pages, we don't need
    to test all pages, just one of them.
    '''

    def setUp(self):
        #Create test user but don't login.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')

        self.data = {'user': self.user, 'title': 'Test Title', 'url':
                'http://example.com', 'journal': 'Journal of Test', 'year':
                '2011', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', }

        p = Paper(**self.data) #unpack dictionary to arguments
        p.save()

    def tearDown(self):
        pass

    def test_login_required(self):
        r = self.client.get('/papers/', {})
        self.assertRedirects(r, '%s?next=%s' % (reverse('auth_login'), '/papers/'))


class PageExistsTest(TestCase):

    def setUp(self):
        #Create and login test user.
        self.user = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

        #Create a sample paper
        self.data = {'user': self.user, 'title': 'Test Title', 'url':
                'http://example.com', 'journal': 'Journal of Test', 'year':
                '2011', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', }

        self.paper = Paper(**self.data) #unpack dictionary to arguments
        self.paper.save()

    def tearDown(self):
        pass

    def test_static_assets_exists(self):
        r = self.client.get('/static/css/screen.css', {})
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/static/css/print.css', {})
        self.assertEqual(r.status_code, 200)

        r = self.client.get('/static/css/buttons.css', {})
        self.assertEqual(r.status_code, 200)

        #TODO: Make favicon.
        r = self.client.get('/favicon.ico', {})
        self.assertEqual(r.status_code, 404)

    def test_dashboard_exists(self):
        r = self.client.get('/papers/', {})
        self.assertEqual(r.status_code, 200)

    def test_papers_new_manual_exists(self):
        r = self.client.get('/papers/new/manual/', {})
        self.assertEqual(r.status_code, 200)

        #Also make sure that a form is being shown. Just check for a Title field
        #in the form. Assume if 'Title' exists, rest of the form does too.
        self.assertTrue(re.search('Title', str(r.context['self'].form)))

    def test_papers_new_auto_exists(self):
        r = self.client.get('/papers/new/', {})
        self.assertEqual(r.status_code, 200)

        #Also make sure that a form is being shown.
        self.assertTrue(re.search('URL', str(r.context['self'].form)))

    def test_papers_view_exists(self):
        r = self.client.get('/papers/%s/' % self.paper.local_id, {})
        self.assertEqual(r.status_code, 200)

        self.assertEqual(r.context['self'].paper.title, self.paper.title) 

    def test_papers_edit_exists(self):
        r = self.client.get('/papers/%s/edit/' % self.paper.local_id, {})
        self.assertEqual(r.status_code, 200)

        self.assertTrue(re.search('Title', str(r.context['self'].form)))
