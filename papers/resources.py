from dagny import Resource, action

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
import django.contrib.messages as messages

from papers import models, forms, tasks, helpers

import os

class Paper(Resource):

    @action
    def index(self):
        #NOTE: This sorting code is all hackish. Let's nuke it sometime and start
        #      all over.
        sort_by = self.request.GET.get('sort_by', '-added')

        SORT_KEYS = ('added', 'year', 'journal')
        #We want to set the state before modifying the sort_by variable.
        self.sort_current = sort_by[1:] if sort_by[0] == '-' else sort_by #remove the '-' in front
        self.sort_current = self.sort_current if self.sort_current in SORT_KEYS else 'added'
        self.sort_state = {
                #By default, we sort by '-added'.
                #NOTE: Because the '+' character in urls is not interpreted, we
                #      assume '' to be '+' behavior.
                'added': '' if sort_by == '-added' else '-', # earliest to latest
                'year': '' if sort_by == '-year' else '-', #latest to earliest
                'journal': '-' if sort_by == 'journal' else '', #a to z
                }

        if self.sort_current in SORT_KEYS: #get rid of initial +/-
            #We don't actually have a field called 'added' in our model. The
            #corresponding field is 'created'. So we map it here.
            if sort_by == 'added':
                sort_by = 'created'
            if sort_by[1:] == 'added':
                sort_by = '%s%s' % (sort_by[0], 'created')
            p = models.Paper.objects.filter(user = self.request.user).order_by(sort_by)
        else:
            #Get papers (latest first)
            p = models.Paper.objects.filter(user = self.request.user).order_by('-pk')
        
        #Set output variables
        self.papers = p

    @action
    def show(self, paper_id):
        self.paper = get_object_or_404(models.Paper, user = self.request.user, local_id = paper_id)

    @action
    def new(self):
        self.form = forms.ImportURLForm()

    @action
    def new_manual(self, task_id = None):
        POST = self.request.POST.copy() #because it is immutable

        #If task_id is specified, get the result and merge it into request.POST.
        if task_id:
            result = tasks.import_paper_url.AsyncResult(task_id)
            if result.ready() and result.successful():
                data = result.result
                #In-place merge of data into post array. Will overwrite any existing
                #conflicting POST data.
                POST.update(data)

        if task_id:
            self.form = forms.PaperForm(POST)
        else:
            self.form = forms.PaperForm()

    @action
    def create(self):
        self.form = forms.ImportURLForm(self.request.POST)
        if self.form.is_valid():
            data = self.form.cleaned_data
            #print data

            #Get paper citation information in the background. Return the
            #task_id so that it can be polled.
            result = tasks.import_paper_url.delay(data['url'])
            task_id = result.task_id
            
            #Redirect to status.
            return redirect('Paper#create_status', task_id)
        
        #The following will render the page that create was called from. This will
        #display the original form with errors.
        return self.new.render()


    @action
    def create_status(self, task_id):
        self.task_id = task_id

    @action
    def create_manual(self):
        self.form = forms.PaperForm(self.request.POST, self.request.FILES)
        if self.form.is_valid():
            data = self.form.cleaned_data
            #print data
            
            p = models.Paper(user = self.request.user, title = data['title'], 
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
                helpers.save_uploaded_file(data['file'], path)

                p.file = data['file'].name
                p.save()

                #Call paper thumbnail generation task. Returns the AsyncResult
                #object, which was don't use here.
                p.generate_thumbnail()

            #Redirect to dashboard.
            messages.success(self.request, 'Paper was successfully added.')
            return redirect('Paper#index')

        #The following will render the page that create was called from. This will
        #display the original form with errors.
        return self.new.render()
