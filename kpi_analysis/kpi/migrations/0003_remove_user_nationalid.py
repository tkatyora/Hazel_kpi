# Generated by Django 5.0.3 on 2024-03-14 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kpi", "0002_rename_accountnumber_user_econetnumber_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="nationalId",
        ),
    ]
