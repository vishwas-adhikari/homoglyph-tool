"""
WSGI config for homoglyph_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Ensure this matches the correct path to your settings file.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homoglyph_project.settings')

application = get_wsgi_application()