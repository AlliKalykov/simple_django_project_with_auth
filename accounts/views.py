from rest_framework import generics, status, viewsets, permissions, exceptions
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    UserCreateSerializer,
    UserResponseSerializer,
    UserUpdateSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ChangeEmailSerializer,
    ChangeEmailConfirmSerializer,
)


def get_user_with_token(user, request):
    refresh = RefreshToken.for_user(user)
    data = {
        "user": UserResponseSerializer(instance=user, context={"request": request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return data


class UserViewSet(viewsets.ModelViewSet):
    throttle_scopes = ["user"]
    queryset = User.objects.all()
    serializer_class = UserResponseSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "partial_update":
            return UserUpdateSerializer
        return UserResponseSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = get_user_with_token(user, request)
        return Response(data=data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = get_user_with_token(user, request)
        return Response(data=data, status=status.HTTP_200_OK)

    def get_object(self):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={"success": "User deleted"})

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        data = get_user_with_token(user, request)
        return Response(data)


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if not user:
            return exceptions.AuthenticationFailed()
        user.last_login = timezone.now()
        user.save()
        data = get_user_with_token(user, request)
        return Response(data=data, status=status.HTTP_200_OK)


class LogoutView(generics.CreateAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = RefreshToken(serializer.validated_data["refresh"])
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT, data={"success": "Logout successful"})


class ChangePasswordAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user
        data = serializer.validated_data
        if not user.check_password(data["old_password"]):
            raise exceptions.ValidationError({"error": "Old password is not correct"})
        user.set_password(data["new_password"])
        user.save()
        return Response(status=status.HTTP_200_OK, data={"success": "Password changed successfully"})


class ResetPasswordAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        pass


class ChangeEmailAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeEmailSerializer

    def post(self, request, *args, **kwargs):
        pass


class ChangeEmailConfirmAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangeEmailConfirmSerializer

    def post(self, request, *args, **kwargs):
        pass
