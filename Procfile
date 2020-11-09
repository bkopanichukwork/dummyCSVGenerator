web: gunicorn dummyCSVGenerator.wsgi
worker: celery -A generator worker -B --loglevel=info