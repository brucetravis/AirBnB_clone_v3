#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """
    Packs web_static into a .tgz archive
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Create the file name with timestamp
    now = datetime.utcnow()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Create the archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.failed:
        return None
    else:
        return "versions/{}".format(archive_name)
