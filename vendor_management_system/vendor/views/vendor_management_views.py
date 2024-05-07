import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from vendor.utils.custom_response_helper import custom_response

logger = logging.getLogger(__name__)


class VendorViews(APIView):

    def get(self, request):
        try:
            vendor_qs = Vendor.objects.all()
            if not vendor_qs:
                return Response(
                    data=custom_response([], "no vendors found", True),
                    status=status.HTTP_204_NO_CONTENT,
                )

            serialized_data = VendorSerializer(vendor_qs, many=True)
            return Response(
                data=custom_response(serialized_data.data, "", True),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in vendor list {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, requst):
        try:
            data = requst.data
            logger.info(f"data for creating vendor: {data}")
            vendor_serializer = VendorSerializer(data=data)
            if vendor_serializer.is_valid():
                vendor_serializer.save()
                logger.info(f"vendor data saved successfully")
                return Response(
                    custom_response(
                        data=vendor_serializer.data,
                        message="vendor data saved successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    custom_response(
                        data=None, message=vendor_serializer.errors, success=False
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in creating vendor {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VendorManagement(APIView):

    def get(self, request, vendor_id):
        try:
            vendor_qs = Vendor.objects.get(id=vendor_id)
            serialized_data = VendorSerializer(vendor_qs)
            return Response(
                data=custom_response(serialized_data.data, "", True),
                status=status.HTTP_200_OK,
            )
        except Vendor.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error in vendor list {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, requst, vendor_id):
        try:
            data = requst.data
            logger.info(f"data for updating vendor_id:{vendor_id} {data}")
            vendor = Vendor.objects.get(id=vendor_id)
            vendor_serializer = VendorSerializer(vendor, data=data, partial=True)
            if vendor_serializer.is_valid():
                vendor_serializer.save()
                return Response(
                    custom_response(
                        data=vendor_serializer.data,
                        message="vendor data updated successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    custom_response(
                        data=None, message=vendor_serializer.errors, success=False
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Vendor.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data=custom_response([], f"error updaing vendor:{vendor_id} {str(e)}", False),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    def delete(self,request,vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.delete()
            logger.info(f"vendor with id:{vendor_id} deleted successfully")
            return Response(
                    custom_response(
                        data=None,
                        message=f"vendor with id:{vendor_id} deleted successfully",
                        success=True,
                    ),
                    status=status.HTTP_200_OK,
                )
        except Vendor.DoesNotExist as ve:
            return Response(
                data=custom_response([], str(ve), False),
                status=status.HTTP_400_BAD_REQUEST,
            )