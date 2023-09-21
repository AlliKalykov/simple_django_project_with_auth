import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):

    # create_user and create_superuser is mandatory

    def create_user(
            self,
            username: str,
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            middle_name: str = None,
            phone: str = None,
            is_active: bool = True,
            is_staff: bool = False,
            is_superuser: bool = False,
            password=None
    ):
        if not username:
            raise ValueError("Username required!")
        email = self.normalize_email(email)

        user:  User = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            phone=phone,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    _uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(
        verbose_name="Почта", max_length=100, unique=True,
    )
    username = models.CharField(max_length=60, unique=True)
    phone = PhoneNumberField("Телефон", unique=True, null=True, blank=True)
    first_name = models.CharField("Фамилия", max_length=100, blank=True, null=True)
    last_name = models.CharField("Имя", max_length=100, blank=True, null=True)
    middle_name = models.CharField("Отчество", max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="Последнее соединение", auto_now=True
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"  # values will be identified using email now
    # shouldn't add 'username' here, since it is already in USERNAME_FIELD
    REQUIRED_FIELDS = []

    objects = UserManager()

    # these 3 are required methods
    def __str__(
        self,
    ):  # This gets displayed when an object of Account class is called in template
        return self.username  # multiple values can be concatenated like this

    def has_perm(self, perm, obj=None):  # has permission to make changes
        return self.is_staff  # only allowed if admin

    def has_module_perms(self, app_label):  # give permission to module
        return True  # instead of True we can give access to specific position (eg: is_admin, is_staff or both)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
