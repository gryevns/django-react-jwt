from django.conf import settings
from django.middleware import csrf
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt import exceptions, serializers, views


AUTH_COOKIE_NAME = settings.SIMPLE_JWT["AUTH_COOKIE_NAME"]


def get_refresh_token_cookie(value):
    return {
        "key": settings.SIMPLE_JWT["AUTH_COOKIE_NAME"],
        "value": value,
        "httponly": True,
        "max_age": settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
        "secure": settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        "samesite": settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    }


class TokenObtainPairView(views.TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        csrf.get_token(self.request)
        if response.data.get("refresh"):
            refresh_token_cookie = get_refresh_token_cookie(response.data["refresh"])
            response.set_cookie(**refresh_token_cookie)
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshSerializer(serializers.TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get(AUTH_COOKIE_NAME)
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise exceptions.InvalidToken(f"Invalid {AUTH_COOKIE_NAME} in cookie")


class CookieTokenRefreshView(views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            refresh_token_cookie = get_refresh_token_cookie(response.data["refresh"])
            response.set_cookie(**refresh_token_cookie)
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenClearView(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie(key=AUTH_COOKIE_NAME)
        return response
