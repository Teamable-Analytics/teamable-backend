# Generated by Django 5.0 on 2024-09-11 02:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_team_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="coursemember",
            name="sis_user_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="coursemember",
            name="lms_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddConstraint(
            model_name="coursemember",
            constraint=models.UniqueConstraint(
                fields=("course", "lms_id"), name="unique_lms_id_in_course"
            ),
        ),
        migrations.AddConstraint(
            model_name="coursemember",
            constraint=models.UniqueConstraint(
                fields=("course", "sis_user_id"), name="unique_sis_user_id_in_course"
            ),
        ),
    ]
