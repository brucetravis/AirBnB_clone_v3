#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers using do_deploy.
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Change this to your username

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers using Fabric.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Create the release directory
        release_dir = '/data/web_static/releases/'
        run('mkdir -p {}'.format(release_dir))

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension>
        archive_filename = archive_path.split('/')[-1]
        release_folder = release_dir + archive_filename[:-4]  # Remove the '.tgz' extension
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents to the release folder and remove unnecessary folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))
        run('rm -rf {}/web_static'.format(release_folder))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version
        run('ln -s {} /data/web_static/current'.format(release_folder))

        print("New version deployed!")

        return True

    except Exception as e:
        return False

if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print("Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=your_archive.tgz")
    else:
        do_deploy(argv[2])
