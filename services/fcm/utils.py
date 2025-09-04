from firebase_admin import messaging
from fcm.models.fcm_device import FCMDevice

def send_fcm_notification(token, title, body, data=None, force_popup=False):
    """
    Send an FCM notification to a single device.
    """
    print("Sending to token:", token)

    custom_data = data or {}

    custom_data["force_popup"] = "true" if force_popup else "false"

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=custom_data,
    )

    response = messaging.send(message)
    return response

def notify_users(users, title, body, data=None, force_popup=False):
    """
    Send notifications to multiple users.
    """
    devices = FCMDevice.objects.filter(user__in=users)
    
    print(devices)
    print(len(devices))
    print(force_popup)

    for device in devices:
        try:
            send_fcm_notification(
                device.token,
                title,
                body,
                data=data,
                force_popup=force_popup,
            )
        except Exception as e:
            print("FCM Error:", e)