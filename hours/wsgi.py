import os
import sys

path = '/path/to/CVAM-hours/hours'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
