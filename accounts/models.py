import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    credit_card = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
