# Generated by Django 5.0.3 on 2024-03-28 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_rename_rating_user_site_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='site_rating',
        ),
        migrations.CreateModel(
            name='SiteRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
        ),
    ]
