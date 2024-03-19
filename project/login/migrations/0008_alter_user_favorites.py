# Generated by Django 5.0.2 on 2024-03-16 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_remove_user_my_posts_remove_user_favorites_and_more'),
        ('posts', '0008_remove_post_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='posts.post'),
        ),
    ]
