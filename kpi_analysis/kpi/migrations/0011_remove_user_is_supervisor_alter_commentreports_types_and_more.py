# Generated by Django 5.0.3 on 2024-03-19 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kpi", "0010_alter_commentreports_body_alter_commentreports_types"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_supervisor",
        ),
        migrations.AlterField(
            model_name="commentreports",
            name="types",
            field=models.CharField(
                choices=[
                    ("comment", "Commnet"),
                    ("decision", "Decision"),
                    ("report", "Report"),
                    ("finalcomment", "Final Commnet"),
                    ("finaldecision", "Final Decision"),
                ],
                default="Not Selected",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="roles",
            field=models.CharField(
                blank=True,
                choices=[
                    ("technition", "Technition"),
                    ("admin", "User Manager"),
                    ("analysisManager", "Analysis Manager"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
