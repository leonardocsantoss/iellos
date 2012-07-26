from __future__ import with_statement
from fabric.api import *

env.hosts = [
    'root@iellos.com',
]
env.warn_only = True

def deploy():
    with cd('/var/apps/iellos/'):
        # get lastest version from git
        run('git pull')
        # restart apache
        run('/etc/init.d/apache2 restart')