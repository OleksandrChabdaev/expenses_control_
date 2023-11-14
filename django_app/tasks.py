import os
import threading
import time

from invoke import task


def wait_port_is_open(host, port):
    import socket

    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return False
        except socket.gaierror:
            pass
        time.sleep(1)


# @task
# def cron(ctx):
#     ctx.run("python manage.py crontab add")
#     ctx.run("service cron start")


@task
def init_db(ctx, recreate_db=False):
    wait_port_is_open(os.getenv("POSTGRES_HOST", "db"), 5432)
    if recreate_db:
        ctx.run("python -m manage dbshell < clear.sql")
        ctx.run("python -m manage dbshell < ./db.dump")
    ctx.run("./manage.py makemigrations")
    ctx.run("./manage.py migrate")


@task
def collect_static_element(ctx):
    ctx.run("python -m manage collectstatic --noinput")


@task
def run_local(ctx):
    init_db(ctx, recreate_db=False)
    collect_static_element(ctx)

    # thread_cron = threading.Thread(target=cron, args=(ctx,))
    # thread_cron.start()

    ctx.run("./manage.py runserver 0.0.0.0:8000")


@task
def test(ctx):
    wait_port_is_open(os.getenv("POSTGRES_HOST", "db"), 5432)
    ctx.run("python -m manage test")
