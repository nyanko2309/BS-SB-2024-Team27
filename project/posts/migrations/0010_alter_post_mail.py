# Generated by Django 5.0.3 on 2024-03-31 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]