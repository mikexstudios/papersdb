from dagny import Resource, action

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import django.contrib.messages as messages
from annoying.decorators import ajax_request

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
                
                #Try to detect if the paper is a preprint/ASAP article and warn
                #user to check the ASAP box if so.
                if not data.get('year', False):
                    self.is_asap_detected = True

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
        
        #Otherwise, invalid form. Re-render the new page with form errors.
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
                path = os.path.join(settings.UPLOAD_ROOT, self.request.user.username,
                        p.hash)
                helpers.save_uploaded_file(data['file'], path)

                p.file = data['file'].name
                p.save()

            #Redirect to dashboard.
            messages.success(self.request, 'Paper was successfully added.')
            return redirect('Paper#index')

        #Otherwise, invalid form. Re-render the new_manual page with form errors.
        #Try to detect if the paper is a preprint/ASAP article and warn user
        #to check the ASAP box if so.
        if not self.request.POST.get('is_asap', False) and \
           not self.request.POST.get('year', False):
            self.is_asap_detected = True
        return self.new_manual.render()

    @action
    @action.deco(ajax_request)
    def import_url_poll(self, task_id):
        '''
        Given a task_id, checks database to see if Task has completed. If so,
        returns parsed data from the Task.

        TODO: Maybe make this a generalized URL view where any task can be checked
        up on.
        '''
        #Reconstruct the task from the given id.
        result = tasks.import_paper_url.AsyncResult(task_id)

        response = {'is_done': False, 'success': False, 'data': False}
        if result.ready():
            response['is_done'] = True
            if result.successful():
                response['success'] = True
                #NOTE: We don't make use of the returned data at the moment.
                response['data'] = result.result
            #Otherwise, data is False

        return response

    @action
    def edit(self, paper_id):
        self.paper = get_object_or_404(models.Paper, user = self.request.user, local_id = paper_id)
        self.form = forms.PaperForm(instance = self.paper)

        #Try to detect if the paper is a preprint/ASAP article and warn
        #user to check the ASAP box if so.
        if not self.paper.is_asap and not self.paper.year:
            self.is_asap_detected = True

    @action
    def update(self, paper_id):
        self.paper = get_object_or_404(models.Paper, user = self.request.user, local_id = paper_id)
        p_file = self.paper.file #Need to make a copy of this since the ModelForm overwrites it.
        self.form = forms.PaperForm(self.request.POST, self.request.FILES, instance = self.paper)

        if self.form.is_valid():
            data = self.form.cleaned_data
            #print data

            #NOTE: Checking for unicode type is an ugly hack.
            if data['file'] and type(data['file']) != unicode:
                path = os.path.join(settings.UPLOAD_ROOT, self.request.user.username,
                        self.paper.hash)

                #If there is an existing file, delete that first. Also delete
                #the associated thumbnail.
                if p_file:
                    try:
                        os.unlink(os.path.join(path, p_file))
                        os.unlink(os.path.join(path, settings.THUMBNAIL_FILENAME % self.paper.hash))
                        self.paper.has_thumbnail = False
                        self.paper.save()

                        #Also delete the existing crocodoc upload
                        self.paper.crocodoc.delete()
                    except OSError:
                        #The file is already missing.
                        pass

                #Save file. data.file is an UploadedFile object.
                helpers.save_uploaded_file(data['file'], path)

                self.form.file = data['file'].name
                self.paper = self.form.save() #save first so that we can generate thumbnail

            self.form.save()

            #Redirect to individual paper.
            messages.success(self.request, 'Paper was successfully updated.')
            return redirect('Paper#show', paper_id)

        #Otherwise, invalid form. Re-render the edit page with form errors.
        #Try to detect if the paper is a preprint/ASAP article and warn user
        #to check the ASAP box if so.
        if not self.request.POST.get('is_asap', False) and \
           not self.request.POST.get('year', False):
            self.is_asap_detected = True
        return self.edit.render()


    @action
    def quickview(self, paper_id):
        self.paper = get_object_or_404(models.Paper, user = self.request.user, local_id = paper_id)

        #Redirect to Crocodoc's public viewing url, if exists
        if self.paper.crocodoc and self.paper.crocodoc.short_id:
            return redirect(self.paper.crocodoc.embeddable_url())

        #Otherwise, redirect back to individual show page
        return redirect('Paper#show', paper_id)

    @action
    def download(self, paper_id):
        self.paper = get_object_or_404(models.Paper, user = self.request.user, local_id = paper_id)

        #Redirect to the file for download, if exists
        if self.paper.file:
            return redirect(self.paper.get_file_url())

        #Otherwise, redirect back to individual show page
        return redirect('Paper#show', paper_id)




#All pages in paper must require prior login.
Paper = Paper._decorate(login_required)
