#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime
from os.path import exists
from os import listdir

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'bruceambundo'  # Update with your SSH username
env.key_filename = ['my_ssh_private_key.pem']  # Update with your SSH private key path

def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number < 0:
        return

    # Clean local archives
    local_archives = sorted(listdir('versions'), reverse=True)
    for local_archive in local_archives[number:]:
        local('rm -f versions/{}'.format(local_archive))

    # Clean remote archives
    remote_archives = run('ls -1 /data/web_static/releases/').split('\n')
    remote_archives = sorted(remote_archives, reverse=True)
    for remote_archive in remote_archives[number:]:
        run('rm -rf /data/web_static/releases/{}'.format(remote_archive))

if __name__ == "__main__":
    do_clean()
