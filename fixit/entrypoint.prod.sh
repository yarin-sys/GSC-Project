#!/usr/bin/env bash

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# after worker 3 --> <your_app_name.wsgi:application>
python -m gunicorn --bind 0.0.0.0:8000 --workers 3 fixit.wsgi:application