from django.conf import settings
from django.test import TestCase
#from django.test.client import Client

#from django.contrib.auth.models import User
#from .models import 

#from .helpers import 

#from datetime import datetime, date

#from annoying.functions import get_object_or_None

import re
import os

from papers.forms import NewPaperForm
from django.core.files.uploadedfile import SimpleUploadedFile
class AddPaperFormTest(TestCase):

    def setUp(self):
        #This is dummy valid data.
        self.post = {'title': 'Test Title', 'url': 'http://example.com',
                'journal': 'Journal of Test', 'year': '2011', 'submit':
                'Submit', 'volume': '1', 'authors': 
                "Author One\nAuthor Two\nAuthor Three", 'issue': '2', 'pages':
                '3-4', }

        #This is a dummy blank pdf.
        self.TEST_FILES_PATH = os.path.join(settings.SITE_ROOT, 'papers',
                                            'tests', 'files')
        f = open(os.path.join(self.TEST_FILES_PATH, 'blank.pdf'), 'rb')
        self.files = {'file': SimpleUploadedFile(f.name, f.read())}
        f.close()

    def tearDown(self):
        pass

    def test_empty_form_errors(self):
        #Make all the values in the data empty
        post = dict((k, '') for (k, v) in self.post.iteritems())
        f = NewPaperForm(post)

        self.assertFalse(f.is_valid())
        self.assertEqual(f.errors, {
            'title': [u'This field is required.'], 
            'authors': [u'This field is required.'], 
        })

    def test_valid_form(self):
        f = NewPaperForm(self.post, self.files)

        self.assertTrue(f.is_valid())

    def test_normalize_authors_newlines(self):
        '''
        Since each author is entered on a new line, depending on the OS, the newline
        delimiter may not be only '\n'. Thus, we check to make sure that all newlines
        are converted to '\n'.
        '''
        expected_authors = "Author One\nAuthor Two\nAuthor Three"
        post = self.post.copy()

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
            post['authors'] = c

            f = NewPaperForm(post)
            self.assertTrue(f.is_valid())
            self.assertEqual(f.cleaned_data['authors'], expected_authors)

    def test_invalid_upload_file(self):
        '''
        If uploaded file does not have extension of
        settings.ALLOWED_UPLOAD_EXTENSIONS, then file should be rejected.
        '''
        #This is a dummy blank png file, which is not allowed.
        f = open(os.path.join(self.TEST_FILES_PATH, 'blank.png'), 'rb')
        invalid_files = self.files.copy()
        invalid_files['file'] = SimpleUploadedFile(f.name, f.read())
        f.close()
        
        f = NewPaperForm(self.post, invalid_files)
        self.assertFalse(f.is_valid())

    def test_oversized_upload_file(self):
        '''
        If uploaded file size is greater than
        settings.MAXIMUM_UPLOAD_SIZE_BYTES, then file should be rejected.
        '''
        #Temporarily set maximum file size to 0.
        temp = settings.MAXIMUM_UPLOAD_SIZE_BYTES
        settings.MAXIMUM_UPLOAD_SIZE_BYTES = 0

        f = NewPaperForm(self.post, self.files)
        self.assertFalse(f.is_valid())

        #Undo setting
        settings.MAXIMUM_UPLOAD_SIZE_BYTES = temp
