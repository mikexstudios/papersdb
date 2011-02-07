#from django.conf import settings

#from .models import 

#import datetime
#import calendar
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
