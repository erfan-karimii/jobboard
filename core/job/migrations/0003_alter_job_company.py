# Generated by Django 5.0.2 on 2024-08-25 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_companyprofile_name'),
        ('job', '0002_alter_job_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='account.companyprofile'),
        ),
    ]
