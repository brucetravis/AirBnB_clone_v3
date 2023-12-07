#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Update with your SSH username
env.key_filename = ['my_ssh_private_key.pem']  # Update with your SSH private key path

def do_pack():
    """
    Packs web_static into a .tgz archive
    """
    # ... (same as previous script)

def do_deploy(archive_path):
    """
    Deploys an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to a specific folder
        run('mkdir -p /data/web_static/releases/')
        release_folder = '/data/web_static/releases/{}'.format(
            datetime.utcnow().strftime('%Y%m%d%H%M%S'))
        run('tar -xzf /tmp/{} -C {}'.format(archive_path.split('/')[1], release_folder))

        # Move files from the extracted folder to the web_static folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Remove unnecessary directories
        run('rm -rf {}/web_static'.format(release_folder))

        # Create a symbolic link
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False

def deploy():
    """
    Deploys the web_static content to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()
