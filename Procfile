web: gunicorn taskmaker.wsgi
worker: celery -A taskmaker worker --loglevel=info