from celery import shared_task
from django.contrib.auth.models import User

from apps.common.firebase import send_push_notification
from apps.reminder.views.general_views import get_notification_for_user


@shared_task
def send_notifications():
    users = User.objects.all()
    for user in users:
        send_push_notification(
            user,
            "weekly check",
            get_notification_for_user(user),
        )
