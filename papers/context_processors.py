from django.conf import settings

def sitename(request):
    '''
    Adds sitename defined in settings to the context.
    '''
    return {'SITENAME': settings.SITENAME}
