# Generated by Django 3.2.12 on 2022-06-26 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenace', '0019_maintenancerequest_is_damaged'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='decline_reason',
            field=models.TextField(null=True),
        ),
    ]
