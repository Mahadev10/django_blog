from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    profile_photo = models.ImageField(
        upload_to="users/", blank=True, null=True,default="users/default_user.png")
    email = models.EmailField(unique=True, max_length=200)