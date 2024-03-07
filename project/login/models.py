from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin





#every change run python manage.py makemigrations
#pythone manage.py migratem
class User(models.Model):
        name=models.TextField()
        mail = models.EmailField()#change to email field
        password = models.CharField(max_length=255)
        # pic = models.ImageField(upload_to='profile_pics/')
        age = models.IntegerField()
        description = models.TextField()
        favorites = models.ManyToManyField('self', related_name='favorited_by', symmetrical=False)
        my_posts = models.ManyToManyField('self', related_name='authored_by', symmetrical=False)
