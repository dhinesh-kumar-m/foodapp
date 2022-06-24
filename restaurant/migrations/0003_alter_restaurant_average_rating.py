# Generated by Django 4.0.5 on 2022-06-24 06:16
import django.core.validators
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0002_alter_restaurant_average_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="average_rating",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(5.0),
                ],
            ),
        ),
    ]