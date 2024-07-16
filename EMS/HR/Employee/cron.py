from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
from .models import Employee

class ResetLateMinutesCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']  # Run at midnight

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'Employee.reset_late_minutes_cron_job'

    def do(self):
        employees = Employee.objects.all()
        for employee in employees:
            employee.late_min_ava = 90
            employee.late_time_ava = timedelta(minutes=90)
            employee.save()

        print('Successfully reset late minutes and duration for employees')

@receiver(post_migrate)
def schedule_cron_job(sender, **kwargs):
    from django_cron import CronJobManager

    # Check if it's the beginning of a new month
    today = datetime.today()
    if today.day == 1:
        # Schedule the cron job to run ResetLateMinutesCronJob
        ResetLateMinutesCronJob().schedule()