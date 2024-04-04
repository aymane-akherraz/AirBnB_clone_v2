#!/usr/bin/python3
""" Distributes an archive to your web servers """
from fabric.api import put, run, env
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
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{}.tgz -C {}/'.format(archive_path, path))
        run('rm /tmp/{}.tgz'.format(archive_path))
        run('mv {}/web_static/* {}/'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(path))
        return True
    except:
        return False
