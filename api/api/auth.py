from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework_simplejwt.authentication import JWTAuthentication


def enforce_csrf(request):
    check = CSRFCheck(lambda _: None)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = None
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)
        if not user or not user.is_active:
            return None

        enforce_csrf(request)

        return user, validated_token
