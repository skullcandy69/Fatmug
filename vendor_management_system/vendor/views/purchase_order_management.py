import logging
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vendor.models import PurchaseOrder
from vendor.serializers import PurchaseOrderSerializer
from vendor.service import PurchaseOrderService
from vendor.utils.custom_response_helper import custom_response

logger = logging.getLogger(__name__)


class PurchaseOrders(APIView):
    def get(self, request):
        try:
            purchase_order_qs = PurchaseOrder.objects.all()
            if not purchase_order_qs:
                return Response(
                    data=custom_response([], "no purchase orders found", True),
                    status=status.HTTP_204_NO_CONTENT,
                )

            serialized_data = PurchaseOrderSerializer(purchase_order_qs, many=True)
            return Response(
                data=custom_response(serialized_data.data, "", True),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in fetching purchase orders list {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, requst):
        try:
            data = requst.data
            logger.info(f"data for creating purchase orders: {data}")
            purchase_order_serializer = PurchaseOrderSerializer(data=data)
            if purchase_order_serializer.is_valid():
                purchase_order_serializer.save()
                logger.info(f"purchase order created successfully")
                return Response(
                    custom_response(
                        data=purchase_order_serializer.data,
                        message="purchase order created successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    custom_response(
                        data=None, message=purchase_order_serializer.errors, success=False
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in creating purchase order {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class PurchaseOrderTracking(APIView):
    def get(self, request, po_id):
        try:
            vendor_qs = PurchaseOrder.objects.get(id=po_id)
            serialized_data = PurchaseOrderSerializer(vendor_qs)
            return Response(
                data=custom_response(serialized_data.data, "", True),
                status=status.HTTP_200_OK,
            )
        except PurchaseOrder.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in vendor list {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, requst, po_id):
        try:
            data = requst.data
            logger.info(f"data for updating purchase order id {po_id} {data}")
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            po_data,_message,_st = PurchaseOrderService().update_purchase_order(purchase_order,data)
            
            if _st:
                return Response(
                    custom_response(
                        data=po_data,
                        message=_message,
                        success=_st,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    custom_response(
                        data=po_data, message=_message, success=_st
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except PurchaseOrder.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self,request,po_id):
        try:
            vendor = PurchaseOrder.objects.get(id=po_id)
            vendor.delete()
            logger.info(f"purchase order with id:{po_id} deleted successfully")
            return Response(
                    custom_response(
                        data=None,
                        message=f"purchase order with id:{po_id} deleted successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
        except PurchaseOrder.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class UpdateAcknowlegement(APIView):
    def patch(self,request,po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return Response(
                    custom_response(
                        data=None,
                        message="purchase order updated successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
        except PurchaseOrder.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in updating acknowledgment_date for purchase order:{po_id} {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        
