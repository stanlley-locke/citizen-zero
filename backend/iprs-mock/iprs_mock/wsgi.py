"""
WSGI config for iprs_mock project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iprs_mock.settings')

application = get_wsgi_application()
