"""
WSGI config for django2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
bdir=os.path.dirname(os.path.abspath(__file__))
sys.path.append(bdir)
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appa.settings")

application = get_wsgi_application()
