from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag(takes_context = True)
def quickview(context, paper):
    '''
    Given a Paper object, returns a url to quickview it with Google PDF Preview.
    '''
    request = context['request']
    quickview_url = 'http://docs.google.com/viewer?embedded=true&url=%s'
    paper_url = 'http://%s%s/%s/%s/%s' % (request.get_host(),
            settings.UPLOAD_URL, paper.user.username, paper.hash, paper.file)
    return quickview_url % paper_url
