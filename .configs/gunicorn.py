# Gunicorn configuration file.
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)

if os.environ.get("ENVIRONMENT", "local") == "production":
    bind = "0.0.0.0:8000"

if os.environ.get("ENVIRONMENT", "local") == "local":
    reload = True

backlog = 2048
workers = 4
worker_connections = 1000
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 30
keepalive = 2
spew = False
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "INFO")
accesslog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
proc_name = None


def post_fork(server, worker):
    """Server post-fork hook."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    """Server pre-fork hook."""
    pass


def pre_exec(server):
    """Server pre-exec hook."""
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    """Server ready hook."""
    server.log.info("Server is ready. Spawning workers")


def worker_int(worker):
    """Worker int hook."""
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading
    import sys
    import traceback

    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId, ""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))


def worker_abort(worker):
    """Worker abort hook."""
    worker.log.info("worker received SIGABRT signal")


def ssl_context(conf, default_ssl_context_factory):
    """SSL context hook."""
    import ssl

    # The default SSLContext returned by the factory function is initialized
    # with the TLS parameters from config, including TLS certificates and other
    # parameters.
    context = default_ssl_context_factory()

    # The SSLContext can be further customized, for example by enforcing
    # minimum TLS version.
    context.minimum_version = ssl.TLSVersion.TLSv1_3

    # Server can also return different server certificate depending which
    # hostname the client uses. Requires Python 3.7 or later.
    def sni_callback(socket, server_hostname, context):
        if server_hostname == "foo.127.0.0.1.nip.io":
            new_context = default_ssl_context_factory()
            new_context.load_cert_chain(certfile="foo.pem", keyfile="foo-key.pem")
            socket.context = new_context

    context.sni_callback = sni_callback

    return context
