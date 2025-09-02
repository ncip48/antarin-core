from __future__ import annotations
from typing import TYPE_CHECKING

import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

if TYPE_CHECKING:
    from django.contrib.auth.models import User # Explicitly import User for type hinting


logger = logging.getLogger(__name__)
__all__ = (
    "UserSerializer",
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        from django.contrib.auth import get_user_model
        model = get_user_model() # Use get_user_model() for custom User models
        fields = (
            "subid",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        )
        read_only_fields = (
            "subid",
            "is_staff",
            "is_active",
            "date_joined",
            "last_login",
        )
        # You might want to add extra_kwargs for password if you're handling user creation/update
        # extra_kwargs = {
        #     'password': {'write_only': True, 'required': False} # Use required=False for updates
        # }
