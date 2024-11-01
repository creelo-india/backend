# Generated by Django 5.1 on 2024-10-19 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creelo_app', '0003_productimage_image_link_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_featured_product',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_new_arrivals',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='is_top_selling_product',
            field=models.BooleanField(default=False),
        ),
    ]