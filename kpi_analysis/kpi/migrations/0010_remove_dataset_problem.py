# Generated by Django 5.0.6 on 2024-05-29 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kpi", "0009_dataset_problem_alter_user_city_alter_user_region_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="problem",
        ),
    ]
