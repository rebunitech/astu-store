# Generated by Django 3.2.13 on 2022-05-18 23:43

import auser.validators
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[auser.validators.PhoneNumberValidator()], verbose_name='phone number')),
                ('location', models.CharField(blank=True, help_text='Physical location.', max_length=200, null=True, verbose_name='address')),
                ('po_box', models.CharField(blank=True, max_length=10, null=True, verbose_name='P.O Box')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('sex', models.CharField(blank=True, choices=[('M', 'MALE'), ('F', 'FEMALE')], max_length=2, null=True, verbose_name='Gender')),
                ('bio', models.TextField(blank=True, help_text='Tell us about your self', null=True, verbose_name='Bio')),
                ('profile_picture', models.ImageField(default='default.svg', upload_to='profile_pictures/', verbose_name='Profile picture')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting account', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('short_name', models.CharField(max_length=10, verbose_name='short name')),
                ('date_created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'school',
                'verbose_name_plural': 'schools',
                'db_table': 'school',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('short_name', models.CharField(max_length=10, verbose_name='short name')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='auser.school', verbose_name='school')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='StoreKeeper',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auser.user')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_keepers', to='auser.department', verbose_name='department')),
            ],
            options={
                'abstract': False,
            },
            bases=('auser.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auser.user')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to='auser.department', verbose_name='department')),
            ],
            options={
                'abstract': False,
            },
            bases=('auser.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolRepresentative',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auser.user')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='school_representatives', to='auser.school', verbose_name='school')),
            ],
            options={
                'abstract': False,
            },
            bases=('auser.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DepartmentRepresentative',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auser.user')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_representatives', to='auser.department', verbose_name='department')),
            ],
            options={
                'abstract': False,
            },
            bases=('auser.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['id'], name='user_id_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='user_username_idx'),
        ),
    ]
