"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application
    
# GETTING-STARTED: change 'myproject' to your project name:
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


try:
    application = get_wsgi_application()
    print 'WSGI without exception'
except Exception:
    print 'handling WSGI exception'
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)