# Generated by Django 5.2.4 on 2025-07-07 05:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VTS_Admin_Portal', '0004_remove_trainer_phone_remove_trainer_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('category', models.CharField(choices=[('design', 'Design'), ('development', 'Development'), ('fullstack', 'Fullstack'), ('softskills', 'Soft Skills')], max_length=50)),
                ('duration_weeks', models.PositiveIntegerField(help_text='Duration in weeks')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('fee', models.DecimalField(decimal_places=2, help_text='Course fee in INR', max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='VTS_Admin_Portal.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Trainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='trainees/')),
                ('address_line1', models.CharField(blank=True, max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(blank=True, max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=10)),
                ('country', models.CharField(default='India', max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('assigned_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainees', to='VTS_Admin_Portal.course')),
                ('assigned_trainer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trainees', to='VTS_Admin_Portal.trainer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trainee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
