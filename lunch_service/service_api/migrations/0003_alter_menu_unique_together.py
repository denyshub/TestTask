# Generated by Django 5.1.1 on 2024-09-09 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("service_api", "0002_alter_menu_restaurant_vote"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="menu",
            unique_together={("restaurant", "date")},
        ),
    ]
