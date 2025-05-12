"""
WSGI config for reading_loft project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reading_loft.settings')

application = get_wsgi_application()
