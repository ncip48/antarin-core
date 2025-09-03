from firebase_admin import messaging
from fcm.models.fcm_device import FCMDevice

def send_fcm_notification(token, title, body, data=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {},  # optional custom payload
    )

    response = messaging.send(message)
    return response

def notify_user(user, title, body):
    devices = FCMDevice.objects.filter(user=user)
    for device in devices:
        try:
            send_fcm_notification(device.token, title, body)
        except Exception as e:
            print("FCM Error:", e)