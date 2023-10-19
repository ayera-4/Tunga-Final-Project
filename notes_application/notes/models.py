from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Notes(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False, blank=True, null=True)
    due_date = models.DateField(max_length=255, blank=True, null=True)
    note_done = models.BooleanField(default=False, blank=True, null=True)
    priority = models.CharField(max_length=255)

class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

class Auth_token(models.Model):
    active_token = models.CharField(verbose_name="Active_token", max_length=255)
