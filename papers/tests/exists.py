from django.conf import settings
from django.test import TestCase
#from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
#from .models import 

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re

class LoginRequiredTest(TestCase):
    '''
    Tests that specified pages require login.
    '''

    def setUp(self):
        self.pages = (
                '/dashboard/',
                '/papers/new/',
        )

    def tearDown(self):
        pass

    def test_login_required(self):
        for p in self.pages:
            r = self.client.get(p, {})
            self.assertRedirects(r, '%s?next=%s' % (reverse('auth_login'), p))


class PageExistsTest(TestCase):

    def setUp(self):
        #Create and login test user.
        u = User.objects.create_user('test', 'test@example.com', 'test')
        self.client.login(username = 'test', password = 'test')

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
        r = self.client.get('/dashboard/', {})
        self.assertEqual(r.status_code, 200)

    def test_papers_new_exists(self):
        r = self.client.get('/papers/new/', {})
        self.assertEqual(r.status_code, 200)

        #Also make sure that a form is being shown. Just check for a Title field
        #in the form. Assume if 'Title' exists, rest of the form does too.
        self.assertTrue(re.search('Title', str(r.context['form'])))
