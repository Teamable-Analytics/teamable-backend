# Generated by Django 5.0 on 2024-10-05 19:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_remove_coursemember_name_coursemember_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attribute",
            name="manage_type",
            field=models.CharField(
                choices=[("UserManaged", "UserManaged"), ("Grade", "Grade")],
                default="UserManaged",
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]