# Generated by Django 4.2.7 on 2024-01-18 13:56
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_itineraryitemsorm_description_itineraryitemsorm_lat_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="itineraryitemsorm",
            name="description",
            field=models.CharField(max_length=500, null=True),
        ),
    ]
