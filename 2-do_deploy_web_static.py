#!/usr/bin/python3
""" Distributes an archive to your web servers """
from fabric.api import *
import os

env.user = 'ubuntu'
env.hosts = ['52.86.133.238', '52.87.211.253']


def do_deploy(archive_path):
    """ Distributes an archive to your web servers """

    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        archive_path = archive_path.split('/')[1].strip('.tgz')
        path = "/data/web_static/releases/{}".format(archive_path)
        sudo('mkdir -p {}/'.format(path))
        sudo('tar -xzf /tmp/{}.tgz -C {}/'.format(archive_path, path))
        sudo('rm /tmp/{}.tgz'.format(archive_path))
        sudo('mv {}/web_static/* {}/'.format(path, path))
        sudo('rm -rf {}/web_static'.format(path))
        sudo('rm -rf /data/web_static/current')
        sudo('ln -s {}/ /data/web_static/current'.format(path))
        return True
    except Exception:
        return False
