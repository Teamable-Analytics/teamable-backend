# Generated by Django 5.0 on 2024-09-18 02:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_coursemember_sis_user_id_alter_coursemember_lms_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursemember",
            name="name",
        ),
        migrations.AddField(
            model_name="coursemember",
            name="first_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="coursemember",
            name="last_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
