# Generated by Django 3.2.13 on 2022-06-25 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auser", "0003_alter_collegeuser_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="college",
            name="description",
            field=models.TextField(max_length=300, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="department",
            name="description",
            field=models.TextField(max_length=300, verbose_name="description"),
        ),
    ]