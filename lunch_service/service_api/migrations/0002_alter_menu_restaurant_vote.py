# Generated by Django 5.1.1 on 2024-09-09 16:26

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="menus",
                to="service_api.restaurant",
            ),
        ),
        migrations.CreateModel(
            name="Vote",
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
                ("date", models.DateField(default=datetime.date(2024, 9, 9))),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service_api.employee",
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="service_api.menu",
                    ),
                ),
            ],
        ),
    ]
