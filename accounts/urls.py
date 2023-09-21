from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
    TokenBlacklistView,
)

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.UserViewSet.as_view({"post": "create"}), name="signup_user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("logout/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("password/change/", views.ChangePasswordAPIView.as_view(), name="password_change"),
    path(
        "profile/", views.UserViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        kwargs={"pk": "me"},
        name="user_me",
    ),
]
