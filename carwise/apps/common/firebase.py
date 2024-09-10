import os
import json
import logging
from django.conf import settings
from pyfcm import FCMNotification

# Set up logging
logger = logging.getLogger("my_app")

# Path to your service account key
service_account_path = os.path.join(settings.STATIC_ROOT, "serviceAccountKey.json")

# Load the service account details from the file
with open(service_account_path) as f:
    config = json.load(f)

# Initialize the FCMNotification object using both the FCM server key and project_id
push_service = FCMNotification(config["private_key"], config["project_id"])


def send_fcm_message(user, notification_body, data_payload=None):
    # Get the user's FCM token
    fcm_token = user.fcm_tokens.first()

    if fcm_token:
        try:
            # Send a notification with optional data payload
            result = push_service.notify(
                fcm_token=fcm_token.token,
                notification_body=notification_body,
                data_payload=data_payload,
            )

            logger.info(f"FCM message sent: {result}")

            # Check if the notification was successfully sent
            if result["success"] == 1:
                logger.debug("Notification sent successfully.")
                return True
            else:
                logger.warning("Failed to send notification.")
                return False
        except Exception as e:
            logger.error(f"Error sending FCM message: {e}")
            return False
    else:
        logger.warning("No FCM token found for the user.")
        return False
