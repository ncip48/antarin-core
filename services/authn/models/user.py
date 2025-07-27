from __future__ import annotations
from typing import TYPE_CHECKING
from django.utils.translation import gettext_lazy as _

import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
# Assuming 'core.models' is correctly in your project structure
from core.models import get_subid_model


if TYPE_CHECKING:
    # If get_subid_model() adds specific methods/attributes that need type hinting,
    # you might need to import a base class or define a protocol here.
    # For now, assuming it primarily adds fields/managers.
    pass


logger = logging.getLogger(__name__)
__all__ = (
    "User",
)

class User(get_subid_model(), AbstractUser):
    """
    Custom User model inheriting from Django's AbstractUser and a custom
    sub-ID model. Uses email as the primary authentication field.
    """
    email = models.EmailField(_("email address"), unique=True)
    
    # Set email as the field used for authentication
    USERNAME_FIELD = 'email'
    
    # These fields are prompted for when creating a user via createsuperuser,
    # even if they are not part of the USERNAME_FIELD.
    REQUIRED_FIELDS = ['username'] 

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["email"] # Order users by email by default

    def __str__(self):
        """
        Returns a string representation of the user, preferring email,
        then username, then a generic identifier.
        """
        if self.email:
            return self.email
        elif self.username:
            return self.username
        return f"User ID: {self.pk}"

    # You can add custom methods or properties here if needed
    # For example:
    # @property
    # def full_name(self):
    #     return f"{self.first_name} {self.last_name}".strip()