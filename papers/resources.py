from dagny import Resource, action

from django.conf import settings
from papers import models
from django.shortcuts import redirect, get_object_or_404


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
