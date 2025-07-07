from celery import shared_task
from django.db import transaction
from booking.models import Trip
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def accept_booking_task(booking_id, driver_id):
    try:
        with transaction.atomic():
            booking = Trip.objects.select_for_update().get(id=booking_id)

            if booking.status != "pending":
                _send_ws_to_driver(driver_id, {
                    "status": "failed",
                    "message": "Booking sudah diambil orang lain"
                })
                return

            booking.status = "accepted"
            booking.driver_id = driver_id
            booking.save()

            _send_ws_to_driver(driver_id, {
                "status": "success",
                "message": "Booking berhasil diambil",
                "booking_id": booking.id
            })

            _send_ws_to_user(booking.customer_id, {
                "status": "accepted",
                "driver_id": driver_id,
                "booking_id": booking.id
            })
    except Trip.DoesNotExist:
        _send_ws_to_driver(driver_id, {
            "status": "error",
            "message": "Booking tidak ditemukan"
        })


@shared_task
def update_booking_status_task(booking_id, new_status, driver_id):
    try:
        with transaction.atomic():
            booking = Trip.objects.select_for_update().get(id=booking_id)

            if booking.driver_id != driver_id:
                return

            if new_status == "on_trip" and booking.status == "accepted":
                booking.status = "on_trip"
            elif new_status == "completed" and booking.status == "on_trip":
                booking.status = "completed"
            else:
                return

            booking.save()

            _send_ws_to_user(booking.customer_id, {
                "status": booking.status,
                "booking_id": booking.id
            })
    except Trip.DoesNotExist:
        pass
    
@shared_task
def send_location_update(user_id, lat, lng):
    _send_ws_to_user(f"user_{user_id}", {
        "lat": lat,
        "lng": lng
    })


def _send_ws_to_driver(driver_id, payload):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"driver_{driver_id}", {
            "type": "driver.message",
            "message": payload
        }
    )


def _send_ws_to_user(user_id, payload):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)(
        f"user_{user_id}", {
            "type": "user.message",
            "message": payload
        }
    )