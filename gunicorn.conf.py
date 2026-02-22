import multiprocessing

bind = "unix:/var/run/gunicorn/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 60
max_requests = 500
max_requests_jitter = 100
preload_app = True
