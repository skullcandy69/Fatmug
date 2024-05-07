from django.db.models import Avg, Count, F
import logging

from vendor.models import PurchaseOrder, VendorPerformance
from vendor.utils.constants import PurchaseOrderStatus
from django.db.models.signals import post_save
from django.dispatch import receiver
from vendor.models import PurchaseOrder

logger = logging.getLogger(__name__)


class VendorPerformanceService:

    @staticmethod
    def calculate_on_time_delivery_rate(vendor):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status__in=PurchaseOrderStatus.success_status_list
        )
        on_time_orders = completed_orders.filter(
            status=PurchaseOrderStatus.completed_on_time
        )
        total_completed_orders = completed_orders.count()
        if total_completed_orders > 0:
            return round(on_time_orders.count() / total_completed_orders, 3)
        else:
            return 0.0

    @staticmethod
    def calculate_quality_rating_avg(vendor):
        completed_orders_with_rating = PurchaseOrder.objects.filter(
            vendor=vendor,
            status__in=PurchaseOrderStatus.success_status_list,
            quality_rating__isnull=False,
        )
        return (
            round(
                completed_orders_with_rating.aggregate(
                    average_rating=Avg("quality_rating")
                )["average_rating"],
                3,
            )
            or 0.0
        )

    @staticmethod
    def calculate_average_response_time(vendor):
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        )
        if acknowledged_orders.exists():
            total_response_time = acknowledged_orders.annotate(
                response_time=F("acknowledgment_date") - F("issue_date")
            ).aggregate(total_response_time=Avg("response_time"))["total_response_time"]
            return round(
                total_response_time.total_seconds() / acknowledged_orders.count(), 3
            )
        else:
            return 0.0

    @staticmethod
    def calculate_fulfillment_rate(vendor):
        total_orders = PurchaseOrder.objects.filter(vendor=vendor)
        completed_orders = total_orders.filter(
            status__in=PurchaseOrderStatus.success_status_list
        )
        successful_orders = completed_orders.exclude(
            quality_rating__lt=3
        )  # Assuming quality_rating < 3 indicates issues
        successful_orders = successful_orders.exclude(
            status=PurchaseOrderStatus.completed
        )
        if total_orders.count() > 0:
            return round(successful_orders.count() / total_orders.count(), 3)
        else:
            return 0.0

    @classmethod
    def update_performance_metrics(cls, vendor_obj):
        try:
            on_time_delivery_rate = cls.calculate_on_time_delivery_rate(vendor_obj)
            quality_rating_avg = cls.calculate_quality_rating_avg(vendor_obj)
            average_response_time = cls.calculate_average_response_time(vendor_obj)
            fulfillment_rate = cls.calculate_fulfillment_rate(vendor_obj)

            vendor_performace, _created = VendorPerformance.objects.get_or_create(
                vendor=vendor_obj
            )

            vendor_performace.average_response_time = average_response_time
            vendor_performace.quality_rating_avg = quality_rating_avg
            vendor_performace.fulfillment_rate = fulfillment_rate
            vendor_performace.on_time_delivery_rate = on_time_delivery_rate

            vendor_performace.save()
        except Exception as e:
            logger.error(
                f"error in saving vendor performance data {str(e)} for vendor:{vendor_obj.id} "
            )

    @receiver(
        post_save,
        sender=PurchaseOrder,
        dispatch_uid="update_vendor_performance_metrics",
    )
    def update_vendor_performance_metrics(sender, instance, created, **kwargs):
        if not created:
            VendorPerformanceService.update_performance_metrics(instance.vendor)
            print(
                "Vendor performance metrics updated for completed purchase order:",
                instance,
            )
