from contextlib import contextmanager
from importlib import import_module
import time
from fabric import colors

from fabric.context_managers import prefix, cd, settings, hide
from fabric.decorators import task
from fabric.operations import run
from fabric.state import env
from fabric.utils import puts, abort


env.user = 'www-data'
env.repository_url = 'https://github.com/apdastous/LunchEconomy.git'
env.wsgi_app = 'lunch_economy.wsgi:application'


@task
def dev():
    env.hosts = ['dev.lunch-economy.com']
    env.branch = 'development'
    env.base_directory = '/opt/lunch-economy/dev/'
    env.releases_directory = env.base_directory + 'releases/'
    env.activate = env.releases_directory + 'current/env/bin/activate'
    env.requirements = env.releases_directory + 'current/requirements/dev.txt'
    env.gunicorn_conf = env.releases_directory + 'current/deploy/gunicorn_dev.conf.py'
    env.log_directory = '/var/log/lunch-economy/dev/'


@task
def prod():
    env.hosts = ['lunch-economy.com']
    env.branch = 'master'
    env.base_directory = '/opt/lunch-economy/prod/'
    env.releases_directory = env.base_directory + 'current/releases/'
    env.activate = env.releases_directory + 'current/env/bin/activate'
    env.requirements = env.releases_directory + 'current/requirements/common.txt'
    env.gunicorn_conf = env.releases_directory + 'current/deploy/gunicorn_prod.conf.py'
    env.log_directory = '/var/log/lunch-economy/prod/'


@contextmanager
def virtualenv():
    with prefix("source " + env.activate):
        yield


@task
def setup():
    make_directories()
    clone_repository()
    checkout_latest()


@task
def deploy():
    checkout_latest()
    symlink_current_release()
    create_virtualenv()
    install_pip_requirements()
    sync_db()
    if not gunicorn_running():
        start_gunicorn()
    else:
        reload_gunicorn()


def make_directories():
    run("mkdir -p " + env.releases_directory)
    run("mkdir -p " + env.log_directory)


def create_virtualenv():
    with cd(env.releases_directory + "current/"):
        run("virtualenv --no-site-pacakges env")


def install_pip_requirements():
    with cd(env.releases_directory + "current/"):
        with virtualenv():
            run("pip install --download-cache /tmp/" + env.user + "/pip-cache -r " + env.requirements)


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


def sync_db():
    with cd(env.releases_directory + "current/"):
        run("python manage.py syncdb --noinput")


def gunicorn_running():
    gunicorn_conf = import_module(env.gunicorn_conf)
    return run("ls " + gunicorn_conf.pidfile, quiet=True).succeeded


def gunicorn_running_workers():
    count = None
    with hide('running', 'stdout', 'stderr'):
        count = run("ps -e -o ppid | grep `cat " + env.gunicorn_run_dir + "` | wc -l")
    return count


@task
def gunicorn_status():
    if gunicorn_running():
        puts(colors.green("Gunicorn is running."))
        puts(colors.green("Active workers: {0}".format(gunicorn_running_workers())))
    else:
        puts(colors.blue("Gunicorn isn't running."))


@task
def start_gunicorn():
    if gunicorn_running():
            puts(colors.red("Gunicorn is already running!"))
            return
    with cd(env.releases_directory + "current/"):
        with virtualenv():
            run("gunicorn " + env.wsgi_app + "-c " + env.gunicorn_conf)

    if gunicorn_running():
        puts(colors.green("Gunicorn started."))
    else:
        abort(colors.red("Gunicorn wasn't started!"))


@task
def stop_gunicorn():
    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return

    run('kill `cat %s`' % (env.gunicorn_pidpath))

    for timeout in range(0,10):
        if gunicorn_running():
            time.sleep(1)
        else:
            puts(colors.green("Gunicorn was stopped."))
            return
    else:
        abort(colors.red("Gunicorn wasn't stopped!"))


@task
def restart_gunicorn():
    stop_gunicorn()
    start_gunicorn()


@task
def reload_gunicorn():
    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return
    puts(colors.yellow('Gracefully reloading Gunicorn...'))
    gunicorn_conf = import_module(env.gunicorn_conf)
    run("kill -HUP `cat " + gunicorn_conf.pidfile + "`")