from contextlib import contextmanager
import time

from fabric.context_managers import prefix, cd, settings
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env


env.user = 'www-lunch'
env.repository_url = 'https://github.com/apdastous/LunchEconomy.git'
env.wsgi_app = 'lunch_economy.wsgi:application'


@task
def dev():
    env.hosts = ['dev.lunch-economy.com']
    env.branch = 'development'

    env.base_directory = '/opt/lunch-economy/dev/'
    env.db_directory = env.base_directory + 'db/'
    env.gunicorn_run_directory = env.base_directory + 'run/'
    env.releases_directory = env.base_directory + 'releases/'
    env.log_directory = '/var/log/lunch-economy/dev/'

    env.activate = env.base_directory + 'env/bin/activate'
    env.requirements = env.releases_directory + 'current/requirements/dev.txt'

    env.django_settings_module = 'lunch_economy.settings.dev'

    env.supervisor_job = 'lunch-economy-dev'


@task
def prod():
    env.hosts = ['lunch-economy.com']
    env.branch = 'master'

    env.base_directory = '/opt/lunch-economy/prod/'
    env.gunicorn_run_directory = env.base_directory + 'run/'
    env.db_directory = env.base_directory + 'db/'
    env.releases_directory = env.base_directory + 'current/releases/'
    env.log_directory = '/var/log/lunch-economy/prod/'

    env.activate = env.base_directory + 'env/bin/activate'
    env.requirements = env.releases_directory + 'current/requirements/common.txt'

    env.django_settings_module = 'lunch_economy.settings.prod'

    env.supervisor_job = 'lunch-economy-prod'


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
    run_tests()
    sync_db()
    restart()


@contextmanager
def virtualenv():
    with prefix("source " + env.activate):
        yield


def make_directories():
    run("mkdir -p " + env.base_directory)
    run("mkdir -p " + env.gunicorn_run_directory)
    run("mkdir -p " + env.releases_directory)
    run("mkdir -p " + env.db_directory)
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


def run_tests():
    with cd(env.releases_directory + "current/"):
        with virtualenv():
            run("python manage.py test --settings " + env.django_settings_module)


def sync_db():
    with cd(env.releases_directory + "current/"):
        with virtualenv():
            run("python manage.py syncdb --noinput --settings " + env.django_settings_module)


@task
def start():
    with settings(warn_only=True):
        run("sudo supervisorctl start " + env.supervisor_job)


@task
def stop():
    with settings(warn_only=True):
        run("sudo supervisorctl stop " + env.supervisor_job)


@task
def restart():
    with settings(warn_only=True):
        run("sudo supervisorctl restart " + env.supervisor_job)
