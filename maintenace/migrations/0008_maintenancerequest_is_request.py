# Generated by Django 3.2.12 on 2022-06-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenace', '0007_remove_maintenancerequest_is_requeste'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='is_request',
            field=models.BooleanField(default=True),
        ),
    ]
