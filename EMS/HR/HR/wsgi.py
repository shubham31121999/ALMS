"""
WSGI config for HR project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HR.settings")

# application = get_wsgi_application()
import os
import sys
from django.core.wsgi import get_wsgi_application

print("Setting DJANGO_SETTINGS_MODULE")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HR.settings')

print("Getting WSGI application")
try:
    application = get_wsgi_application()
    print("WSGI application successfully loaded")
except Exception as e:
    print(f"Failed to get WSGI application: {e}")
    raise

