# Generated by Django 5.0.3 on 2024-03-28 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_alter_post_category_alter_post_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='phone',
            field=models.TextField(blank=True, null=True),
        ),
    ]
