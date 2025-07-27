from __future__ import annotations
from django.contrib.gis.db import models as geomodels
from typing import TYPE_CHECKING
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import get_subid_model

if TYPE_CHECKING:
    from authn.models.user import User

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
    nik = models.CharField(max_length=32, unique=True, null=True, blank=True)
    location = geomodels.PointField(geography=True, null=True, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='driver', null=True, blank=True)
    ktp = models.ImageField(upload_to='document', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    objects = DriverManager()
    
    def __str__(self):
        return f"Driver: ({self.user.username}) {self.user.first_name} {self.user.last_name}"