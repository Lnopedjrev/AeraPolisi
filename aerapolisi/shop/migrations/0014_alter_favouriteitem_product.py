# Generated by Django 4.2.5 on 2024-04-16 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_remove_products_owner_alter_productsgallery_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favouriteitem",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="shop.productoffers",
            ),
        ),
    ]
