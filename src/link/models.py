import os
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from link.managers import ProtectedResourceManager


class ProtectedResource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    uri = models.TextField(default=None, null=True)
    views_count = models.PositiveIntegerField(default=0)
    file = models.FileField(default=None, null=True, upload_to=settings.UPLOAD_PATH)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProtectedResourceManager()

    def is_valid_password(self, raw_password):
        return check_password(raw_password, self.password)

    def is_available(self):
        return (self.created_at + timedelta(hours=settings.LINK_PROTECTED_RESOURCE_ACCESS_TIME_HOURS)) > now()

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
