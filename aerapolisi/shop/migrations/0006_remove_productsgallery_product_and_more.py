# Generated by Django 4.2.5 on 2023-12-09 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_alter_products_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productsgallery",
            name="product",
        ),
        migrations.AddField(
            model_name="productsgallery",
            name="product",
            field=models.ManyToManyField(default=None, to="shop.products"),
        ),
    ]
