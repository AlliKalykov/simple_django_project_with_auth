from rest_framework import serializers
from accounts.models import User
from phonenumber_field.serializerfields import PhoneNumberField
from typing import Union

UserSerializers = Union["UserCreateSerialiser", "UserUpdateSerialiser", "UserResponseSerializer"]

error_messages = {"blank": "field can not be blank", "required": "field required", "invalid": "invalid"}


class BaseUserSerializer(serializers.ModelSerializer):
    error_messages = {"blank": "field can not be blank", "required": "field required", "invalid": "invalid"}

    class Meta:
        model = User


class UserResponseSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        read_only_fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )


class UserCreateSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "middle_name",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(BaseUserSerializer):
    email = serializers.CharField(allow_blank=False, error_messages=error_messages)

    class Meta(BaseUserSerializer.Meta):
        fields = ("email", "password")


class UserUpdateSerializer(BaseUserSerializer):

    class Meta(UserResponseSerializer.Meta):
        fields = (
            "first_name",
            "last_name",
            "middle_name",
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AccountSerializer(serializers.ModelSerializer):
    error_messages = {"blank": "field can not be blank", "required": "field required", "invalid": "invalid"}

    first_name = serializers.CharField(
        allow_blank=False, min_length=2, error_messages={"min_length": "length must be 2 or more symbols", **error_messages}
    )
    last_name = serializers.CharField(
        allow_blank=False, min_length=2, error_messages={"min_length": "length must be 2 or more symbols", **error_messages}
    )
    middle_name = serializers.CharField(
        allow_blank=False, min_length=2, error_messages={"min_length": "length must be 2 or more symbols", **error_messages}
    )
    phone = PhoneNumberField(allow_blank=False, error_messages=error_messages)
    email = serializers.EmailField(allow_blank=False, error_messages=error_messages)
    new_email = serializers.EmailField(allow_blank=False, error_messages=error_messages)
    username = serializers.CharField(
        allow_blank=False, min_length=2, error_messages={"min_length": "length must be 2 or more symbols", **error_messages}
    )
    password = serializers.CharField(
        allow_blank=False, min_length=8, error_messages={"min_length": "length must be 8 or more symbols", **error_messages}
    )
    new_password = serializers.CharField(
        allow_blank=False, min_length=8, error_messages={"min_length": "length must be 8 or more symbols", **error_messages}
    )
    code = serializers.CharField(
        allow_blank=False,
        min_length=4,
        max_length=4,
        error_messages={"min_length": "length must be 4 symbols", "max_length": "length must be 4 symbols",
                        **error_messages},
    )
    refresh = serializers.CharField(min_length=128, required=True, error_messages=error_messages)

    class Meta:
        abstract = True


class LogoutSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("refresh",)


class ChangePasswordSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("password", "new_password")

    def validate(self, attrs):
        if attrs["password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": "passwords must be different"})
        return attrs


class ResetPasswordSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("email",)


class ChangeEmailSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("new_email",)


class ChangeEmailConfirmSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("new_email", "code",)


class ChangePhoneSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("phone",)


class ChangePhoneConfirmSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("phone", "code",)


class ChangeUsernameSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("username",)


class ChangeUsernameConfirmSerializer(AccountSerializer):
    class Meta:
        model = User
        fields = ("username", "code",)
