# import firebase_admin
# from firebase_admin import credentials, messaging

# # Path to your service account key file
# service_account_path = "serviceAccountKey.json"

# # Initialize the Firebase Admin SDK with the service account
# cred = credentials.Certificate(service_account_path)
# firebase_admin.initialize_app(cred)


# def send_fcm_notification(token, title, body):
#     """
#     Sends a push notification to a single device using Firebase Cloud Messaging.

#     :param token: The FCM token of the device to send the notification to.
#     :param title: The title of the notification.
#     :param body: The body text of the notification.
#     """
#     message = messaging.Message(
#         notification=messaging.Notification(
#             title=title,
#             body=body,
#         ),
#         token=token,
#     )

#     # Send the message
#     response = messaging.send(message)
#     print("Successfully sent message:", response)
