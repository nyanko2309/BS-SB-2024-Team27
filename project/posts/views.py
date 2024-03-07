from django.shortcuts import render

# Create your views here.
class Post(models.Model):
    description = models.TextField()