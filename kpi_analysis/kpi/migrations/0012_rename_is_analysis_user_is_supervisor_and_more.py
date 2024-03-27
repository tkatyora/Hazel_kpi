# Generated by Django 5.0.3 on 2024-03-19 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kpi", "0011_remove_user_is_supervisor_alter_commentreports_types_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="is_analysis",
            new_name="is_supervisor",
        ),
        migrations.AlterField(
            model_name="user",
            name="roles",
            field=models.CharField(
                blank=True,
                choices=[
                    ("technition", "Technition"),
                    ("supervisor", "Anaysis Supervisor"),
                    ("admin", "Analysis Manager"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
