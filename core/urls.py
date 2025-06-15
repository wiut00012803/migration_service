from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

rest_auth_patterns = (
    [
        path(
            "login/",
            auth_views.LoginView.as_view(
                template_name="rest_framework/login.html"
            ),
            name="login",
        ),
        path(
            "logout/",
            auth_views.LogoutView.as_view(
                next_page="/api-auth/login/"
            ),
            name="logout",
        ),
    ],
    "rest_framework",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("migrations_app.urls")),
    path("api-auth/", include(rest_auth_patterns, namespace="rest_framework")),
]
