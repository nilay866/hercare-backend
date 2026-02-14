#!/bin/bash
set -e

# Start Gunicorn with Uvicorn workers
exec gunicorn -c gunicorn_conf.py main:app
