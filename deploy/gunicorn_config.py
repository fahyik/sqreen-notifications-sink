import os

# heroku only listens on PORT
port = os.environ.get("PORT")

access_log_format = '%(h)s %(l)s %({Forwarded}i)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s'
workers = 2
worker_class = "gevent"
worker_connections = 500
bind = f"0.0.0.0:{port}"
timeout = 600
max_requests = 1000
max_requests_jitter = 4
