# Generated by Django 5.0.2 on 2024-08-18 08:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_userprofile_resume_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
