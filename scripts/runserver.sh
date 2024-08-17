#!/bin/bash
python manage.py collectstatic --no-input
python manage.py migrate --no-input
gunicorn --config config/gunicorn.conf.py teamable.wsgi:application