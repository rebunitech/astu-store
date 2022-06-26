# Generated by Django 3.2.13 on 2022-06-25 18:25

import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auser", "0002_alter_user_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collegeuser",
            name="department",
            field=smart_selects.db_fields.ChainedForeignKey(
                chained_field="college",
                chained_model_field="college",
                limit_choices_to={"status": "active"},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="staffs",
                to="auser.department",
                verbose_name="department",
            ),
        ),
    ]