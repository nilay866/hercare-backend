import os
import multiprocessing

# Gunicorn config variables
loglevel = os.getenv("LOG_LEVEL", "info")
workers = os.getenv("WORKERS", multiprocessing.cpu_count() * 2 + 1)
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
