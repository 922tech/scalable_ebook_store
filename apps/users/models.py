from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    updated_at = models.DateTimeField(auto_now_add=True)


class Profile(User):
    wallet_charge = models.PositiveBigIntegerField()

