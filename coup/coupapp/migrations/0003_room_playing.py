# Generated by Django 5.0.4 on 2024-04-28 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupapp', '0002_room_delete_party'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='playing',
            field=models.BooleanField(default=False),
        ),
    ]
