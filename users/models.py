from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from model_utils import Choices

# Create your models here.
USER_ROLES = Choices(
    'admin',
    'user',
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("User must have a valid email address.")
        user = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get("first_name", None),
            middle_name=kwargs.get("middle_name", None),
            last_name=kwargs.get("middle_name", None),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.role = 'admin'
        user.is_active = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
    )
    first_name = models.CharField(max_length=25, blank=True, null=True)
    middle_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=254, choices=USER_ROLES, default=USER_ROLES.admin)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    object = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = self.first_name
        if self.middle_name:
            full_name = full_name + '' + self.middle_name
            if self.last_name:
                full_name = full_name + '' + self.last_name
                return full_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role == USER_ROLES.admin

    def is_user(self):
        return self.role == USER_ROLES.user

    class Meta:
        db_table = "users_user"
