#!/usr/bin/env bash

cd /usr/src/app/
sleep 2  # Waiting for DB to apply migrations
python manage.py migrate

# Run web app under gunicorn
gunicorn -b 0.0.0.0:8000 --pythonpath "/usr/src/app" --workers=2 --threads=2 --worker-class=gthread --log-file=- webapp.webapp.wsgi