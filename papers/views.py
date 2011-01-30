from django.conf import settings
import django.contrib.messages as messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.template import RequestContext
#from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from django.contrib.contenttypes.models import ContentType #for adding perm
#from django.contrib.auth.models import Permission #for adding perm
from django.db import models #for aggregator methods

#The reason why we use django's urlencode instead of urllib's urlencode is that
#django's version can operate on unicode strings.
#from django.utils.http import urlencode

from annoying.decorators import render_to
#from annoying.functions import get_object_or_None

from .forms import NewPaperForm
from .models import Paper
#from .tasks import 

#import datetime

@render_to('papers/home.html')
def home(request):

    return {}

@render_to('papers/dashboard.html')
def dashboard(request):

    return {}

@render_to('papers/new_paper.html')
def new_paper(request):
    if request.method == 'POST':
        form = NewPaperForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            
            p = Paper(title = data['title'], authors = data['authors'], 
                      journal = data['journal'], year = data['year'],
                      volume = data['volume'], issue = data['issue'], 
                      pages = data['pages'], url = data['url'])
            p.save()

            #Redirect to dashboard.
            messages.success(request, 'Paper was successfully added.')
            return redirect('dashboard')
    else: 
        form = NewPaperForm()

    return {'form': form}

