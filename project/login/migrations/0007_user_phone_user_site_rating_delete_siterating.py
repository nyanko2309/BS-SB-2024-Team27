# Generated by Django 5.0.3 on 2024-03-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_remove_user_site_rating_siterating'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='site_rating',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=0),
        ),
        migrations.DeleteModel(
            name='SiteRating',
        ),
    ]
