from django.contrib.gis.db import models as geomodels
from django.db import models

class Trip(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("on_trip", "On Trip"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    pickup_point = geomodels.PointField(geography=True)
    destination_point = geomodels.PointField(geography=True, null=True, blank=True)
    driver = models.ForeignKey("driver.Driver", null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trip #{self.id} - {self.customer} ({self.status})"