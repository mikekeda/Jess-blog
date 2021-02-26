"""
Gunicorn config.
"""
bind = "unix:/uwsgi/jess_blog.sock"
workers = 1
timeout = 30
max_requests = 100
daemon = False
umask = "91"
user = "nginx"
loglevel = "info"
