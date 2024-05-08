from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from vendor.models import Vendor


class VendorSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]


class VendorSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "contact_number",
            "vendor_code",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]

    def validate(self, attrs):
        if 'vendor_code' in attrs:
            raise ValidationError("You cannot update the vendor_code field.")
        if 'username' in attrs:
            raise ValidationError("You cannot update the username field.")
        return attrs
