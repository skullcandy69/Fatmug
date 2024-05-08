from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.shortcuts import redirect       
from django.urls import reverse


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "/vendor/login/" or request.path.startswith(reverse('admin:index')):
            response = self.get_response(request)
            return response
        elif "Authorization" in request.headers:
            try:
                token_key = request.headers["Authorization"].split()[1]
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except (Token.DoesNotExist, IndexError):
                return JsonResponse(
                    {"error": "Invalid authentication token"}, status=401
                )
        else:
            return JsonResponse({"error": "Authentication Token required"}, status=401)

        response = self.get_response(request)
        return response
