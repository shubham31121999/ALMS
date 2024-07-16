from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from celery import shared_task
from celery.schedules import crontab # Make sure to import your app correctly

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HR.settings')

app = Celery('HR')

app.conf.enable_utc = False
app.conf.update(
    broker_url='amqp://guest@127.0.0.1:5672//',
    result_backend='rpc://',
    broker_connection_retry_on_startup=True,
    timezone='Asia/Kolkata',
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'generate-salary-everyday-11-50am': {
        'task': 'Employee.tasks.generate_salary',
        'schedule': crontab(minute='*/1'),
    },
    
    # 'update-employee-availability-everyday-11pm': {
    #     'task': 'Employee.tasks.update_employee_availability',  # Adjust the path if necessary
    #     'schedule': crontab(minute='*/5'),
    # },

    'deduct-leave-daily-5am': {
        'task': 'your_app.tasks.deduct_leave_for_employee',
        'schedule': crontab(minute=0, hour=5),  # Run deduct_leave_for_employee task every day at 5:00 AM
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

if __name__ == '__main__':
    app.start()