run celery using 
# celery -A celery_worker.celery worker --loglevel=info

run gunicorn
# gunicorn -w 1 -b :5000 run:app --reload