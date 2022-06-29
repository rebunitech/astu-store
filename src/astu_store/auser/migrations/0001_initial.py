# Generated by Django 3.2.12 on 2022-06-28 19:35

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
                'permissions': [('can_add_college_representative', 'Can add college representative'), ('can_remove_college_representative', 'Can remove college representative'), ('can_view_college_representative', 'Can view college representative'), ('can_change_college_representative', 'Can change college representative'), ('can_delete_college_representative', 'Can delete college representative'), ('can_activate_college_representative', 'Can activate college representative'), ('can_deactivate_college_representative', 'Can deactivate college representative'), ('can_add_department_representative', 'Can add department representative'), ('can_view_department_representative', 'Can view department representative'), ('can_change_department_representative', 'Can change department representative'), ('can_delete_department_representative', 'Can delete department representative'), ('can_activate_department_representative', 'Can activate department representative'), ('can_deactivate_department_representative', 'Can deactivate department representative'), ('can_add_staff_member', 'Can add staff member'), ('can_view_staff_member', 'Can change staff member'), ('can_change_staff_member', 'Can view staff member'), ('can_delete_staff_member', 'Can delete staff member'), ('can_activate_staff_member', 'Can activate staff member'), ('can_deactivate_staff_member', 'Can deactivate staff member'), ('can_add_store_officer', 'Can add store officer'), ('can_view_store_officer', 'Can change store officer'), ('can_change_store_officer', 'Can view store officer'), ('can_delete_store_officer', 'Can delete store officer'), ('can_activate_store_officer', 'Can activate store officer'), ('can_deactivate_store_officer', 'Can deactivate store officer')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('short_name', models.CharField(max_length=10, verbose_name='short name')),
                ('description', models.TextField(max_length=1000, verbose_name='description')),
                ('status', models.CharField(choices=[('active', 'Active'), ('deactivated', 'Deactivated')], default='active', max_length=15, verbose_name='status')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'college',
                'verbose_name_plural': 'colleges',
                'db_table': 'college',
                'permissions': [('can_change_status', 'Can activate status')],
                'unique_together': {('short_name',)},
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('short_name', models.CharField(max_length=10, verbose_name='short name')),
                ('description', models.TextField(max_length=1000, verbose_name='description')),
                ('status', models.CharField(choices=[('active', 'Active'), ('deactivated', 'Deactivated')], default='active', max_length=15, verbose_name='status')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('college', models.ForeignKey(limit_choices_to={'status': 'active'}, on_delete=django.db.models.deletion.PROTECT, related_name='departments', to='auser.college', verbose_name='college')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
                'db_table': 'department',
                'unique_together': {('college', 'short_name')},
            },
        ),
        migrations.CreateModel(
            name='CollegeUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auser.user')),
                ('college', models.ForeignKey(limit_choices_to={'status': 'active'}, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='auser.college', verbose_name='college')),
                ('department', models.ForeignKey(limit_choices_to={'status': 'active'}, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='auser.department', verbose_name='department')),
            ],
            options={
                'verbose_name': 'in college user',
                'verbose_name_plural': 'in college users',
                'db_table': 'college_user',
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
