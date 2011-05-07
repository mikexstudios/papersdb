from dagny import Resource, action

from django.conf import settings
from papers import models


class Paper(Resource):

    @action
    def index(self, sort_by = '-added'):
        SORT_KEYS = ('added', 'year', 'journal')
        #We want to set the state before modifying the sort_by variable.
        self.sort_current = sort_by[1:] if sort_by[1:] in SORT_KEYS else 'added'
        self.sort_state = {
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
            p = models.Paper.objects.filter(user = self.request.user).order_by(sort_by)
        else:
            #Get papers (latest first)
            p = models.Paper.objects.filter(user = self.request.user).order_by('-pk')
        
        #Set output variables
        self.papers = p
