from django.db import models

class Post(models.Model):
    description = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    payment = models.TextField(null=True, blank=True)
    work_hours = models.TextField(null=True, blank=True)
    phys_lvl = models.IntegerField(null=True, blank=True)
    kind_of_job = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)

