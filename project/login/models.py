from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# every change run python manage.py makemigrations
# pythone manage.py migrate
class User(models.Model):
    name = models.TextField(null=True)
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    favorites = models.JSONField(default=list)
    my_posts = models.JSONField(default=list)
    phone = models.TextField(null=True, blank=True)
    site_rating = models.IntegerField(default=0, choices=[(i, i) for i in range(6)])

