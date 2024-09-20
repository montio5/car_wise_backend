import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.common.notification import send_push_notification
from apps.reminder.views.general_views import get_notification_for_user


class Command(BaseCommand):
    help = "Send notifications to all users"

    def handle(self, *args, **kwargs):
        logging.info("Executing send_notifications function...")
        # only users who has the notification token
        users = User.objects.filter(fcm_tokens__isnull=False).distinct()
        for user in users:
            try:
                # Send push notification to each user
                message = get_notification_for_user(user)
                send_push_notification(user, "daily check", message)
                logging.info(f"Notification sent to {user.username}: {message}")
            except Exception as e:
                logging.error(f"Error sending notification to {user.username}: {e}")

        logging.info("send_notifications function executed successfully!")
