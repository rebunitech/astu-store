# Generated by Django 3.2.13 on 2022-06-28 08:09

import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0005_auto_20220628_0236"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="product",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.PROTECT,
                to="inventory.product",
                verbose_name="Product",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="item",
            name="table",
            field=smart_selects.db_fields.ChainedForeignKey(
                auto_choose=True,
                blank=True,
                chained_field="lab",
                chained_model_field="lab",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="items",
                to="inventory.table",
                verbose_name="table",
            ),
        ),
    ]
