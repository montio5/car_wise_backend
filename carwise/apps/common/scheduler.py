from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
import logging
from django.contrib.auth.models import User
from apps.common.notification import send_push_notification
from apps.reminder.views.general_views import get_notification_for_user

scheduler = BackgroundScheduler()


def send_notifications():
    logging.info("Executing send_notifications function...")
    users = User.objects.all()
    print("---------------------here")
    for user in users:
        send_push_notification(
            user,
            "daily check",
            get_notification_for_user(user),
        )
        print("---------------------",get_notification_for_user(user))
    logging.info("send_notifications function executed successfully!")


def start_scheduler():
    scheduler.add_jobstore(DjangoJobStore(), "default")
    register_events(scheduler)
    # scheduler.add_job(send_notifications, "interval", days=14)
    scheduler.add_job(send_notifications, "interval", minutes=2)
    scheduler.start()
