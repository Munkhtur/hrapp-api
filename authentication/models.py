from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created


# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, full_name, password, **other_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, full_name, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('has_module_perms', 'authentication')

        if other_fields.get('is_staff') is not True:
            raise ValueError('Super user must be assigned staff True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super user must be assigned superuser True')

        return self.create_user(email, full_name, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=20, unique=True)
    full_name = models.CharField(max_length=30)
    password = models.CharField(
        max_length=255)
    department = models.CharField(max_length=30)
    total_hours = models.FloatField(default=0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # has_module_perms('authentication')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    print(reset_password_token.user.email, "reset token")
    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
