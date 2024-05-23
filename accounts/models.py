import uuid
import os
import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


def rename_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    return os.path.join('images/', filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=100, blank=True, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Uploads(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    file = models.ImageField(upload_to=rename_file_upload, blank=False)
    timestamp = models.DateTimeField(
        auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.file.name


class NewsRecord(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    file_path = models.TextField(blank=False)
    external_file_path = models.TextField(blank=True)
    extracted_text = models.TextField(blank=False)
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.file_path
