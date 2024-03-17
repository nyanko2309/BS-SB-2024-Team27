from django.db import models


# Create your views here.
class Post(models.Model):
    description = models.TextField()
    location = models.TextField()
    payment = models.TextField()
    work_hours = models.TextField()
    phys_lvl = models.IntegerField()
    kind_of_job = models.TextField()
    category = models.TextField()


