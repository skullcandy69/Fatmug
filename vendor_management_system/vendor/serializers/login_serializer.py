from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user:
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Invalid username or password')
