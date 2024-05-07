from vendor.models.abstract_date_time import AbstractDateTime
from django.db import models

class VendorPerformance(AbstractDateTime):
    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quality_rating_avg = models.FloatField(null=True)
    on_time_delivery_rate = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

    def __str__(self):
        return f"vendor_id:{self.vendor.id} id{self.id}"
