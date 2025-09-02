from __future__ import annotations
from django.contrib.gis.db import models as geomodels
from typing import TYPE_CHECKING
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import get_subid_model
from authn.models import User

if TYPE_CHECKING:
    from authn.models import User

logger = logging.getLogger(__name__)

__all__ = (
    "DriverQuerySet",
    "DriverManager",
    "Driver",
)

class DriverQuerySet(models.QuerySet):
    def owned(self, user: User) -> DriverQuerySet:
        """
        Returns drivers owned by the given user.
        """
        return self.filter(user=user)

_DriverManagerBase = models.Manager.from_queryset(DriverQuerySet)

class DriverManager(_DriverManagerBase):
    pass

class Driver(get_subid_model()):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = geomodels.PointField(geography=True, null=True, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = DriverManager()
    
    def __str__(self):
        return f"Driver: ({self.user.username}) {self.user.first_name} {self.user.last_name}"