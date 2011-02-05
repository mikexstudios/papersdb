from django.conf import settings
from django import forms
from django.utils.text import get_text_list #humanize a list

#from .models import 

#import re
import os

class NewPaperForm(forms.Form):
    title = forms.CharField(widget = forms.Textarea, label = 'Title')
    authors = forms.CharField(widget = forms.Textarea, label = 'Authors')
    journal = forms.CharField(required = False, max_length = 255, label = 'Journal')
    year = forms.IntegerField(required = False, min_value = 0, max_value = 99999,
            label = 'Year')
    #NOTE: Volume and issue may not necessarily be numbers.
    volume = forms.CharField(required = False, max_length = 255, label = 'Volume')
    issue = forms.CharField(required = False, max_length = 255, label = 'Issue')
    pages = forms.CharField(required = False, max_length = 255, label = 'Pages')
    url = forms.URLField(required = False, max_length = 9999, label = 'URL')

    file = forms.FileField(required = False, label='Upload Paper')

    def clean_authors(self):
        '''
        Normalize newlines to \n. Also remove any unnecessary whitespace.
        '''
        authors = self.cleaned_data['authors']
        return '\n'.join(authors.splitlines())

    def clean_file(self):
        '''
        Validation on uploaded file. Checks if file extension is allowed.
        '''
        uploaded_file = self.cleaned_data['file']

        #If file not actually submitted, skip clean.
        if not uploaded_file:
            return None
        
        #Check for allowed extensions:
        ext = os.path.splitext(uploaded_file.name)[1]
        ext = ext[1:] #get rid of .
        ext = ext.lower() #make lowercase
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            valid_files = ['.%s' % i for i in settings.ALLOWED_UPLOAD_EXTENSIONS]
            valid_files = get_text_list(valid_files, ', and')
            raise forms.ValidationError(
                'Not a valid file! Only %s files are allowed!' % valid_files
            )

        #Check for allowed file size:
        if uploaded_file.size > settings.MAXIMUM_UPLOAD_SIZE_BYTES:
            raise forms.ValidationError(
                'File is too large! Only files with size <= %s MB are allowed!' % settings.MAXIMUM_UPLOAD_SIZE_MB
            )
        
        #Otherwise, everything checks out:
        return uploaded_file
