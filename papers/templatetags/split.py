from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, delimiter):
    #django automatically escapes the delimiter. So we need to un-escape it:
    delimiter = delimiter.decode('unicode-escape')
    return value.split(delimiter)

@register.filter
@stringfilter
def splitlines(value):
    return value.splitlines()
