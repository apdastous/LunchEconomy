from contextlib import contextmanager
import time

from fabric import colors
from fabric.context_managers import prefix, cd, settings
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.utils import puts, abort


env.user = 'www-lunch'
env.repository_url = 'https://github.com/apdastous/LunchEconomy.git'
env.wsgi_app = 'lunch_economy.wsgi:application'


@task
def dev():
    env.hosts = ['dev.lunch-economy.com']
    env.branch = 'development'
    env.base_directory = '/opt/lunch-economy/dev/'
    env.activate = env.base_directory + 'env/bin/activate'
    env.releases_directory = env.base_directory + 'releases/'
    env.requirements = env.releases_directory + 'current/requirements/dev.txt'
    env.gunicorn_conf = 'deploy.gunicorn_dev_conf'  # Relative to fabfile
    env.log_directory = '/var/log/lunch-economy/dev/'


@task
def prod():
    env.hosts = ['lunch-economy.com']
    env.branch = 'master'
    env.base_directory = '/opt/lunch-economy/prod/'
    env.activate = env.base_directory + 'env/bin/activate'
    env.releases_directory = env.base_directory + 'current/releases/'
    env.requirements = env.releases_directory + 'current/requirements/common.txt'
    env.gunicorn_conf = 'deploy.gunicorn_prod_conf'  # Relative to fabfile
    env.log_directory = '/var/log/lunch-economy/prod/'


@task
def setup():
    make_directories()
    clone_repository()
    checkout_latest()
    create_virtualenv()


@task
def deploy():
    checkout_latest()
    symlink_current_release()
    install_pip_requirements()
    sync_db()


@contextmanager
def virtualenv():
    with prefix("source " + env.activate):
        yield


def make_directories():
    run("mkdir -p " + env.releases_directory)
    run("mkdir -p " + env.log_directory)


def clone_repository():
    with cd(env.base_directory):
        run("git clone " + env.repository_url + " repository")


def checkout_latest():
    env.release = time.strftime('%Y%m%d%H%M%S')
    with cd(env.base_directory):
        run("cd repository; git pull origin " + env.branch)
        run("mkdir -p releases/")
        run("cp -R repository releases/" + env.release)
        run("rm -rf releases/" + env.release + "/.git*")


def symlink_current_release():
    with settings(warn_only=True):
        with cd(env.base_directory):
            run("rm releases/previous")
            run("mv releases/current releases/previous")
            run("ln -s " + env.release + " releases/current")


def create_virtualenv():
    with cd(env.base_directory):
        run("virtualenv --no-site-packages env")


def install_pip_requirements():
    with virtualenv():
        run("pip install --download-cache /tmp/" + env.user + "/pip-cache -r " + env.requirements)


def sync_db():
    with cd(env.base_directory):
        run("mkdir -p db/")
        run("python manage.py syncdb --noinput")


