from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from posts.models import Post

#every change run python manage.py makemigrations
#pythone manage.py migratem

class User(models.Model):
   name=models.TextField()
   mail = models.EmailField()
   password = models.CharField(max_length=100)
 # pic = models.ImageField(upload_to='profile_pics/')
   age = models.IntegerField()
   description = models.TextField()
   favorites = models.JSONField(default=list)
   my_posts = models.JSONField(default=list)

