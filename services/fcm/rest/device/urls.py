from django.urls import path
from .views import RegisterFCMDeviceView

urlpatterns = [
    path("register-fcm/", RegisterFCMDeviceView.as_view(), name="register-fcm"),
]
