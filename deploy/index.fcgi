#!/usr/bin/python
import os, sys
from os.path import join

PROJECT_ROOT_PATH = '/home/iellos/iellos'
sys.path.insert(0, PROJECT_ROOT_PATH)
sys.path.insert(0, os.path.dirname(PROJECT_ROOT_PATH))
sys.path.insert(0, join(PROJECT_ROOT_PATH, "lib"))
sys.path.insert(0, join(PROJECT_ROOT_PATH, "src"))
sys.path.insert(0, join(PROJECT_ROOT_PATH, "apps"))

# Switch to the directory of your project.
os.chdir(PROJECT_ROOT_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = "iellos.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
