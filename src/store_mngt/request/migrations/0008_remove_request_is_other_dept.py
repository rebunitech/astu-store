# Generated by Django 4.0.4 on 2022-06-25 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0007_rename_requesting_request_is_other_dept'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='is_other_dept',
        ),
    ]
