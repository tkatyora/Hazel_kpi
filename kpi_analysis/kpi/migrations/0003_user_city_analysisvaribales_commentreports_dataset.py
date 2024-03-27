# Generated by Django 5.0.3 on 2024-03-27 09:58

import django.db.models.deletion
import kpi.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kpi", "0002_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="city",
            field=models.ManyToManyField(blank=True, to="kpi.city"),
        ),
        migrations.CreateModel(
            name="AnalysisVaribales",
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
                ("name", models.CharField(max_length=100)),
                ("created_on", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommentReports",
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
                ("body", models.TextField(blank=True, null=True)),
                (
                    "types",
                    models.CharField(
                        choices=[
                            ("comment", "Comment"),
                            ("decision", "Decision"),
                            ("report", "Report"),
                            ("finaldecision", "Final Decision"),
                        ],
                        default="Not Selected",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "analysisfile",
                    models.FileField(
                        max_length=255,
                        null=True,
                        upload_to="",
                        validators=[kpi.models.validate_file_extension],
                    ),
                ),
                (
                    "fullReportFile",
                    models.FileField(
                        max_length=255,
                        null=True,
                        upload_to="",
                        validators=[kpi.models.validate_file_extension],
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "Picture",
                    models.ImageField(blank=True, null=True, upload_to="Pictures"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DataSet",
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
                (
                    "types",
                    models.CharField(
                        choices=[
                            ("xlsx", "Excel Format"),
                            ("csv", "CSV(Comma SEparated Values) Format"),
                        ],
                        default="Not Selected",
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        max_length=255,
                        null=True,
                        upload_to="",
                        validators=[kpi.models.validate_file_extension],
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=50, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
