# Generated by Django 5.0.6 on 2024-07-08 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0029_customer_online_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favourite",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.customer",
            ),
        ),
    ]
