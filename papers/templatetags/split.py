from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, delimiter):
    '''
    NOTE: This doesn't work right now because django escapes the delimiter!
    So \n becomes \\n
    '''
    return value.split(delimiter)

@register.filter
@stringfilter
def splitlines(value):
    return value.splitlines()
