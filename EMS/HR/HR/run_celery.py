from celery import app

# Run the Celery worker
app.worker_main(['worker', '--loglevel=info'])