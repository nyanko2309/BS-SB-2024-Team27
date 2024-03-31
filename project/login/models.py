from django.db import models
class User(models.Model):
    name = models.TextField(null=True)
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    favorites = models.JSONField(default=list)
    my_posts = models.JSONField(default=list)
    site_rating = models.IntegerField(default=0, choices=[(i, i) for i in range(6)])

