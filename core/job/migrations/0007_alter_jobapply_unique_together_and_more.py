# Generated by Django 5.0.2 on 2024-08-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_companyprofile_name'),
        ('job', '0006_alter_jobapply_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jobapply',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='jobapply',
            constraint=models.UniqueConstraint(fields=('job_seeker', 'job'), name='unique_job_seeker_job', violation_error_message='This job seeker has already applied for this job.'),
        ),
    ]
