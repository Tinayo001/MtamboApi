# Generated by Django 5.1.3 on 2024-12-09 11:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_alter_user_account_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceProvider',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('specialization', models.CharField(choices=[('hvac', 'HVAC Systems'), ('elevators', 'Elevators'), ('generators', 'Generators')], default='hvac', max_length=20)),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(blank=True, max_length=255, null=True)),
                ('company_registration_number', models.CharField(max_length=50)),
            ],
        ),
    ]
