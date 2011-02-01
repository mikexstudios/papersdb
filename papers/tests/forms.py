from django.conf import settings
from django.test import TestCase
#from django.test.client import Client

#from django.contrib.auth.models import User
#from .models import 

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re

from .papers.forms import NewPaperForm
class AddPaperFormTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_form_errors(self):
        data = {'title': '', 'url': '', 'journal': '', 'year': '', 'submit':
                'Submit', 'volume': '', 'authors': '', 'issue': '', 'pages':
                '', }
        f = NewPaperForm(data)

        self.assertFalse(f.is_valid())
        self.assertEqual(f.errors, {
            'title': [u'This field is required.'], 
            'authors': [u'This field is required.'], 
        })

    def test_valid_form(self):
        data = {'title': 'Test Title', 'url': 'http://example.com', 'journal':
        'Journal of Test', 'year': '2011', 'submit': 'Submit', 'volume': '1',
        'authors': "Author One\nAuthor Two\nAuthor Three",
        'issue': '2', 'pages': '3-4', }
        f = NewPaperForm(data)

        self.assertTrue(f.is_valid())
