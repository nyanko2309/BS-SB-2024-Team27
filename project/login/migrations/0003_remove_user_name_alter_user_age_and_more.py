# Generated by Django 5.0.3 on 2024-03-07 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_user_name_remove_user_favorites_alter_user_my_posts_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='user',
            name='favorites',
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='my_posts',
            field=models.ManyToManyField(related_name='authored_by', to='login.user'),
        ),
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(related_name='favorited_by', to='login.user'),
        ),
    ]