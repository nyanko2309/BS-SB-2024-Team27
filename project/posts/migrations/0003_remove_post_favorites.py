# Generated by Django 5.0.3 on 2024-03-21 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='favorites',
        ),
    ]