# Generated by Django 3.2.13 on 2022-06-28 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="description",
        ),
    ]