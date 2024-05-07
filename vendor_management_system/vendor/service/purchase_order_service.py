from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from vendor.models import PurchaseOrder
from vendor.serializers import PurchaseOrderSerializer
from vendor.utils.constants import PurchaseOrderStatus
from vendor.service.vendor_performance_service import VendorPerformanceService

class PurchaseOrderService:

    @staticmethod
    def update_purchase_order(po, data={}):
        try:
            order_status = data.pop("status", None)
            if order_status in PurchaseOrderStatus.success_status_list:
                if timezone.now() <= po.delivery_date:
                    po.status = PurchaseOrderStatus.completed_on_time
                else:
                    po.status = PurchaseOrderStatus.completed

            serializer = PurchaseOrderSerializer(po, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return serializer.data, "purchase order updated successfully", True
            else:
                return {}, serializer.errors, False
        except Exception as e:
            return {}, str(e), False
        