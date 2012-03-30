import os, sys
from os.path import join
PROJECT_ROOT_PATH = os.path.dirname(
os.path.dirname(os.path.abspath(__file__))
)
sys.path.insert(0, PROJECT_ROOT_PATH)
sys.path.insert(0, join(PROJECT_ROOT_PATH, "lib"))
sys.path.insert(0, join(PROJECT_ROOT_PATH, "src"))
sys.path.insert(0, join(PROJECT_ROOT_PATH, "apps"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()