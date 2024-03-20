from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_post_favorites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='favorites',
        ),
    ]
