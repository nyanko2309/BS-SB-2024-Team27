# Generated by Django 5.0.2 on 2024-03-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_user_name'),
        ('posts', '0006_remove_post_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='my_posts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='favorites',
        ),
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='posts.post'),
        ),
    ]
