from django.conf import settings
from django import forms

#from .models import 

#import re

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
