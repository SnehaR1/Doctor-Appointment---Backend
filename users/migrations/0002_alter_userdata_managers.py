# Generated by Django 4.2.11 on 2024-04-01 16:10

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="userdata",
            managers=[
                ("objects", users.models.UserManager()),
            ],
        ),
    ]