from django.conf import settings

from celery.task import task

#from .models import 

import time
from subprocess import Popen, PIPE #for executing external command
import sys
import os
import re

@task
def add(x, y):
    return x + y

@task
def import_paper_url(url):
    '''
    Given a url, calls external program to obtain citation information. If
    successful, will parse citation information and return a structured
    format.
    '''
    parser = os.path.join(settings.PARSER_PATH, 'driver.tcl')
    #TODO: urlencode url to remove special characters
    command = "%s parse '%s'" % (parser, url)
    output = Popen(command, stdout=PIPE, shell=True,
             close_fds=True).stdout.read()
    #print output

    #Parse output. This is specific for citeulike's parser.
    lines = output.splitlines()
    citation = {}
    for line in lines:
        try:
            k, v = re.split(' -> ', line)
            citation[k] = v

            #The URL entered was directed to a parser, but nothing could be
            #parsed on that page.
            if citation.get('status') == 'err':
                return False
        except ValueError:
            #Means that splitting did not work. Let's keep going.
            continue

    #Correct for authors. The authors list is formatted like:
    #last_name first_name initials {raw_name}
    #ex. {Boettcher Shannon SW {Boettcher, Shannon W.}} {Warren Emily EL
    #    {Warren, Emily L.}} {Putnam Morgan MC {Putnam, Morgan C.}} 
    if citation.get('authors'):
        #Find the shortest match
        authors = re.findall(r'{.+?}}', citation['authors'])
        #For now, let's return the raw author name.
        simplified_authors = []
        for a in authors:
            m = re.match(r'^.*{(.+)}}$', a)
            if m:
                simplified_authors.append(m.group(1))
        #Flatten into a string with new lines separating the authors.
        citation['authors'] = '\n'.join(simplified_authors)
        

    #Simplify start and end pages to a single field: pages
    #We assume that we'll always have a start page.
    citation['pages'] = '%s-%s' % (citation.get('start_page'), 
                                   citation.get('end_page'))
    #If either of the pages is empty, we reduce the surrounding characters.
    #ex. '1482 - ' -> '1482'
    citation['pages'] = citation['pages'].strip('- ')
    
    return citation

@task
def generate_paper_thumbnail(paper):
    '''
    Given a Paper with an associated uploaded file, will call imagemagick on the
    file to generate a thumbnail of it.
    '''
    #Make sure that the paper has an associated uploaded file
    if not paper.file:
        return False

    #Make sure that the file exists
    paper_dir = os.path.join(settings.UPLOAD_ROOT, paper.user.username, paper.hash)
    paper_file = os.path.join(paper_dir, paper.file)
    if not os.path.exists(paper_file):
        return False

    #Generate the thumbnail
    thumbnail_file = os.path.join(paper_dir, settings.THUMBNAIL_FILENAME % paper.hash)
    command = settings.IMAGEMAGICK_CMD % ({'document': paper_file, 
                                           'thumbnail': thumbnail_file})
    output = Popen(command, stdout=PIPE, shell=True,
             close_fds=True).stdout.read()
    print output

    #Verify that the thumbnail exists
    if not os.path.exists(thumbnail_file):
        return False

    #Everything is good! Set flag to indicate that thumbnail has been generated!
    paper.has_thumbnail = True
    return True

