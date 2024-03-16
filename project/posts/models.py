from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    description = models.TextField()
    location = models.TextField()
    payment = models.TextField()
    work_hours = models.TextField()
    phys_lvl = models.IntegerField()
    kind_of_job = models.TextField()
    category = models.TextField()
    favorites = models.ManyToManyField(User, related_name='favorite_posts')
