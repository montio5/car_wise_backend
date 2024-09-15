# views.py

import json
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User

from apps.user.models import UserFCMToken


def send_push_notification(user, title, message):
    expo_url = "https://exp.host/--/api/v2/push/send"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    tokens=user.fcm_tokens.all()
    if tokens:
        fcm_token = tokens.first()
        data = {
            "to": fcm_token.token,
            "title": title,
            "body": message,
        }

        response = requests.post(expo_url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()
        return None
    return None

