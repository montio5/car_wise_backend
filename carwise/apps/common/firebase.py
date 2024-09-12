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
    token=user.fcm_tokens.first()
    data = {
        "to": token,
        "title": title,
        "body": message,
    }

    response = requests.post(expo_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_id = data.get("user_id")
            title = data.get("title", "No Title")
            message = data.get("message", "No Message")

            # Fetch the user and their token
            user = User.objects.get(id=user_id)
            push_token = UserFCMToken.objects.get(user=user).token

            # Send the notification using Expo's Push API
            response = send_push_notification(push_token, title, message)

            if response:
                return JsonResponse(
                    {"status": "Notification sent successfully", "response": response}
                )
            else:
                return JsonResponse(
                    {"error": "Failed to send notification"}, status=500
                )

        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except UserFCMToken.DoesNotExist:
            return JsonResponse({"error": "Push token not found for user"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
