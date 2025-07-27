from __future__ import annotations
from typing import TYPE_CHECKING

import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from authn.rest.auth.serializers import UserSerializer
from driver.models.driver import Driver


if TYPE_CHECKING:
    from authn.models.user import User
    from driver.models.driver import Driver


logger = logging.getLogger(__name__)
__all__ = (
    "DriverSerializer",
)

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Driver
        fields = (
            "subid",  # Include 'id' for primary key identification
            "user",
            "nik",
            "location",
            "last_active",
            "photo",
            "ktp",
            "is_available",
            "is_verified",
            "registered_at",
        )
        read_only_fields = (
            "subid",
            "user", # Assuming user is set automatically or via a different view logic
            "last_active",
            "registered_at",
            "is_verified", # Assuming verification is an admin action, not user editable
        )