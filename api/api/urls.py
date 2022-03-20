from django.contrib import admin
from django.urls import include, path

from . import jwt


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/",
        jwt.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        jwt.CookieTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/clear/",
        jwt.CookieTokenClearView.as_view(),
        name="token_refresh",
    ),
    path("api/", include("example.urls")),
]
