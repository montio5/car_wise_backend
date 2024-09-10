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
try:
    with open(service_account_path) as f:
        config = json.load(f)
    logger.debug("Successfully loaded service account key.")
except Exception as e:
    logger.error(f"Error loading service account key: {e}")

# Initialize the FCMNotification object using both the FCM server key (private_key) and project_id
try:
    push_service = FCMNotification(config["private_key"], config["project_id"])
    logger.debug("Successfully initialized FCMNotification.")
except Exception as e:
    logger.error(f"Error initializing FCMNotification: {e}")


def send_fcm_message(user, message_title, message_body, data_message=None):
    # Get the user's FCM token
    fcm_token = user.fcm_tokens.first()

    if fcm_token:
        try:
            # Send a message to a single device using send_message
            result = push_service.send_message(
                registration_id=fcm_token.token,
                title=message_title,
                body=message_body,
                data=data_message,  # Optional, can be None if not needed
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
