# Generated by Django 4.2.5 on 2023-09-22 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_rename_mainadvertisement_slideimages_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="slideimages",
            options={"ordering": ["time_create", "title"], "verbose_name": "Slide"},
        ),
    ]
