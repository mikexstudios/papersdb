from django.conf import settings
from django.test import TestCase
#from django.test.client import Client

#from django.contrib.auth.models import User
#from .models import 

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re

from papers.forms import NewPaperForm
class AddPaperFormTest(TestCase):

    def setUp(self):
        #This is dummy valid data.
        self.data = {'title': 'Test Title', 'url': 'http://example.com',
                'journal': 'Journal of Test', 'year': '2011', 'submit':
                'Submit', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', }

    def tearDown(self):
        pass

    def test_empty_form_errors(self):
        #Make all the values in the data empty
        data = dict((k, '') for (k, v) in self.data.iteritems())
        f = NewPaperForm(data)

        self.assertFalse(f.is_valid())
        self.assertEqual(f.errors, {
            'title': [u'This field is required.'], 
            'authors': [u'This field is required.'], 
        })

    def test_valid_form(self):
        f = NewPaperForm(self.data)

        self.assertTrue(f.is_valid())

    def test_normalize_authors_newlines(self):
        '''
        Since each author is entered on a new line, depending on the OS, the newline
        delimiter may not be only '\n'. Thus, we check to make sure that all newlines
        are converted to '\n'.
        '''
        expected_authors = "Author One\nAuthor Two\nAuthor Three"
        data = self.data.copy()

        cases = [
            #CR+LF newline (Windows)
            "Author One\r\nAuthor Two\r\nAuthor Three",
            #LF newline (*nix)
            "Author One\nAuthor Two\nAuthor Three",
            #CR newline (Old OSes)
            "Author One\rAuthor Two\rAuthor Three",
            #Mixed newline
            #NOTE: This fails because \n\r is considered two newlines. We'll
            #      accept that.
            #"Author One\rAuthor Two\n\rAuthor Three",
        ]

        for c in cases:
            data['authors'] = c

            f = NewPaperForm(data)
            self.assertTrue(f.is_valid())
            self.assertEqual(f.cleaned_data['authors'], expected_authors)