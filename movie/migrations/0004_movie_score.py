# Generated by Django 3.1 on 2022-05-03 15:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movie", "0003_auto_20211228_0153"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="score",
            field=models.FloatField(
                default=5.0,
                validators=[
                    django.core.validators.MinValueValidator(0.0),
                    django.core.validators.MaxValueValidator(10.0),
                ],
            ),
        ),
    ]
