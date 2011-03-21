#from django.conf import settings

#from .models import 

#import datetime
#import calendar
import os
import hashlib #encryption (MD5)
import time, random #used to seed encryption

def random_md5(seed = ''):
    '''
    Generates a random MD5 based on the current timestamp (in seconds). Can be
    made extra random by specifying a seed that is prepended to the timestamp.

    @return string 32-character length md5 hash
    '''
    #NOTE: There can be hash colllisons if this function is called too fast in 
    #      succession since the time hasn't had a chance to advance. So we
    #      add a random number generator too.
    s = seed + str(time.time() * random.random())
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()

def save_uploaded_file(f, path, filename = ''):
    '''
    Given an UploadedFile object, saves the data to disk.
    See: http://docs.djangoproject.com/en/dev/topics/http/file-uploads/

    @param f File object
    @param path The path where the file will saved.
    @param filename File name. Defaults to the file name of the File object.
    '''
    if filename == '':
        filename = f.name
    #Need to make the hash directory (if it doesn't already exist) before
    #saving file.
    try:
        os.makedirs(path, mode = 0755)
    except OSError:
        #Directory already exists. That's fine.
        pass
    save_path = os.path.join(path, filename)
    destination = open(save_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
