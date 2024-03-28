#accesslog = 'log'
#errorlog = 'err'
# turn off timeout to prevent unwanted termination.
timeout = 0
# force the worker to restart on client disconnect to prevent
# ffmpeg running forever otherwise
max_requests = 1
workers = 4
