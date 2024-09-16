from django.contrib.auth.models import User

from apps.common.notification import send_push_notification
from apps.reminder.views.general_views import get_notification_for_user


def send_notifications():
    users = User.objects.all()
    for user in users:
        send_push_notification(
            user,
            "daily check",
            get_notification_for_user(user),
        )
