from django.db import models
from django.contrib.auth import get_user_model
from core.models import get_subid_model

User = get_user_model()

class  Notification(get_subid_model()):
    title = models.CharField(max_length=255)
    body = models.TextField()
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    force_popup = models.BooleanField(default=False)
