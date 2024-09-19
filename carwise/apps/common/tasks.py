import os
import django
import logging
from django.contrib.auth.models import User
from apps.common.notification import send_push_notification
from apps.reminder.views.general_views import get_notification_for_user

# Set the environment variable to point to your Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carwise.carwise.settings")

# Setup Django (required to access models and other Django features)
django.setup()

# Logging configuration (optional)
logging.basicConfig(level=logging.INFO)


def send_notifications():
    logging.info("Executing send_notifications function...")
    users = User.objects.all()

    for user in users:
        try:
            # Send push notification to each user
            message = get_notification_for_user(user)
            send_push_notification(user, "daily check", message)
            logging.info(f"Notification sent to {user.username}: {message}")
        except Exception as e:
            logging.error(f"Error sending notification to {user.username}: {e}")

    logging.info("send_notifications function executed successfully!")


if __name__ == "__main__":
    send_notifications()
