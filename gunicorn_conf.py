import multiprocessing
import os

# Gunicorn config variables
bind = "0.0.0.0:5000"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "120"))
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "5"))
workers = int(os.getenv("GUNICORN_WORKERS", str(max(2, multiprocessing.cpu_count()))))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = os.getenv(
    "GUNICORN_WORKER_CLASS", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
)
wsgi_app = "app.main:app"
