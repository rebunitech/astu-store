# Generated by Django 3.2.4 on 2022-07-23 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20220713_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dead_stock_number',
            field=models.CharField(max_length=250, verbose_name='dead stock number'),
        ),
    ]
