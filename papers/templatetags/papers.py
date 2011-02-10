from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def quickview(paper):
    '''
    Given a Paper object, returns a url to quickview it with Google PDF Preview.
    '''
    quickview_url = 'http://docs.google.com/viewer?embedded=true&url=%s'
    paper_url = '%s/%s/%s/%s' % (settings.UPLOAD_URL, paper.user.username,
                              paper.hash, paper.file)
    return quickview_url % paper_url
