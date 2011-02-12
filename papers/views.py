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

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

from .forms import NewPaperForm, ImportURLForm
from .models import Paper
#from .tasks import 
from .helpers import random_md5, save_uploaded_file

#import datetime
import os

@render_to('papers/home.html')
def home(request):

    return {}

@login_required
@render_to('papers/dashboard.html')
def dashboard(request):
    #Get papers (latest first)
    p = Paper.objects.filter(user = request.user).order_by('-pk')

    return {'papers': p}

@login_required
@render_to('papers/new_paper.html')
def new_paper(request):
    if request.method == 'POST':
        form = NewPaperForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            
            p = Paper(user = request.user, title = data['title'], 
                    authors = data['authors'], journal = data['journal'], 
                    year = data['year'], volume = data['volume'], 
                    issue = data['issue'], pages = data['pages'], 
                    url = data['url'])
            #Generate a random hash that will be used as a non-guessable ID
            #for this paper.
            p.hash = random_md5()

            if data['file']:
                #Save file. data.file is an UploadedFile object.
                path = os.path.join(settings.UPLOAD_ROOT, request.user.username,
                        p.hash)
                save_uploaded_file(data['file'], path)

                p.file = data['file'].name

            p.save()

            #Redirect to dashboard.
            messages.success(request, 'Paper was successfully added.')
            return redirect('dashboard')
    else: 
        form = NewPaperForm()

    #Also create the get citation form
    import_url_form = ImportURLForm()


    return {'form': form, 'import_url_form': import_url_form}

@login_required
@ajax_request
def papers_import_url(request):
    if request.method == 'POST':
        form = ImportURLForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            
            #TODO: Execute task to grab paper data. Then return some id so that
            #      the check status can be polled.
            return {'id': 435253, 'success': True}

    #Means that user accessed url directly or form failed.
    return {'success': False}

@login_required
@ajax_request
def papers_import_url_poll(request, import_id):
    '''
    Given an import_id, checks database to see if Task has completed. If so,
    returns parsed data from the Task.
    '''

    return {'is_done': False}

