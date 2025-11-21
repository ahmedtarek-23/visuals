# gunicorn.conf.py
import multiprocessing

# Critical memory settings
workers = 1  # Only 1 worker for 512MB
worker_class = "sync"
worker_connections = 1000

# Memory management
max_requests = 500      # Restart worker after 500 requests
max_requests_jitter = 50  # Add randomness to restarts
preload_app = True      # Load app before forking (saves memory)
timeout = 120

# Reduce buffer sizes
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190