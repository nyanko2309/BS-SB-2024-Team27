# Generated by Django 5.0.2 on 2024-03-07 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.TextField(default='name'),
            preserve_default=False,
        ),
    ]