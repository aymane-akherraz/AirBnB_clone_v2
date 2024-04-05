#!/usr/bin/python3
""" Distributes an archive to your web servers """
from fabric.api import put, run, env
from os import path


env.user = 'ubuntu'
env.hosts = ['52.86.133.238', '52.87.211.253']


def do_deploy(archive_path):
    """ Distributes an archive to your web servers """

    if not path.exists(archive_path):
        return False

    if put(archive_path, '/tmp/').failed:
        return False

    archive_path = archive_path.split('/')[1].strip('.tgz')

    path = "/data/web_static/releases/{}".format(archive_path)
    if run('mkdir -p {}/'.format(path)).failed:
        return False
    if run('tar -xzf /tmp/{}.tgz -C {}/'.format(archive_path, path)).failed!
        return False
    if run('rm /tmp/{}.tgz'.format(archive_path)).failed:
        return False
    if run('mv {}/web_static/* {}/'.format(path, path)).failed:
        return False
    if run('rm -rf {}/web_static'.format(path)).failed:
        return False
    if run('rm -rf /data/web_static/current').failed:
        return False
    if run('ln -s {}/ /data/web_static/current'.format(path)).failed:
        return False
    return True
