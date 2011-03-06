from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag()
def paperurl(paper):
    '''
    Given a Paper object, returns the *relative* url to the paper.
    '''
    paper_url = '%s/%s/%s/%s' % (settings.UPLOAD_URL, paper.user.username,
            paper.hash, paper.file)
    return paper_url

@register.simple_tag(takes_context = True)
def quickview(context, paper):
    '''
    Given a Paper object, returns a url to quickview it with Google PDF Preview.
    '''
    request = context['request']
    quickview_url = 'http://docs.google.com/viewer?embedded=true&url=%s'
    relative_paper_url = paperurl(paper)
    paper_url = 'http://%s%s' % (request.get_host(), relative_paper_url)
    return quickview_url % paper_url

@register.filter
@stringfilter
def pm_to_arrow(val):
    '''
    Given a '+' or '-' string, returns an unicode up arrow for + and down arrow
    for '-'.
    '''
    if val == '+':
        return mark_safe('&uarr;')
    elif val == '-':
        return mark_safe('&darr;')
    
    return val

@register.filter
@stringfilter
def invert_pm(val):
    '''
    Given a '+' or '-' string, returns the opposite sign.
    '''
    if val == '+':
        return '-'
    elif val == '-':
        return '+'
    
    return val
