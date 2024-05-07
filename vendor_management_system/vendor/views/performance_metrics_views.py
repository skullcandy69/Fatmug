import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vendor.models import VendorPerformance
from vendor.serializers import VendorPerformanceSerializer
from vendor.utils.custom_response_helper import custom_response

logger = logging.getLogger(__name__)


class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor_performance = VendorPerformance.objects.get(vendor_id=vendor_id)
            serialized_data = VendorPerformanceSerializer(vendor_performance)
            return Response(
                data=custom_response(serialized_data.data, "", True),
                status=status.HTTP_200_OK,
            )
        except VendorPerformance.DoesNotExist as vp:
            return Response(
                data=custom_response([], str(vp), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data=custom_response(
                    [], f"error in fetching vendor performance metrics {str(e)}", False
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
