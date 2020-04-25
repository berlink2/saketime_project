from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Must input a valid email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True: raise ValueError(
            "Superuser must have is_staff=True."
        )
        if extra_fields.get("is_superuser") is not True: raise ValueError(
            "Superuser must have is_superuser=True."
        )
        return self._create_user(email,password, **extra_fields)


class User(AbstractUser):

    username = models.CharField(max_length=50, null=True, blank=True, default='saketime_user')
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_employee(self):
        return self.is_active and (
                self.is_superuser
                or self.is_staff
                and self.groups.filter(name="Employees").exists()
        )

    @property
    def is_dispatcher(self):
        return self.is_active and (
                self.is_superuser
                or self.is_staff
                and self.groups.filter(name="Dispatchers").exists()
        )



