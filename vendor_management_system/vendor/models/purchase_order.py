from django.db import models

class PurchaseOrder(models.Model):
    STATUS_CHOICES =  (
        ("pending", "pending"),
        ("completed_on_time", "completed_on_time"),
        ("completed", "completed"),
        ("canceled", "canceled"),
    )

    vendor = models.ForeignKey("vendor.Vendor", on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.po_number} status:{self.status}"
