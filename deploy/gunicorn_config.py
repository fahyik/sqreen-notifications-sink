workers = 3
worker_class = "gevent"
worker_connections = 500
bind = "0.0.0.0:5000"
timeout = 600
max_requests = 1000
max_requests_jitter = 4

access_log_format = '%(h)s %(l)s %({Forwarded}i)s %(l)s %(r)s %(s)s %(b)s %(f)s %(a)s'
