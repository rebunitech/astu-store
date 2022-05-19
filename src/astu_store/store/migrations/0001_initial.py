# Generated by Django 3.2.13 on 2022-05-19 11:09

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auser", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpecificationType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "si_unit",
                    models.CharField(
                        help_text="e.g. m, kg, etc.",
                        max_length=255,
                        verbose_name="SI unit",
                    ),
                ),
            ],
            options={
                "verbose_name": "specification type",
                "verbose_name_plural": "specification types",
                "db_table": "specification_type",
            },
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "block",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="block",
                    ),
                ),
                (
                    "room",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="room",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACT", "Active"), ("INA", "Inactive")],
                        default="ACT",
                        help_text="Is the store on use?",
                        max_length=3,
                        verbose_name="status",
                    ),
                ),
                (
                    "remark",
                    models.TextField(blank=True, max_length=255, verbose_name="remark"),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stores",
                        to="auser.department",
                        verbose_name="department",
                    ),
                ),
            ],
            options={
                "verbose_name": "store",
                "verbose_name_plural": "stores",
                "db_table": "store",
                "unique_together": {("block", "room")},
            },
        ),
        migrations.CreateModel(
            name="Shelf",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "shelf_id",
                    models.CharField(
                        default=store.models.uuid_hex,
                        max_length=50,
                        unique=True,
                        verbose_name="shelf id",
                    ),
                ),
                (
                    "no_row",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Number of row(s)",
                    ),
                ),
                (
                    "no_column",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Number of column(s)",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("ACT", "Active"), ("INA", "Inactive")],
                        default="ACT",
                        max_length=3,
                        verbose_name="status",
                    ),
                ),
                (
                    "remark",
                    models.TextField(blank=True, max_length=255, verbose_name="remark"),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shelves",
                        to="store.store",
                        verbose_name="store",
                    ),
                ),
            ],
            options={
                "verbose_name": "shelf",
                "verbose_name_plural": "shelves",
                "db_table": "shelf",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "quantity",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="quantity",
                    ),
                ),
                (
                    "dead_stock_number",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="dead stock number",
                    ),
                ),
                (
                    "year",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="year",
                    ),
                ),
                ("supplier", models.CharField(max_length=255, verbose_name="supplier")),
                (
                    "status",
                    models.CharField(
                        choices=[("ACT", "Active"), ("INA", "Inactive")],
                        default="ACT",
                        max_length=3,
                        verbose_name="status",
                    ),
                ),
                (
                    "remark",
                    models.TextField(blank=True, max_length=255, verbose_name="remark"),
                ),
                (
                    "shelf",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="items",
                        to="store.shelf",
                        verbose_name="shelf",
                    ),
                ),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="store.store",
                        verbose_name="store",
                    ),
                ),
            ],
            options={
                "verbose_name": "item",
                "verbose_name_plural": "items",
                "db_table": "item",
            },
        ),
        migrations.CreateModel(
            name="Specification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.FloatField(verbose_name="value")),
                (
                    "remark",
                    models.TextField(blank=True, max_length=255, verbose_name="remark"),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="store.item",
                        verbose_name="item",
                    ),
                ),
                (
                    "specification_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="specifications",
                        to="store.specificationtype",
                        verbose_name="specification type",
                    ),
                ),
            ],
            options={
                "verbose_name": "specification",
                "verbose_name_plural": "specifications",
                "db_table": "specification",
                "unique_together": {("item", "specification_type")},
            },
        ),
    ]