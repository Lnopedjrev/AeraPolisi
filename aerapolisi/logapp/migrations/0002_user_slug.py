# Generated by Django 4.2.5 on 2023-09-23 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="slug",
            field=models.SlugField(
                default="sosat", max_length=255, unique=True, verbose_name="Profile"
            ),
        ),
    ]
