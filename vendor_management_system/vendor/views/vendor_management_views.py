from rest_framework import generics
from vendor.models import Vendor
from vendor.serializers import VendorSerializer

class VendorList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


