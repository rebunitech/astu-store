# Generated by Django 3.2.4 on 2022-07-13 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auser", "0001_initial"),
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="critical_no",
            field=models.IntegerField(help_text="Min number of item that must be in store."),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(max_length=100, verbose_name="slug"),
        ),
        migrations.AlterUniqueTogether(
            name="product",
            unique_together={("slug", "department")},
        ),
    ]