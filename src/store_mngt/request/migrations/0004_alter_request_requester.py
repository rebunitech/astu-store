# Generated by Django 4.0.4 on 2022-06-24 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('request', '0003_alter_request_requester'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='requester',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL, verbose_name='staffmember'),
        ),
    ]
