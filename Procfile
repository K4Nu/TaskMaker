web: gunicorn taskmaker.wsgi
worker: celery -A taskmaker worker --without-heartbeat --without-gossip --without-mingle --loglevel=info