# Generated by Django 4.2.7 on 2023-11-18 13:05
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_itineraryitemsorm"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="itineraryitemsorm",
            table="itinerary_items",
        ),
    ]
