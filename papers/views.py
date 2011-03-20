from django.conf import settings
import django.contrib.messages as messages
from django.shortcuts import render_to_response, redirect, get_object_or_404
#from django.template import RequestContext
#from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
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
from .tasks import import_paper_url
from .helpers import random_md5, save_uploaded_file

#import datetime
import os

@render_to('papers/home.html')
def home(request):

    return {}

@login_required
@render_to('papers/dashboard.html')
def dashboard(request, sort_by = '-added'):
    SORT_KEYS = ('added', 'year', 'journal')
    #We want to set the state before modifying the sort_by variable.
    sort_current = sort_by[1:] if sort_by[1:] in SORT_KEYS else 'added'
    sort_state = {
            #By default, we sort by '-added'.
            'added': '+' if sort_by == '-added' else '-', # earliest to latest
            'year': '+' if sort_by == '-year' else '-', #latest to earliest
            'journal': '-' if sort_by == '+journal' else '+', #a to z
            }

    if sort_by[1:] in SORT_KEYS: #get rid of initial +/-
        #We don't actually have a field called 'added' in our model. The
        #corresponding field is 'created'. So we map it here.
        if sort_by[1:] == 'added':
            sort_by = '%s%s' % (sort_by[0], 'created')
        #order_by cannot accept '+field', it must be 'field'
        if sort_by[0] == '+':
            sort_by = sort_by[1:]
        p = Paper.objects.filter(user = request.user).order_by(sort_by)
    else:
        #Get papers (latest first)
        p = Paper.objects.filter(user = request.user).order_by('-pk')


    return {'papers': p, 'sort_state': sort_state, 'sort_current': sort_current}

@login_required
@render_to('papers/papers_view.html')
def papers_view(request, paper_id):
    p = get_object_or_404(Paper, user = request.user, local_id = paper_id)

    return {'paper': p}

@login_required
@render_to('papers/new_paper_manual.html')
def new_paper_manual(request, task_id = None):
    post = request.POST.copy() #because it is immutable

    #If task_id is specified, get the result and merge it into request.POST.
    if task_id:
        result = import_paper_url.AsyncResult(task_id)
        if result.ready() and result.successful():
            data = result.result
            #In-place merge of data into post array. Will overwrite any existing
            #conflicting POST data.
            post.update(data)

    #import pdb; pdb.set_trace()

    if request.method == 'POST':
        form = NewPaperForm(post, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            #print data
            
            p = Paper(user = request.user, title = data['title'], 
                    authors = data['authors'], journal = data['journal'], 
                    year = data['year'], volume = data['volume'], 
                    issue = data['issue'], pages = data['pages'], 
                    url = data['url'])
            #We save first in order to have a hash automatically generated
            p.save()

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
        if task_id:
            form = NewPaperForm(post)
        else:
            form = NewPaperForm()

    #Also create the get citation form
    import_url_form = ImportURLForm()


    return {'form': form, 'import_url_form': import_url_form}

@login_required
@render_to('papers/new_paper_auto.html')
def new_paper_auto(request):
    if request.method == 'POST':
        form = ImportURLForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            #print data

            #Get paper citation information in the background. Return the
            #task_id so that it can be polled.
            result = import_paper_url.delay(data['url'])
            task_id = result.task_id
            
            #Redirect to status.
            return redirect('new_paper_status', task_id)
    else: 
        form = ImportURLForm()

    return {'form': form}

@login_required
@render_to('papers/new_paper_status.html')
def new_paper_status(request, task_id):
    #There's no way of verifying that a task_id exists or not, unless we save it
    #manually.

    return {'task_id': task_id}


@login_required
@ajax_request
def papers_import_url_poll(request, task_id):
    '''
    Given a task_id, checks database to see if Task has completed. If so,
    returns parsed data from the Task.

    TODO: Maybe make this a generalized URL view where any task can be checked
    up on.
    '''

    #Reconstruct the task from the given id.
    result = import_paper_url.AsyncResult(task_id)

    response = {'is_done': False, 'success': False, 'data': False}
    if result.ready():
        response['is_done'] = True
        if result.successful():
            response['success'] = True
            #NOTE: We don't make use of the returned data at the moment.
            response['data'] = result.result
        #Otherwise, data is False

    return response


@login_required
@render_to('papers/papers_edit.html')
def papers_edit(request, paper_id):
    p = get_object_or_404(Paper, user = request.user, local_id = paper_id)

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
            #We save first in order to have a hash automatically generated
            p.save()

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

    return {'form': form}
