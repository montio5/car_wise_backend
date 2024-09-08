import os
import json

from django.conf import settings
from pyfcm import FCMNotification

service_account_path = os.path.join(settings.STATIC_ROOT, "serviceAccountKey.json")


with open(service_account_path) as f:
    config = json.load(f)

push_service = FCMNotification(config["private_key"], config["project_id"])

def send_fcm_message(user, message_title, message_body, data_message=None):
    fcm_token = user.fcm_tokens.first()
    if fcm_token:
        result = push_service.notify_single_device(
            registration_id=fcm_token.token,
            message_title=message_title,
            message_body=message_body,
            data_message=data_message,
        )
        if result['success'] == 1:
            return True
        else:
            return False
    else:
        return False
