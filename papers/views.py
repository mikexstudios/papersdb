#from django.conf import settings
#import django.contrib.messages as messages
#from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.template import RequestContext
#from django.core.urlresolvers import reverse
#from django.http import HttpResponse, HttpResponseBadRequest
#from django.views.decorators.http import require_POST
#from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth.decorators import login_required
#from django.contrib.contenttypes.models import ContentType #for adding perm
#from django.contrib.auth.models import Permission #for adding perm
#from django.db import models #for aggregator methods

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
#from django.utils.http import urlencode

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

#from .forms import ImportURLForm, PaperForm
#from .models import Paper
#from .tasks import import_paper_url
#from .helpers import random_md5, save_uploaded_file

#import datetime
#import os

@render_to('paper/home.html')
def home(request):

    return {}
