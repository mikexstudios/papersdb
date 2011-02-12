from django.conf import settings

from celery.task import task

#from .models import 

import time

@task
def add(x, y):
    return x + y

@task
def import_paper_url(url):
    time.sleep(10)
    
    return {'title': 'My Sample title', 'authors': 'One Two Three'}
