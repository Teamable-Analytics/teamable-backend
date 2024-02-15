# Generated by Django 5.0 on 2024-02-15 20:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="course",
            options={},
        ),
        migrations.AlterModelOptions(
            name="section",
            options={},
        ),
        migrations.CreateModel(
            name="CourseMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "role",
                    models.CharField(
                        choices=[("S", "Student"), ("I", "Instructor")], max_length=1
                    ),
                ),
                ("lms_id", models.CharField(blank=True, max_length=100)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.course"
                    ),
                ),
                (
                    "sections",
                    models.ManyToManyField(
                        related_name="section_members", to="app.section"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Relationship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("F", "friend"), ("E", "enemy")], max_length=1
                    ),
                ),
                (
                    "from_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="outbound_relationships",
                        to="app.coursemember",
                    ),
                ),
                (
                    "to_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inbound_relationships",
                        to="app.coursemember",
                    ),
                ),
            ],
            options={
                "unique_together": {("from_member", "to_member")},
            },
        ),
    ]
