from django.conf import settings

from celery.task import task

import crocodoc

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
    command = "tclsh %s parse '%s'" % (parser, url)
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
    citation['pages'] = '%s-%s' % (citation.get('start_page', ''), 
                                   citation.get('end_page', ''))
    #If either of the pages is empty, we reduce the surrounding characters.
    #ex. '1482 - ' -> '1482'
    citation['pages'] = citation['pages'].strip('- ')

    #Apply some corrections to the data, mainly for ASAP documents. If any of
    #the given fields has <= 0 numerical value, then we blank the field.
    for k in ['year', 'volume', 'issue', 'pages']:
        try:
            if int(citation[k]) <= 0:
                del citation[k]
        except ValueError: #can't cast to int
            continue
    
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

    if paper.has_thumbnail:
        return True #thumbnail already generated

    #Make sure that the file exists
    paper_dir = paper.get_file_dir()
    paper_file = paper.get_file_path()
    if not os.path.exists(paper_file):
        return False

    #Generate the thumbnail
    thumbnail_file = os.path.join(paper_dir, settings.THUMBNAIL_FILENAME % paper.hash)
    command = settings.IMAGEMAGICK_CMD % ({'document': paper_file, 
                                           'thumbnail': thumbnail_file})
    output = Popen(command, stdout=PIPE, shell=True,
             close_fds=True).stdout.read()
    #print output

    #Verify that the thumbnail exists
    if not os.path.exists(thumbnail_file):
        return False

    #Everything is good! Set flag to indicate that thumbnail has been generated!
    paper.has_thumbnail = True
    paper.save()
    return True


@task
def crocodoc_upload_paper(paper, method = 'url'):
    '''
    Given a Paper with an associated uploaded file, will upload the Paper to
    Crocodoc via the URL method.

    @param method string 'url' or 'post' depending on the upload method.
    '''
    #Make sure that the paper has an associated uploaded file
    if not paper.file:
        return False

    #Double check again that in the time it took to execute this task, that
    #the paper wasn't already uploaded.
    if paper.crocodoc.uuid:
        return True

    c = crocodoc.Crocodoc(settings.CROCODOC_API_KEY)
    #NOTE: We do not upload in async mode since we want to immediately be able
    #      to set the document as viewable. This may slow down queue processing
    #      a bit though.
    if method == 'post': #good for local testing
        with open(paper.get_file_path(), 'r') as f:
            r = c.upload(f, private = True)
    else:
        r = c.upload(paper.get_file_url(), private = True)

    try:
        paper.crocodoc.short_id = r['shortId']
        paper.crocodoc.uuid = r['uuid']
        paper.crocodoc.save()
    except KeyError, exc:
        #Means that the document was not sucessfully uploaded or perhaps we
        #ran into a rate limiting issue. So let's try again.
        return crocodoc_upload_paper.retry(exc = exc)

    #Also obtain a session_id for the document.
    crocodoc_get_session_id(paper)

    return True

@task
def crocodoc_get_session_id(paper):
    '''
    Given a paper with crocodoc information, obtains a session id.

    TODO: Think about adding retry to failing session_id getting.
    '''
    if not paper.file or not paper.crocodoc.uuid:
        return False

    c = crocodoc.Crocodoc(settings.CROCODOC_API_KEY)
    r = c.get_session(paper.crocodoc.uuid)
    try:
        paper.crocodoc.session_id = r['sessionId']
        paper.crocodoc.save()
    except KeyError:
        return False

    return True
    
@task
def crocodoc_delete_uuid(uuid):
    '''
    Given a uuid, deletes the upload. We accept uuid instead of Paper object
    since the Paper object may have already been deleted by the time this
    task is called.
    '''
    c = crocodoc.Crocodoc(settings.CROCODOC_API_KEY)
    r = c.delete(uuid)
    if not r:
        #Means that there was something wrong when deleting the file. For now,
        #let's do nothing.
        pass

    return True
