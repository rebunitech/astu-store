# Generated by Django 3.2.4 on 2022-07-12 16:09

import astu_inventory.apps.inventory.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.IntegerField(help_text='Block number the lab will be found.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='block')),
                ('room', models.IntegerField(help_text='Lab room number inside block.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='room')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', help_text='Is the lab on use?', max_length=8, verbose_name='status')),
                ('remark', models.TextField(blank=True, help_text='Additional note.', max_length=255, verbose_name='remark')),
                ('department', models.ForeignKey(help_text='Department new lab belongs to.', on_delete=django.db.models.deletion.PROTECT, related_name='labs', to='auser.department', verbose_name='department')),
                ('lab_assistant', models.ManyToManyField(related_name='labs', to=settings.AUTH_USER_MODEL, verbose_name='lab assistant')),
            ],
            options={
                'verbose_name': 'lab',
                'verbose_name_plural': 'labs',
                'unique_together': {('block', 'room')},
            },
        ),
        migrations.CreateModel(
            name='Measurment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'measurement',
                'verbose_name_plural': 'measurements',
                'db_table': 'measurement',
            },
        ),
        migrations.CreateModel(
            name='SpecificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('si_unit', models.CharField(help_text='e.g. m, kg, etc.', max_length=255, verbose_name='SI unit')),
            ],
            options={
                'verbose_name': 'specification type',
                'verbose_name_plural': 'specification types',
                'db_table': 'specification_type',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.CharField(default=astu_inventory.apps.inventory.models.get_ID, help_text='Unique identifier for new table.', max_length=50, unique=True, verbose_name='table ID')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', help_text='Is the table on use?', max_length=8, verbose_name='status')),
                ('remark', models.TextField(blank=True, help_text='Additional note.', max_length=255, verbose_name='remark')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='inventory.lab', verbose_name='lab')),
            ],
            options={
                'verbose_name': 'table',
                'verbose_name_plural': 'tables',
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('remark', models.TextField(verbose_name='remark')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='inventory.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'sub category',
                'verbose_name_plural': 'sub categories',
                'db_table': 'sub_category',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.IntegerField(help_text='Block number the store will be found.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='block')),
                ('room', models.IntegerField(help_text='Store room number inside block.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='room')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', help_text='Is the store on use?', max_length=8, verbose_name='status')),
                ('remark', models.TextField(blank=True, help_text='Additional note.', max_length=255, verbose_name='remark')),
                ('department', models.ForeignKey(help_text='Department new store belongs to.', on_delete=django.db.models.deletion.PROTECT, related_name='stores', to='auser.department', verbose_name='department')),
                ('store_officers', models.ManyToManyField(related_name='stores', to=settings.AUTH_USER_MODEL, verbose_name='store officers')),
            ],
            options={
                'verbose_name': 'store',
                'verbose_name_plural': 'stores',
                'db_table': 'store',
                'permissions': (('can_list_stores', 'Can list stores'),),
                'unique_together': {('block', 'room')},
            },
        ),
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf_id', models.CharField(default=astu_inventory.apps.inventory.models.get_ID, help_text='Unique identifier for new shelf.', max_length=50, unique=True, verbose_name='shelf ID')),
                ('no_row', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Number of row(s)')),
                ('no_column', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Number of column(s)')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', help_text='Is the shelf on use?', max_length=8, verbose_name='status')),
                ('remark', models.TextField(blank=True, help_text='Additional note.', max_length=255, verbose_name='remark')),
                ('store', models.ForeignKey(help_text='Store that the shelf will be stored.', on_delete=django.db.models.deletion.CASCADE, related_name='shelves', to='inventory.store', verbose_name='store')),
            ],
            options={
                'verbose_name': 'shelf',
                'verbose_name_plural': 'shelves',
                'db_table': 'shelf',
                'permissions': (('can_list_shelves', 'Can list shelves'),),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('kind', models.CharField(choices=[('CONSUMABLE', 'Consumable'), ('NON_CONSUMABLE', 'Non-Consumable')], max_length=25, verbose_name='kind')),
                ('critical_no', models.IntegerField(help_text='min number of Item that must be in store')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.category', verbose_name='category')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auser.department', verbose_name='department')),
                ('measurment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.measurment', verbose_name='measurement')),
                ('sub_category', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='category', chained_model_field='category', on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='inventory.subcategory', verbose_name='sub category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity')),
                ('dead_stock_number', models.CharField(max_length=50, verbose_name='dead stock number')),
                ('purpose', models.CharField(choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('BOTH', 'Undergraduate and Postgraduate')], default='BOTH', max_length=10, verbose_name='purpose')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='expiration date')),
                ('year_of_purchase', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900)], verbose_name='year of purchase')),
                ('supplier', models.CharField(blank=True, max_length=255, null=True, verbose_name='supplier')),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=8, verbose_name='status')),
                ('remark', models.TextField(blank=True, max_length=255, verbose_name='remark')),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.lab', verbose_name='lab')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.product', verbose_name='Product')),
                ('shelf', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='store', chained_model_field='store', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='inventory.shelf', verbose_name='shelf')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.store', verbose_name='store')),
                ('table', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='lab', chained_model_field='lab', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='inventory.table', verbose_name='table')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('remark', models.TextField(blank=True, max_length=255, verbose_name='remark')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='inventory.item', verbose_name='item')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='inventory.product', verbose_name='product')),
                ('specification_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='specifications', to='inventory.specificationtype', verbose_name='specification type')),
            ],
            options={
                'verbose_name': 'specification',
                'verbose_name_plural': 'specifications',
                'db_table': 'specification',
                'unique_together': {('product', 'specification_type'), ('item', 'specification_type')},
            },
        ),
    ]
