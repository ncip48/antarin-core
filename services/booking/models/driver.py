from django.contrib.gis.db import models as geomodels
from django.db import models

class Driver(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    location = geomodels.PointField(geography=True, null=True, blank=True)
    last_active = models.DateTimeField(auto_now=True)
    