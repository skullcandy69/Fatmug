from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class Vendor(AbstractUser):
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    vendor_code = models.UUIDField(unique=True,default=uuid4)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return self.username
