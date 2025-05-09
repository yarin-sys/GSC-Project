from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(null=True, blank=True,unique=True, max_length=20)
    address = models.TextField()