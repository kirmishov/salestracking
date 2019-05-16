from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # name = models.TextField(max_length=40)
    pass