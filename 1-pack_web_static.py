#!/usr/bin/python3
""" Generates a .tgz archive from the contents of the web_static folder """
from fabric.api import local
from datetime import datetime


def do_pack():
    """ Generates a .tgz archive """

    local("mkdir -p versions/")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(time)
    res = local("tar -cvzf {} web_static".format(path))
    if res.failed:
        return None
    return path
