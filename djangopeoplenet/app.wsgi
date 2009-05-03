import os, sys

# Get rid of 'sys.stdout access restricted by mod_wsgi' error
sys.stdout = sys.stderr

paths = (
    '/home/simon/sites/djangopeople.net',
    '/home/simon/sites/djangopeople.net/djangopeoplenet',
    '/home/simon/sites/djangopeople.net/djangopeoplenet/djangopeople/lib',
)
for path in paths:
    if not path in sys.path:
        sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangopeoplenet.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

